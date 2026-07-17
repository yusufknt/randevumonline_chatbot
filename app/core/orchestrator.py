from __future__ import annotations

import asyncio
import logging
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

from app.channels import instagram as ig
from app.channels import whatsapp as wa
from app.channels.instagram import flow as ig_flow
from app.channels.whatsapp import flow_sender as flow_mod
from app.core import ai
from app.core.tools import ToolContext
from app.core.db import (
    append_conversation_message,
    claim_inbound_message,
    find_business_by_ig_user_id,
    find_business_by_wa_phone_number_id,
    update_conversation_context,
    upsert_conversation,
    upsert_customer_by_instagram,
    upsert_customer_by_whatsapp,
)

log = logging.getLogger(__name__)


def _is_in_quiet_hours(business: dict) -> bool:
    qh = (business.get("ai_settings") or {}).get("quiet_hours")
    if not qh:
        return False
    tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
    now_l = datetime.now(tz).time()
    h, m = qh["start"].split(":")
    start = time(int(h), int(m))
    h, m = qh["end"].split(":")
    end = time(int(h), int(m))
    if start <= end:
        return start <= now_l < end
    # gece yarısını aşan aralık
    return now_l >= start or now_l < end


def _fallback_message(business: dict, default: str) -> str:
    return (business.get("ai_settings") or {}).get("fallback_message") or default


# Aynı kullanıcıya sessiz saatler bildirimi en fazla bu aralıkta bir gönderilir.
QUIET_NOTICE_DEBOUNCE_SECONDS = 6 * 3600


async def _maybe_quiet_notice(
    business: dict, conv: dict, channel: str, recipient_id: str,
) -> None:
    """Sessiz saatlerde tek seferlik (debounce'lu) bilgilendirme gönderir.

    `ai_settings.quiet_hours_message` tanımlı değilse hiçbir şey yapmaz (mevcut
    'tamamen sessiz' davranışı korunur) — geriye dönük uyumlu.
    """
    msg = (business.get("ai_settings") or {}).get("quiet_hours_message")
    if not msg:
        return
    last = (conv.get("context") or {}).get("quiet_notice_at")
    if isinstance(last, datetime):
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        if (datetime.now(timezone.utc) - last).total_seconds() < QUIET_NOTICE_DEBOUNCE_SECONDS:
            return
    try:
        if channel == "whatsapp":
            await wa.send_text(business, recipient_id, msg)
        else:
            await ig.send_text(business, recipient_id, msg)
    except Exception:
        log.exception("Sessiz saatler bildirimi gönderilemedi (%s)", channel)
        return
    await update_conversation_context(
        conv["_id"], {"quiet_notice_at": datetime.now(timezone.utc)}
    )
    await _log_assistant_message(conv["_id"], msg)


async def _log_user_message(
    conv_id, inbound_text: str, inbound_msg_id: str,
    interactive_type: str | None = None,
) -> None:
    await append_conversation_message(conv_id, {
        "role": "user",
        "content": inbound_text,
        "timestamp": datetime.now(timezone.utc),
        "channel_msg_id": inbound_msg_id,
        "tool_name": None,
        "tool_args": ({"interactive_type": interactive_type}
                      if interactive_type else None),
    })


async def _ig_acknowledge(business: dict, sender_id: str) -> None:
    """Mesaj alındığını göster: önce 'görüldü', sonra 'yazıyor…'.

    Doc en iyi pratiği; AI turu saniyeler sürebildiğinden kullanıcı yok sayılmış
    hissetmez. Hata olursa akışı bozmaz.
    """
    # İkisini paralel gönder (seri await ~0.6s gecikme ekliyordu). Hata akışı bozmaz.
    results = await asyncio.gather(
        ig.send_action(business, sender_id, "mark_seen"),
        ig.send_action(business, sender_id, "typing_on"),
        return_exceptions=True,
    )
    for action, res in zip(("mark_seen", "typing_on"), results):
        if isinstance(res, Exception):
            log.debug("IG sender_action '%s' gönderilemedi", action, exc_info=res)


async def _log_assistant_message(conv_id, text: str) -> None:
    await append_conversation_message(conv_id, {
        "role": "assistant",
        "content": text,
        "timestamp": datetime.now(timezone.utc),
        "channel_msg_id": None,
        "tool_name": None,
        "tool_args": None,
    })


def _booking_eligibility(business: dict, customer: dict) -> str | None:
    ai = business.get("ai_settings") or {}
    who = ai.get("online_booking_who", "registered_only")

    if who == "nobody":
        return _fallback_message(
            business,
            "Şu anda online randevu alımı kapalıdır. Lütfen bizi arayın.",
        )

    if who == "registered_only" and (customer.get("total_appointments") or 0) == 0:
        return (
            "Online randevu sistemimiz şu an yalnız mevcut müşterilerimize "
            "açık. Sizi personelimize aktarıyorum."
        )

    if customer.get("is_blocked"):
        return (
            "Hesabınız randevu alımına kapatılmıştır. Detay için lütfen "
            "bizi arayın."
        )

    no_show_limit = int(ai.get("no_show_block_limit", 2))
    if (customer.get("no_show_count") or 0) >= no_show_limit:
        return (
            "Önceki randevularınıza gelmediğiniz için online randevu alımı "
            "geçici olarak kapalıdır. Lütfen bizi arayın."
        )
    return None


async def handle_whatsapp_payload(payload: dict) -> None:
    for inbound in wa.parse_inbound(payload):
        if not await claim_inbound_message("whatsapp", inbound.message_id):
            log.info("[whatsapp] tekrar webhook atlandı mid=%s", inbound.message_id)
            continue
        business = await find_business_by_wa_phone_number_id(inbound.phone_number_id)
        if not business:
            log.warning("Eşleşen business yok: phone_number_id=%s",
                        inbound.phone_number_id)
            continue

        customer = await upsert_customer_by_whatsapp(
            business["_id"], inbound.wa_id, name=inbound.profile_name
        )
        conv = await upsert_conversation(
            business["_id"], "whatsapp", inbound.wa_id, customer_id=customer["_id"]
        )
        await _log_user_message(
            conv["_id"], inbound.text, inbound.message_id,
            interactive_type=inbound.interactive_type,
        )

        if _is_in_quiet_hours(business):
            log.info("Quiet hours — yanıt vermiyor (biz=%s)",
                     business.get("business_id"))
            await _maybe_quiet_notice(business, conv, "whatsapp", inbound.wa_id)
            continue

        log.info("[whatsapp ← %s] %s", inbound.wa_id, inbound.text)

        if inbound.interactive_type == "nfm_reply" and inbound.nfm_response_json:
            try:
                reply = flow_mod.summary_text_from_nfm_reply(
                    inbound.nfm_response_json
                )
            except Exception:
                log.exception("nfm_reply özet metni oluşturulamadı")
                reply = _fallback_message(
                    business,
                    "Randevunuz alındı. Detayları kısa süre içinde iletiyoruz.",
                )
        else:
            gate = _booking_eligibility(business, customer)
            if gate:
                reply = gate
            else:
                try:
                    result = await flow_mod.send_booking_flow(
                        business, conv, inbound.wa_id,
                    )
                except Exception:
                    log.exception("Flow CTA mesajı gönderilemedi")
                    result = {"error": "send_failed"}

                if result.get("ok"):
                    # CTA mesajı zaten gönderildi; ek text yok.
                    continue
                log.warning("Flow CTA gönderilemedi: %s", result)
                reply = _fallback_message(
                    business,
                    "Randevu sistemimize şu an erişemiyoruz. "
                    "Sizi personelimize aktarıyorum.",
                )

        if not reply:
            continue

        log.info("[whatsapp → %s] %s", inbound.wa_id, reply)
        await _log_assistant_message(conv["_id"], reply)
        try:
            await wa.send_text(business, inbound.wa_id, reply)
        except Exception:
            log.exception("WA send_text başarısız")


async def handle_instagram_payload(payload: dict) -> None:
    for inbound in ig.parse_inbound(payload):
        if not await claim_inbound_message("instagram", inbound.message_id):
            log.info("[instagram] tekrar webhook atlandı mid=%s", inbound.message_id)
            continue
        business = await find_business_by_ig_user_id(inbound.ig_user_id)
        if not business:
            log.warning("Eşleşen business yok: ig_user_id=%s", inbound.ig_user_id)
            continue

        customer = await upsert_customer_by_instagram(
            business["_id"], inbound.sender_id
        )
        conv = await upsert_conversation(
            business["_id"], "instagram", inbound.sender_id,
            customer_id=customer["_id"],
        )
        await _log_user_message(
            conv["_id"], inbound.text or "", inbound.message_id or "",
            interactive_type=(inbound.kind if inbound.kind != "text" else None),
        )

        if _is_in_quiet_hours(business):
            log.info("Quiet hours — yanıt vermiyor (biz=%s)",
                     business.get("business_id"))
            await _maybe_quiet_notice(business, conv, "instagram", inbound.sender_id)
            continue

        log.info("[instagram ← %s] (%s) %s",
                 inbound.sender_id, inbound.kind, inbound.text or inbound.payload)

        # Görüldü + yazıyor göstergeleri (yanıt vereceğimiz kesinleştikten sonra).
        await _ig_acknowledge(business, inbound.sender_id)

        state = conv.get("state")
        # Görsel/sesli/desteklenmeyen medya → nazik fallback (handoff'ta sessiz).
        if inbound.kind == "unsupported":
            sent_texts = await _instagram_unsupported(business, conv, inbound)
        # Reklam / ig.me referral girişi → karşılama menüsü.
        elif inbound.kind == "referral":
            sent_texts = await _instagram_deterministic(
                business, conv, customer, inbound
            )
        # Serbest metin + "Müşteri Temsilcisi" (AI) modu → Groq'a yönlendir.
        elif not inbound.payload and state == ig_flow.STATE_AI_ACTIVE:
            sent_texts = await _instagram_ai_reply(business, conv, customer, inbound)
        # Gerçek personele aktarılmış serbest metin → bot otomatik yanıt vermez.
        elif not inbound.payload and state == ig_flow.STATE_HUMAN_HANDOFF:
            log.info("[instagram] human_handoff — bot sessiz (sender=%s)",
                     inbound.sender_id)
            continue
        else:
            sent_texts = await _instagram_deterministic(
                business, conv, customer, inbound
            )

        for text in sent_texts:
            log.info("[instagram → %s] %s", inbound.sender_id, text)
            await _log_assistant_message(conv["_id"], text)


async def _instagram_deterministic(
    business: dict, conv: dict, customer: dict, inbound,
) -> list[str]:
    """Menü/postback ve serbest-metin regex dispatch'i (AI'sız klasik akış)."""
    # Randevu isteği ise eligibility kontrolü yap
    is_booking_request = (
        inbound.payload == ig_flow.PB_BOOK
        or (not inbound.payload and ig_flow.RX_BOOK.search(inbound.text or ""))
    )
    if is_booking_request:
        gate = _booking_eligibility(business, customer)
        if gate:
            await ig.send_text(business, inbound.sender_id, gate)
            return [gate]

    try:
        return await ig_flow.handle_event(business, conv, inbound)
    except Exception:
        log.exception("ig_flow.handle_event başarısız — fallback dönülüyor")
        fb = _fallback_message(
            business,
            "İsteğinizi anlayamadım, biraz sonra tekrar dener misiniz?",
        )
        try:
            await ig.send_text(business, inbound.sender_id, fb)
            return [fb]
        except Exception:
            log.exception("IG fallback send_text de başarısız")
            return []


async def _instagram_unsupported(business: dict, conv: dict, inbound) -> list[str]:
    """Görsel/sesli/dosya/sticker gibi metin dışı mesajlara nazik yanıt.

    Personele aktarılmış sohbette sessiz kalır (insan ajan görsün diye).
    """
    if conv.get("state") == ig_flow.STATE_HUMAN_HANDOFF:
        return []
    msg = _fallback_message(
        business,
        "Mesajınızı aldım ancak içeriğini buradan görüntüleyemiyorum. "
        "Size yardımcı olabilmem için kısaca yazabilir misiniz?",
    )
    try:
        await ig.send_text(business, inbound.sender_id, msg)
        return [msg]
    except Exception:
        log.exception("IG unsupported fallback gönderilemedi")
        return []


async def _instagram_ai_reply(
    business: dict, conv: dict, customer: dict, inbound,
) -> list[str]:
    """Müşteri Temsilcisi (Groq AI) turu: DB bilgilerine göre yanıt üretir."""
    ctx = ToolContext(business, customer, conv)
    history = conv.get("messages") or []
    try:
        reply, tool_log = await ai.run_turn(ctx, history, inbound.text or "")
    except Exception:
        log.exception("Groq AI turu başarısız — fallback dönülüyor")
        reply = _fallback_message(
            business,
            "Şu an yanıt veremedim, lütfen birazdan tekrar yazar mısınız?",
        )
        tool_log = []

    # AI'nın çağırdığı tool turlarını konuşma geçmişine işle (denetim/iz için)
    for msg in tool_log:
        await append_conversation_message(conv["_id"], msg)

    if not reply:
        return []
    try:
        await ig.send_text(business, inbound.sender_id, reply)
    except Exception:
        log.exception("IG AI yanıtı gönderilemedi")
        return []
    return [reply]
