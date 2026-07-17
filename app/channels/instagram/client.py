from __future__ import annotations

import hashlib
import hmac
import logging
from dataclasses import dataclass
from typing import Literal

import httpx

from app.core.config import get_settings
from app.core.db import get_secret
from app.core.format import truncate

log = logging.getLogger(__name__)

# Meta IG Messaging API karakter/öğe limitleri
QR_TITLE_MAX = 20            # karakter
BTN_TITLE_MAX = 20          # karakter
BTN_TEMPLATE_TEXT_MAX = 640  # karakter (doc: "up to 640 characters")
# Text mesaj limiti BYTE cinsindendir: "Message text must be UTF-8 and be a 1000
# bytes or less." Türkçe harfler (ç,ğ,ş,ı,ö,ü) 2 byte, emoji 4 byte olduğundan
# karakter bazlı kesme yanlış olur → byte bazlı kes/parçala.
TEXT_MAX_BYTES = 1000
QR_MAX_COUNT = 13
BTN_MAX_COUNT = 3
GENERIC_TITLE_MAX = 80
GENERIC_SUBTITLE_MAX = 80
GENERIC_MAX_ELEMENTS = 10
GENERIC_BTN_PER_ELEMENT = 3

InboundKind = Literal["text", "quick_reply", "postback", "unsupported", "referral"]


@dataclass
class InstagramInboundMessage:
    ig_user_id: str
    sender_id: str
    text: str
    message_id: str
    kind: InboundKind = "text"
    payload: str | None = None


def verify_signature(body: bytes, signature_header: str | None) -> bool:
    settings = get_settings()
    if not settings.ig_app_secret:
        log.warning("IG_APP_SECRET ayarlı değil — signature doğrulama atlanıyor.")
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        log.warning("IG imza header yok/format hatalı: %r", signature_header)
        return False
    expected = hmac.new(
        settings.ig_app_secret.encode(), body, hashlib.sha256
    ).hexdigest()
    received = signature_header.split("=", 1)[1]
    ok = hmac.compare_digest(expected, received)
    if not ok:
        # TEŞHİS: Facebook App Secret ile imzalanıyor mu?
        wa_match = False
        if settings.wa_app_secret:
            wa_expected = hmac.new(
                settings.wa_app_secret.encode(), body, hashlib.sha256
            ).hexdigest()
            wa_match = hmac.compare_digest(wa_expected, received)
        log.warning(
            "IG imza UYUŞMADI | IG_secret_ilk4=%s eşleşti=%s | "
            "WA(Facebook)_secret eşleşti=%s | alınan=%s body_len=%d",
            settings.ig_app_secret[:4], ok, wa_match, received, len(body),
        )
    return ok


def _synthetic_mid(kind: str, sender: str, ev: dict, payload: str) -> str:
    """mid'i olmayan olaylar (ice breaker / persistent menu postback'i, referral)
    için kararlı bir idempotency anahtarı üretir.

    Meta bu olaylarda `mid` göndermez; ayrıca aynı webhook teslimatını birden
    çok kez (farklı IP'lerden) yeniden dener. Olay `timestamp`'ı (epoch ms) bir
    teslimatın tüm tekrarlarında aynıdır → sender+ts+payload tekrarları eler,
    gerçekten ayrı tıklamalar (farklı ts) geçer. timestamp yoksa "" döner
    (dedup yapılamaz, eski davranış).
    """
    ts = ev.get("timestamp")
    if ts is None:
        return ""
    return f"{kind}:{sender}:{ts}:{payload}"


def parse_inbound(payload: dict) -> list[InstagramInboundMessage]:
    out: list[InstagramInboundMessage] = []
    if payload.get("object") != "instagram":
        return out
    for entry in payload.get("entry") or []:
        ig_user_id = entry.get("id")
        for ev in entry.get("messaging") or []:
            sender = (ev.get("sender") or {}).get("id")
            if not sender:
                continue

            # Postback (button template / persistent menu / ice breaker tıklaması)
            pb = ev.get("postback")
            if pb:
                pb_payload = pb.get("payload")
                if not pb_payload:
                    continue
                out.append(InstagramInboundMessage(
                    ig_user_id=ig_user_id,
                    sender_id=sender,
                    text=pb.get("title") or "",
                    # Ice breaker / persistent menu postback'lerinde mid gelmez;
                    # yoksa sentetik anahtarla dedup et (mesaj yağmurunu önler).
                    message_id=pb.get("mid")
                    or _synthetic_mid("pb", sender, ev, pb_payload),
                    kind="postback",
                    payload=pb_payload,
                ))
                continue

            msg = ev.get("message") or {}

            # Üst düzey referral (ig.me linki / mevcut sohbette OPEN_THREAD).
            # message/postback olmayan saf referral olayı → karşılama tetikler.
            top_ref = ev.get("referral")
            if top_ref and not msg:
                ref = top_ref.get("ref") or "REFERRAL"
                out.append(InstagramInboundMessage(
                    ig_user_id=ig_user_id,
                    sender_id=sender,
                    text="",
                    # Bu olayların mid'i yok → sentetik anahtarla dedup.
                    message_id=_synthetic_mid("ref", sender, ev, ref),
                    kind="referral",
                    payload=ref,
                ))
                continue

            if msg.get("is_echo"):
                continue
            if msg.get("is_deleted"):
                continue  # silinen mesaja yanıt verme
            mid = msg.get("mid")

            # Quick Reply seçimi: message.quick_reply.payload + message.text(title)
            qr = msg.get("quick_reply")
            if qr and qr.get("payload"):
                title = msg.get("text") or ""
                if not mid:
                    continue
                out.append(InstagramInboundMessage(
                    ig_user_id=ig_user_id,
                    sender_id=sender,
                    text=title,
                    message_id=mid,
                    kind="quick_reply",
                    payload=qr["payload"],
                ))
                continue

            # Düz text
            text = msg.get("text")
            if text and mid:
                out.append(InstagramInboundMessage(
                    ig_user_id=ig_user_id,
                    sender_id=sender,
                    text=text,
                    message_id=mid,
                    kind="text",
                    payload=None,
                ))
                continue

            # Metin yok ama içerik var: görsel/sesli/dosya/share/story mention ya
            # da desteklenmeyen medya (sticker/gif). Bot sessiz kalmamalı.
            if mid and (msg.get("attachments") or msg.get("is_unsupported")):
                out.append(InstagramInboundMessage(
                    ig_user_id=ig_user_id,
                    sender_id=sender,
                    text="",
                    message_id=mid,
                    kind="unsupported",
                    payload=None,
                ))
    return out


# ---------- Outbound helpers ----------

def _utf8_truncate(text: str, max_bytes: int) -> str:
    """Metni UTF-8 byte sınırına göre kırpar; çok-baytlı karakteri ortadan bölmez."""
    if not text:
        return ""
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    return encoded[:max_bytes].decode("utf-8", "ignore")


def split_text_by_bytes(text: str, max_bytes: int = TEXT_MAX_BYTES) -> list[str]:
    """Uzun metni UTF-8 byte sınırını aşmayan parçalara böler.

    Mümkün olduğunda boşluk/satır sonunda böler; tek bir devasa kelime varsa
    byte sınırında zorla keser. Çok-baytlı karakter asla ikiye bölünmez.
    """
    if len(text.encode("utf-8")) <= max_bytes:
        return [text]

    chunks: list[str] = []
    current = ""
    cur_bytes = 0
    for ch in text:
        ch_bytes = len(ch.encode("utf-8"))
        if cur_bytes + ch_bytes > max_bytes:
            cut = max(current.rfind(" "), current.rfind("\n"))
            if cut > max_bytes // 2:  # makul bir boşluk varsa orada böl
                head, tail = current[:cut], current[cut + 1:]
            else:
                head, tail = current, ""
            chunks.append(head)
            current = tail + ch
            cur_bytes = len(current.encode("utf-8"))
        else:
            current += ch
            cur_bytes += ch_bytes
    if current:
        chunks.append(current)

    return [c.strip() for c in chunks if c.strip()] or [""]


def _ig_endpoint(business: dict) -> tuple[str, str]:
    settings = get_settings()
    ig_cfg = (business.get("channels") or {}).get("instagram") or {}
    if not ig_cfg.get("enabled"):
        raise RuntimeError("Bu işletme için Instagram kanalı kapalı.")
    ig_user_id = ig_cfg["ig_user_id"]
    token = get_secret(ig_cfg["access_token_ref"])
    url = f"{settings.ig_graph_base_url}/{ig_user_id}/messages"
    return url, token


async def _post(url: str, token: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json=payload,
        )
        if resp.status_code >= 400:
            log.error("IG send HTTP %s: %s", resp.status_code, resp.text)
            if resp.status_code in (400, 401) and "OAuth" in resp.text:
                log.error(
                    "IG token geçersiz/süresi dolmuş olabilir → "
                    "`python -m scripts ig-refresh-token <slug>` ile yenileyin."
                )
            resp.raise_for_status()
        return resp.json()


async def send_text(business: dict, sender_id: str, text: str) -> dict:
    """Metni gönderir; 1000 byte'ı aşarsa sırayla birden çok mesaja böler."""
    url, token = _ig_endpoint(business)
    resp: dict = {}
    for chunk in split_text_by_bytes(text or ""):
        resp = await _post(url, token, {
            "recipient": {"id": sender_id},
            "message": {"text": chunk},
        })
    return resp


async def send_action(business: dict, sender_id: str, action: str) -> dict:
    """Sender action gönderir: 'mark_seen' | 'typing_on' | 'typing_off'.

    Doc kısıtı: bu istek yalnız `recipient` + `sender_action` içermeli; metin/
    template ayrı istekte gönderilmeli.
    """
    url, token = _ig_endpoint(business)
    return await _post(url, token, {
        "recipient": {"id": sender_id},
        "sender_action": action,
    })


async def send_quick_replies(
    business: dict,
    sender_id: str,
    text: str,
    options: list[dict],
) -> dict:
    if not options:
        raise ValueError("Quick Replies için en az 1 öğe gerekli.")
    options = options[:QR_MAX_COUNT]
    quick_replies = [
        {
            "content_type": "text",
            "title": truncate(o["title"], QR_TITLE_MAX),
            "payload": o["payload"],
        }
        for o in options
    ]
    url, token = _ig_endpoint(business)
    payload = {
        "recipient": {"id": sender_id},
        "message": {
            "text": _utf8_truncate(text, TEXT_MAX_BYTES),
            "quick_replies": quick_replies,
        },
    }
    return await _post(url, token, payload)


def url_button(title: str, url: str) -> dict:
    return {
        "type": "web_url",
        "title": truncate(title, BTN_TITLE_MAX),
        "url": url,
    }


def postback_button(title: str, payload: str) -> dict:
    return {
        "type": "postback",
        "title": truncate(title, BTN_TITLE_MAX),
        "payload": payload,
    }


async def send_button_template(
    business: dict,
    sender_id: str,
    text: str,
    buttons: list[dict],
) -> dict:
    if not buttons:
        raise ValueError("Button Template için en az 1 buton gerekli.")
    buttons = buttons[:BTN_MAX_COUNT]
    url, token = _ig_endpoint(business)
    payload = {
        "recipient": {"id": sender_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": truncate(text, BTN_TEMPLATE_TEXT_MAX),
                    "buttons": buttons,
                },
            }
        },
    }
    return await _post(url, token, payload)


def carousel_element(
    title: str,
    subtitle: str | None = None,
    image_url: str | None = None,
    default_url: str | None = None,
    buttons: list[dict] | None = None,
) -> dict:
    el: dict = {"title": truncate(title, GENERIC_TITLE_MAX)}
    if subtitle:
        el["subtitle"] = truncate(subtitle, GENERIC_SUBTITLE_MAX)
    if image_url:
        el["image_url"] = image_url
    if default_url:
        el["default_action"] = {"type": "web_url", "url": default_url}
    if buttons:
        el["buttons"] = buttons[:GENERIC_BTN_PER_ELEMENT]
    return el


async def send_generic_template(
    business: dict, sender_id: str, elements: list[dict],
) -> dict:
    if not elements:
        raise ValueError("Generic Template için en az 1 element gerekli.")
    elements = elements[:GENERIC_MAX_ELEMENTS]
    url, token = _ig_endpoint(business)
    payload = {
        "recipient": {"id": sender_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {"template_type": "generic", "elements": elements},
            }
        },
        "messaging_type": "RESPONSE",
    }
    return await _post(url, token, payload)


