from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from urllib.parse import quote_plus
from zoneinfo import ZoneInfo

from app.channels.instagram.client import (
    BTN_TEMPLATE_TEXT_MAX,
    InstagramInboundMessage,
    postback_button,
    send_button_template,
    send_quick_replies,
    send_text,
    url_button,
)
from app.core import ai
from app.core.availability import WEEKDAY_NAMES
from app.core.db import (
    list_active_services,
    record_escalation,
    update_conversation_context,
)
from app.core.format import WEEKDAY_TR, format_price, truncate

log = logging.getLogger(__name__)


PB_MENU         = "IG:MENU"
PB_BOOK         = "IG:BOOK"
PB_SERVICES     = "IG:SERVICES"
PB_SERVICES_ALL = "IG:SERVICES_ALL"
PB_INFO         = "IG:INFO"
PB_HUMAN        = "IG:HUMAN"   # "Müşteri Temsilcisi" → AI sohbet modunu başlatır
PB_APPTS        = "IG:APPTS"
PB_CAT_PREFIX   = "IG:CAT:"

# Hizmet listesini tek seferde (gerekirse birden çok mesaj) gösterme eşiği.
# send_text 1000 byte'lık parçalara böldüğünden bu ~bu kadar mesaja denk gelir.
# Bu byte sınırını aşan (çok sayıda hizmetli) işletmelerde mesaj yağmuru
# olmaması için kategori seçim menüsüne (fallback) düşülür.
SERVICES_INLINE_MAX_BYTES = 3500

# Konuşma durumları (conversations.state)
STATE_GREETING      = "greeting"       # Varsayılan / menü akışı
STATE_AI_ACTIVE     = "ai_active"      # Müşteri Temsilcisi (AI) sohbeti açık
STATE_HUMAN_HANDOFF = "human_handoff"  # Gerçek personele aktarıldı; bot sessiz

# Dispatch sırası: APPT > SERVICES > BOOK > INFO > HUMAN
RX_APPT = re.compile(
    r"\b(randevum\b|randevular[iı]m|iptal\s*et|ne\s*zaman\b|ge[çc]mi[şs]\s*randevu|mevcut\s*randevu)",
    re.IGNORECASE,
)
RX_SERVICES = re.compile(
    r"\b(fiyat|[uü]cret|kaç\s*para|kac\s*para|ne\s*kadar|pahal[ıi]|[uü]cretli|hizmet|menü|menu|liste|tarife)",
    re.IGNORECASE,
)
RX_BOOK = re.compile(
    r"\b(randevu|rezervasyon|appointment|book|saat\s*al)",
    re.IGNORECASE,
)
RX_INFO = re.compile(
    r"\b(adres|nerede|nerdesin|neredesiniz|konum|açık\s*m[ıi]|kaça\s*kadar|telefon|numara|ileti[şs]im)",
    re.IGNORECASE,
)
RX_HUMAN = re.compile(
    r"\b(yetkili|personel|insan|temsilci|canlı\s*destek|bot\s*değil)",
    re.IGNORECASE,
)

MENU_DEBOUNCE_SECONDS = 300  # 5 dakika


# ---------- Ana giriş noktası ----------

async def handle_event(
    business: dict,
    conversation: dict,
    inbound: InstagramInboundMessage,
) -> list[str]:
    sender_id = inbound.sender_id

    if inbound.payload:
        return await _dispatch_payload(business, conversation, sender_id,
                                       inbound.payload)

    text = (inbound.text or "").strip()
    if not text:
        return await _send_main_menu(business, conversation, sender_id)

    if RX_APPT.search(text):
        return await _send_appointment_info(business, sender_id)
    if RX_SERVICES.search(text):
        return await _send_services(business, sender_id)
    if RX_BOOK.search(text):
        return await _send_book(business, conversation, sender_id)
    if RX_INFO.search(text):
        return await _send_info(business, sender_id)
    if RX_HUMAN.search(text):
        return await _enter_customer_service(business, conversation, sender_id)

    return await _send_main_menu(business, conversation, sender_id)


async def _dispatch_payload(
    business: dict, conversation: dict, sender_id: str, payload: str,
) -> list[str]:
    if payload == PB_HUMAN:
        return await _enter_customer_service(business, conversation, sender_id)
    # Müşteri Temsilcisi (AI) modundayken başka bir menü aksiyonu → AI modundan çık
    if conversation.get("state") == STATE_AI_ACTIVE:
        await update_conversation_context(conversation["_id"], {}, state=STATE_GREETING)
    if payload == PB_BOOK:
        return await _send_book(business, conversation, sender_id)
    if payload == PB_SERVICES:
        return await _send_services(business, sender_id)
    if payload == PB_SERVICES_ALL:
        return await _send_services_all(business, sender_id)
    if payload == PB_INFO:
        return await _send_info(business, sender_id)
    if payload == PB_APPTS:
        return await _send_appointment_info(business, sender_id)
    if payload == PB_MENU:
        return await _send_main_menu(business, conversation, sender_id, force=True)
    if payload.startswith(PB_CAT_PREFIX):
        category = payload[len(PB_CAT_PREFIX):]
        return await _send_services_by_category(business, sender_id, category)
    log.info("Bilinmeyen IG payload: %s — ana menü gönderiliyor", payload)
    return await _send_main_menu(business, conversation, sender_id, force=True)


async def _send_main_menu(
    business: dict, conversation: dict, sender_id: str, force: bool = False,
) -> list[str]:
    if not force and _menu_recently_sent(conversation):
        log.info("IG ana menü debounce — atlandı (conv=%s)", conversation["_id"])
        return []

    name = business.get("name") or "Biz"
    text = f"Merhaba, {name} olarak nasıl yardımcı olabiliriz?"
    options = [
        {"title": "Randevu Al",         "payload": PB_BOOK},
        {"title": "Hizmetler",          "payload": PB_SERVICES},
        {"title": "Bilgi Al",           "payload": PB_INFO},
        {"title": "Müşteri Temsilcisi", "payload": PB_HUMAN},
    ]
    await send_quick_replies(business, sender_id, text, options)
    await update_conversation_context(
        conversation["_id"],
        {"ig_last_menu_at": datetime.now(timezone.utc)},
    )
    return [text]


async def _send_book(
    business: dict, conversation: dict, sender_id: str,
) -> list[str]:
    contact = business.get("contact") or {}
    booking_url = contact.get("booking_url")

    if not booking_url:
        phone = contact.get("phone") or "—"
        msg = (
            "Online randevu sistemi şu an aktif değil. "
            f"Randevu için bizi arayabilirsiniz: {phone}"
        )
        await send_text(business, sender_id, msg)
        return [msg]

    target_url = _booking_url(booking_url)
    body = (
        "Randevunuzu sitemiz üzerinden kolayca alabilirsiniz.\n"
        "Aşağıdaki butona tıklayarak birkaç adımda tamamlanıyor."
    )
    buttons = [
        url_button("Randevu Sayfası", target_url),
        postback_button("Geri Dön", PB_MENU),
    ]
    await send_button_template(business, sender_id, body, buttons)
    return [body + f" ({target_url})"]


async def _send_services(business: dict, sender_id: str) -> list[str]:
    services = await list_active_services(business["_id"])

    if not services:
        msg = "Hizmet listemiz henüz hazır değil. Detay için bizi arayabilirsiniz."
        await send_text(business, sender_id, msg)
        return [msg]

    categories = _service_categories(services)
    listing = _build_services_listing(services)

    # İdeal akış: tüm hizmetleri tek seferde göster (gerekirse birden çok mesaj).
    # Tek kategori varsa ya da liste makul boyuttaysa hepsini doğrudan listele;
    # böylece müşteri sürekli "geri dön / başka kategori seç" yapmak zorunda kalmaz.
    if len(categories) <= 1 or len(listing.encode("utf-8")) <= SERVICES_INLINE_MAX_BYTES:
        return await _send_services_all(business, sender_id, services)

    # Fallback: hizmet sayısı çok fazla → tek dökümde mesaj yağmuru olmasın diye
    # kategori seçim menüsü sun, ama yine de "Tümünü Gör" seçeneği bırak.
    text = "Hizmetlerimiz oldukça geniş. Hangi kategoriyi görmek istersiniz?"
    options = [
        {"title": truncate(cat, 20), "payload": PB_CAT_PREFIX + cat}
        for cat in categories
    ]
    options.append({"title": "Tümünü Gör", "payload": PB_SERVICES_ALL})
    options.append({"title": "Ana Menü", "payload": PB_MENU})
    await send_quick_replies(business, sender_id, text, options)
    return [text]


async def _send_services_all(
    business: dict, sender_id: str, services: list[dict] | None = None,
) -> list[str]:
    """Tüm hizmetleri kategoriye göre gruplayıp tek dökümde gösterir.

    Metin 1000 byte'ı aşarsa `send_text` otomatik olarak birden çok mesaja böler;
    böylece liste kısaltılmadan eksiksiz iletilir. Ardından kısa bir aksiyon
    mesajı (randevu butonu / telefon) gönderilir.
    """
    if services is None:
        services = await list_active_services(business["_id"])

    if not services:
        msg = "Hizmet listemiz henüz hazır değil. Detay için bizi arayabilirsiniz."
        await send_text(business, sender_id, msg)
        return [msg]

    listing = _build_services_listing(services)
    await send_text(business, sender_id, listing)  # uzun ise otomatik bölünür

    contact = business.get("contact") or {}
    booking_url = contact.get("booking_url")
    if booking_url:
        cta = "Randevunuzu hemen oluşturabilirsiniz."
        buttons = [
            url_button("Randevu Al", _booking_url(booking_url)),
            postback_button("Ana Menü", PB_MENU),
        ]
        await send_button_template(business, sender_id, cta, buttons)
        return [listing, cta]

    phone = contact.get("phone") or "—"
    cta = f"Randevu almak için bizi arayabilirsiniz: {phone}"
    await send_text(business, sender_id, cta)
    return [listing, cta]


async def _send_services_by_category(
    business: dict, sender_id: str, category: str,
) -> list[str]:
    all_services = await list_active_services(business["_id"])
    services = [s for s in all_services if (s.get("category") or "").strip() == category]
    booking_url = (business.get("contact") or {}).get("booking_url")

    if not services:
        msg = f"{category} kategorisinde henüz hizmet eklenmemiş."
        await send_text(business, sender_id, msg)
        return [msg]

    lines: list[str] = [category, ""]
    for s in services:
        price_str = format_price(s.get("price"), s.get("price_max"))
        lines.append(f"• {s['name']} — {s['duration_minutes']} dk — {price_str}")

    if booking_url:
        body = _fit_lines(lines, BTN_TEMPLATE_TEXT_MAX)
        buttons = [
            url_button("Randevu Al", _booking_url(booking_url)),
            postback_button("Kategoriler", PB_SERVICES),
            postback_button("Ana Menü", PB_MENU),
        ]
    else:
        phone = (business.get("contact") or {}).get("phone") or "—"
        phone_suffix = f"\n\nRandevu için: {phone}"
        body = _fit_lines(lines, BTN_TEMPLATE_TEXT_MAX - len(phone_suffix)) + phone_suffix
        buttons = [
            postback_button("Kategoriler", PB_SERVICES),
            postback_button("Ana Menü", PB_MENU),
        ]

    await send_button_template(business, sender_id, body, buttons)
    return [body]


async def _send_appointment_info(business: dict, sender_id: str) -> list[str]:
    contact = business.get("contact") or {}
    booking_url = contact.get("booking_url")

    if booking_url:
        body = "Mevcut randevularınızı görüntülemek veya iptal etmek için sitemize girebilirsiniz."
        buttons = [
            url_button("Randevularım", _booking_url(booking_url)),
            postback_button("Geri Dön", PB_MENU),
        ]
        await send_button_template(business, sender_id, body, buttons)
        return [body]

    phone = contact.get("phone")
    if phone:
        msg = "Randevularınız için lütfen bizi arayın."
        await send_text(business, sender_id, msg)
        await send_text(business, sender_id, phone)
        return [msg, phone]

    msg = "Randevu bilgileriniz için lütfen bizi arayın ya da mağazamıza uğrayın."
    await send_text(business, sender_id, msg)
    return [msg]


async def _send_info(business: dict, sender_id: str) -> list[str]:
    contact = business.get("contact") or {}

    parts: list[str] = [_format_working_hours(business)]
    address = contact.get("address")
    if address:
        parts.append(f"\nAdres: {address}")
    body = "\n".join(parts)

    buttons: list[dict] = []
    maps_url = _maps_url(business)
    if maps_url:
        buttons.append(url_button("Haritada Aç", maps_url))
    buttons.append(postback_button("Geri Dön", PB_MENU))

    await send_button_template(business, sender_id, body, buttons)
    sent = [body]

    # Telefonu ayrı bir metin olarak gönder: Instagram numarayı dokunulabilir
    # (ara) bağlantıya çevirir; şablon metni içinde gömülüyken bu olmuyor.
    phone = contact.get("phone")
    if phone:
        await send_text(business, sender_id, phone)
        sent.append(phone)
    return sent


async def _enter_customer_service(
    business: dict, conversation: dict, sender_id: str,
) -> list[str]:
    """'Müşteri Temsilcisi' butonu / serbest 'canlı destek' talebi.

    AI açıksa AI sohbet modunu başlatır (state=ai_active) ve karşılama gönderir;
    sonraki serbest metinleri orchestrator Groq'a yönlendirir. AI kapalıysa eski
    davranışa düşer ve gerçek personele (telefon) yönlendirir.
    """
    if ai.is_enabled():
        ai_cfg = business.get("ai_settings") or {}
        phone = (business.get("contact") or {}).get("phone")
        # Meta politikası: otomatik deneyim, sohbetin başında ifşa edilmeli.
        # AI ile randevu OLUŞTURULMADIĞI için karşılamada randevu/gün sorusu yok;
        # personele geçiş butonla değil, telefon numarasıyla yönlendirilir.
        # İşletme özel disclosure girdiyse (ai_disclosure) onu kullanırız;
        # ai_disclosure="" ile tamamen kapatılabilir.
        if phone:
            default_disclosure = (
                "Otomatik asistanınızla görüşüyorsunuz; personele ulaşmak için "
                "aşağıdaki numarayı arayabilirsiniz."
            )
        else:
            default_disclosure = "Otomatik asistanınızla görüşüyorsunuz."
        disclosure = ai_cfg.get("ai_disclosure", default_disclosure)

        custom = ai_cfg.get("welcome_message")
        base = custom or (
            f"Merhaba! Ben {business.get('name', 'işletmemiz')} otomatik "
            "asistanıyım. Size nasıl yardımcı olabilirim?"
        )
        welcome = f"{base}\n\n{disclosure}" if disclosure else base

        await update_conversation_context(conversation["_id"], {}, state=STATE_AI_ACTIVE)
        await send_text(business, sender_id, welcome)
        sent = [welcome]
        # Telefonu ayrı metin olarak gönder → dokunulabilir (ara) bağlantı olur.
        if phone:
            await send_text(business, sender_id, phone)
            sent.append(phone)
        return sent

    return await _send_human_handoff(business, conversation, sender_id)


async def _send_human_handoff(
    business: dict, conversation: dict, sender_id: str,
) -> list[str]:
    await update_conversation_context(
        conversation["_id"], {}, state=STATE_HUMAN_HANDOFF,
    )
    await record_escalation(
        business["_id"], conversation["_id"],
        conversation.get("customer_id"), "customer_requested",
        conversation.get("channel", "instagram"),
    )
    log.info("[handoff] conv=%s — personele aktarıldı (telefon yönlendirme)",
             conversation["_id"])
    contact = business.get("contact") or {}
    phone = contact.get("phone")

    if phone:
        msg1 = "Personelimizle doğrudan görüşmek için aşağıdaki numarayı arayabilirsiniz."
        await send_text(business, sender_id, msg1)
        await send_text(business, sender_id, phone)
        return [msg1, phone]

    msg = "Personelimizle görüşmek için lütfen mağazamızı ziyaret edin ya da sosyal medya üzerinden yazın."
    await send_text(business, sender_id, msg)
    return [msg]


# ---------- Yardımcı fonksiyonlar ----------

def _service_categories(services: list[dict]) -> list[str]:
    """Hizmetlerdeki kategorileri ekleniş sırasını koruyarak (tekrarsız) döndürür."""
    categories: list[str] = []
    seen: set[str] = set()
    for s in services:
        cat = (s.get("category") or "").strip()
        if cat and cat not in seen:
            categories.append(cat)
            seen.add(cat)
    return categories


def _build_services_listing(services: list[dict]) -> str:
    """Tüm hizmetleri kategoriye göre gruplayıp tek bir metin halinde döndürür.

    Kesme/budama yapmaz; çağıran taraf `send_text` ile gönderir ve metin
    1000 byte'ı aşarsa otomatik olarak birden çok mesaja bölünür.
    """
    grouped: dict[str, list[dict]] = {}
    order: list[str] = []
    for s in services:
        cat = (s.get("category") or "").strip() or "Diğer"
        if cat not in grouped:
            grouped[cat] = []
            order.append(cat)
        grouped[cat].append(s)

    multi = len(order) > 1
    lines: list[str] = ["Hizmetlerimiz"]
    for cat in order:
        if multi:
            lines.append("")
            lines.append(f"▪ {cat}")
        for s in grouped[cat]:
            price_str = format_price(s.get("price"), s.get("price_max"))
            lines.append(f"• {s['name']} — {s['duration_minutes']} dk — {price_str}")
    return "\n".join(lines)


def _fit_lines(lines: list[str], limit: int) -> str:
    """Satır listesini karakter limitine sığdırır; taşarsa son satırları atar."""
    result: list[str] = []
    for line in lines:
        candidate = "\n".join(result + [line])
        if len(candidate) > limit - 15:
            result.append("...")
            break
        result.append(line)
    return "\n".join(result)


def _booking_url(base_url: str, service: dict | None = None) -> str:
    sep = "&" if "?" in base_url else "?"
    params = ["src=ig"]
    if service is not None:
        params.append(f"service={service['_id']}")
    return f"{base_url}{sep}{'&'.join(params)}"


def _maps_url(business: dict) -> str | None:
    contact = business.get("contact") or {}
    loc = contact.get("location") or {}
    coords = loc.get("coordinates") or []
    if len(coords) == 2:
        lon, lat = coords[0], coords[1]
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    address = contact.get("address")
    if address:
        return f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}"
    return None


def _format_working_hours(business: dict) -> str:
    wh = business.get("working_hours") or []
    by_day = {w["day"]: w for w in wh}
    lines = ["Çalışma Saatlerimiz"]
    for d in WEEKDAY_NAMES:
        entry = by_day.get(d)
        label = WEEKDAY_TR[d]
        if not entry or entry.get("closed"):
            lines.append(f"• {label}: Kapalı")
        else:
            lines.append(
                f"• {label}: {entry.get('open', '?')} – {entry.get('close', '?')}"
            )

    tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
    today = datetime.now(tz).date()
    specials = []
    for sd in business.get("special_days") or []:
        d_str = sd.get("date")
        if isinstance(d_str, datetime):
            d_str = d_str.date().isoformat()
        elif hasattr(d_str, "isoformat"):
            d_str = d_str.isoformat()
        if not isinstance(d_str, str):
            continue
        try:
            d = datetime.fromisoformat(d_str).date()
        except Exception:
            continue
        if d < today or (d - today).days > 30:
            continue
        reason = (sd.get("reason") or "").strip()
        suffix = f" ({reason})" if reason else ""
        if sd.get("closed"):
            specials.append(f"• {d.strftime('%d.%m')}: Kapalı{suffix}")
        elif sd.get("open") and sd.get("close"):
            specials.append(
                f"• {d.strftime('%d.%m')}: {sd['open']} – {sd['close']}{suffix}"
            )
    if specials:
        lines.append("")
        lines.append("Özel günler:")
        lines.extend(specials)
    return "\n".join(lines)


def _menu_recently_sent(conversation: dict) -> bool:
    last = (conversation.get("context") or {}).get("ig_last_menu_at")
    if not isinstance(last, datetime):
        return False
    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)
    delta = (datetime.now(timezone.utc) - last).total_seconds()
    return delta < MENU_DEBOUNCE_SECONDS


__all__ = [
    "handle_event",
    "PB_MENU", "PB_BOOK", "PB_SERVICES", "PB_SERVICES_ALL", "PB_INFO", "PB_HUMAN",
    "PB_APPTS", "PB_CAT_PREFIX",
    "STATE_AI_ACTIVE", "STATE_HUMAN_HANDOFF",
    "RX_BOOK",
]
