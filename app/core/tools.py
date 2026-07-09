"""
AI tool seti. Her tool:
- OpenAI-uyumlu JSON schema (Ollama tool-use ile çalışır)
- Async Python implementasyonu
- Tüm sorgular `business_id` ile sınırlı (güvenlik: müşteri yanlış business'ı sorgulayamaz)
- Tarihler tools arasında ISO-8601 (lokal saat) string olarak konuşulur, DB'ye UTC yazılır

Her tool bir dict döner ve döndüğü değer modele "tool" rolüyle geri verilir.
"""

from __future__ import annotations

import inspect
import logging
import re
from datetime import date, datetime, timedelta, timezone
from typing import Iterable
from zoneinfo import ZoneInfo

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core import booking
from app.core.availability import WEEKDAY_NAMES, find_first_available_slots
from app.core.db import get_db, record_escalation, to_oid, try_oid
from app.core.format import WEEKDAY_TR, local_iso, money_str

log = logging.getLogger(__name__)


# ---------- Yardımcılar ----------

async def _resolve_service_oid(ctx: "ToolContext", value: str | ObjectId) -> ObjectId | None:
    """ObjectId hex ya da hizmet adı kabul eder. AI bazen 'saç kesimi' gibi ad geçiyor."""
    oid = try_oid(value)
    if oid:
        return oid
    if not isinstance(value, str) or not value.strip():
        return None
    doc = await ctx.db.services.find_one({
        "business_id": ctx.business["_id"],
        "name": {"$regex": f"^{re.escape(value.strip())}$", "$options": "i"},
        "is_active": True,
    }, {"_id": 1})
    return doc["_id"] if doc else None


async def _resolve_staff_oid(ctx: "ToolContext", value: str | ObjectId) -> ObjectId | None:
    oid = try_oid(value)
    if oid:
        return oid
    if not isinstance(value, str) or not value.strip():
        return None
    doc = await ctx.db.staff.find_one({
        "business_id": ctx.business["_id"],
        "name": {"$regex": f"^{re.escape(value.strip())}$", "$options": "i"},
        "is_active": True,
    }, {"_id": 1})
    return doc["_id"] if doc else None


# ---------- OpenAI/Ollama tool şemaları ----------
# Tool'lar arası birebir tekrar eden parametre açıklamaları (modelin tool
# seçimini yönlendirir; tek kaynak → tutarlı davranış).
_SERVICE_ID_DESC = (
    "list_services'tan dönen service_id (24 hane). "
    "Tam hizmet adı (örn. 'Saç Kesimi') de kabul edilir."
)
_STAFF_ID_DESC = (
    "list_staff'tan dönen staff_id (24 hane). "
    "Tam personel adı (örn. 'Mehmet Kaya') de kabul edilir."
)
_LOCAL_DATETIME_DESC = "YYYY-MM-DD HH:MM (lokal)"

TOOL_SCHEMAS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "get_business_info",
            "description": (
                "İşletmenin iletişim ve çalışma bilgilerini döner: adres, telefon, "
                "WhatsApp, e-posta, çalışma saatleri, yaklaşan özel günler "
                "(tatil/kısa mesai), online randevu sayfası (booking_url), harita ve "
                "sosyal medya. Adres, konum, telefon/WhatsApp/e-posta, 'açık mısınız', "
                "çalışma saati gibi iletişim/erişim sorularında kullan."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_services",
            "description": "İşletmenin sunduğu aktif hizmetleri listeler.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_staff",
            "description": (
                "Personeli listeler. Hizmet id verilirse sadece o hizmeti "
                "verebilen personelleri döner."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "service_id": {"type": "string", "description": _SERVICE_ID_DESC},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_available_slots",
            "description": (
                "Bir hizmet için uygun randevu saatlerini döner. "
                "staff_id verilmezse hizmeti verebilen tüm personeller arasından "
                "en yakın slotlar döner. start_date verilmezse bugün (lokal)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "service_id": {"type": "string", "description": _SERVICE_ID_DESC},
                    "staff_id": {"type": "string", "description": _STAFF_ID_DESC},
                    "start_date": {"type": "string", "description": "YYYY-MM-DD (lokal)"},
                    "days_to_scan": {"type": "integer", "minimum": 1, "maximum": 60},
                    "max_results": {"type": "integer", "minimum": 1, "maximum": 20},
                },
                "required": ["service_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_staff_available_at",
            "description": (
                "Belirli bir hizmet ve lokal başlangıç saati için, o saatte "
                "müsait olan personeli döner. Müşteri görseldeki yeşil bir "
                "saati seçtiğinde bu tool ile uygun ustaları listele."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "service_id": {"type": "string", "description": _SERVICE_ID_DESC},
                    "start_time": {"type": "string", "description": _LOCAL_DATETIME_DESC},
                },
                "required": ["service_id", "start_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_appointment",
            "description": (
                "Yeni randevu oluşturur. start_time lokal saat olmalı: 'YYYY-MM-DD HH:MM'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "service_id": {"type": "string", "description": _SERVICE_ID_DESC},
                    "staff_id": {"type": "string", "description": _STAFF_ID_DESC},
                    "start_time": {"type": "string", "description": _LOCAL_DATETIME_DESC},
                    "notes": {"type": "string"},
                },
                "required": ["service_id", "staff_id", "start_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_appointment",
            "description": "Müşterinin kendi randevusunu iptal eder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["appointment_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_appointments",
            "description": "Müşterinin yaklaşan randevularını listeler.",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_past": {"type": "boolean"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_customer_name",
            "description": "Müşterinin adı sistemde yoksa veya değiştirmek istiyorsa kayıt eder.",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": (
                "AI çözemediğinde sohbeti insan personele aktarır. Konuşma "
                "state'i 'human_handoff' olur ve müşteriye nazik bir kapanış mesajı "
                "verilmelidir."
            ),
            "parameters": {
                "type": "object",
                "properties": {"reason": {"type": "string"}},
                "required": ["reason"],
            },
        },
    },
]


# ---------- Tool implementasyonları ----------

class ToolContext:
    """Her sohbet turu için sabit context (business + customer + conversation)."""

    def __init__(self, business: dict, customer: dict, conversation: dict):
        self.business = business
        self.customer = customer
        self.conversation = conversation
        self.tz = business.get("timezone", "Europe/Istanbul")

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return get_db()


async def get_business_info(ctx: ToolContext) -> dict:
    business = ctx.business
    contact = business.get("contact") or {}

    by_day = {w["day"]: w for w in (business.get("working_hours") or [])}
    hours = []
    for d in WEEKDAY_NAMES:
        entry = by_day.get(d)
        if not entry or entry.get("closed"):
            hours.append({"day": WEEKDAY_TR[d], "closed": True})
        else:
            hours.append({
                "day": WEEKDAY_TR[d],
                "open": entry.get("open"),
                "close": entry.get("close"),
                "closed": False,
            })

    # Bugünden itibaren 30 gün içindeki özel günler
    today = datetime.now(ZoneInfo(ctx.tz)).date()
    specials = []
    for sd in business.get("special_days") or []:
        raw = sd.get("date")
        if isinstance(raw, datetime):
            raw = raw.date()
        elif isinstance(raw, str):
            try:
                raw = date.fromisoformat(raw)
            except ValueError:
                continue
        if not isinstance(raw, date):
            continue
        if raw < today or (raw - today).days > 30:
            continue
        specials.append({
            "date": raw.isoformat(),
            "closed": bool(sd.get("closed")),
            "open": sd.get("open"),
            "close": sd.get("close"),
            "reason": sd.get("reason"),
        })

    loc = contact.get("location") or {}
    coords = loc.get("coordinates") or []
    maps_url = None
    if len(coords) == 2:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={coords[1]},{coords[0]}"

    socials = business.get("socials") or {}
    return {
        "name": business.get("name"),
        "business_type": business.get("business_type"),
        "phone": contact.get("phone"),
        "whatsapp": contact.get("whatsapp_number"),
        "email": contact.get("email"),
        "address": contact.get("address"),
        "working_hours": hours,
        "special_days": specials,
        "booking_url": contact.get("booking_url"),
        "maps_url": maps_url,
        "instagram": socials.get("instagram"),
        "facebook": socials.get("facebook"),
        "website": socials.get("website"),
        "timezone": ctx.tz,
    }


async def list_services(ctx: ToolContext) -> dict:
    cursor = ctx.db.services.find(
        {"business_id": ctx.business["_id"], "is_active": True}
    )
    items = []
    async for s in cursor:
        items.append({
            "service_id": str(s["_id"]),
            "name": s["name"],
            "duration_minutes": s["duration_minutes"],
            "price": money_str(s["price"]),
            "currency": s.get("currency", "TRY"),
            "category": s.get("category"),
            "description": s.get("description"),
        })
    return {"services": items}


async def list_staff(ctx: ToolContext, service_id: str | None = None) -> dict:
    q: dict = {"business_id": ctx.business["_id"], "is_active": True}
    if service_id:
        sid = await _resolve_service_oid(ctx, service_id)
        if not sid:
            return {"error": "service_not_found", "value": service_id}
        q["service_ids"] = sid
    cursor = ctx.db.staff.find(q)
    items = []
    async for st in cursor:
        items.append({
            "staff_id": str(st["_id"]),
            "name": st["name"],
            "role": st.get("role"),
            "bio": st.get("bio"),
        })
    return {"staff": items}


async def list_available_slots(
    ctx: ToolContext,
    service_id: str,
    staff_id: str | None = None,
    start_date: str | None = None,
    days_to_scan: int = 14,
    max_results: int = 6,
) -> dict:
    sid = await _resolve_service_oid(ctx, service_id)
    if not sid:
        return {"error": "service_not_found", "value": service_id}
    service = await ctx.db.services.find_one(
        {"_id": sid, "business_id": ctx.business["_id"]}
    )
    if not service:
        return {"error": "service_not_found"}

    if start_date:
        try:
            start_d = date.fromisoformat(start_date)
        except ValueError:
            return {"error": "invalid_start_date"}
    else:
        start_d = datetime.now(ZoneInfo(ctx.tz)).date()

    if staff_id:
        st_id = await _resolve_staff_oid(ctx, staff_id)
        if not st_id:
            return {"error": "staff_not_found", "value": staff_id}
        staff_doc = await ctx.db.staff.find_one(
            {"_id": st_id, "business_id": ctx.business["_id"]}
        )
        if not staff_doc or sid not in staff_doc.get("service_ids", []):
            return {"error": "staff_cannot_perform_service"}
        candidates_by_staff = [staff_doc]
    else:
        cursor = ctx.db.staff.find({
            "business_id": ctx.business["_id"],
            "is_active": True,
            "service_ids": sid,
        })
        candidates_by_staff = [s async for s in cursor]
        if not candidates_by_staff:
            return {"error": "no_staff_for_service"}

    results: list[dict] = []
    for staff_doc in candidates_by_staff:
        slots = await find_first_available_slots(
            ctx.db, ctx.business, service, staff_doc,
            start_date=start_d, days_to_scan=days_to_scan,
            max_slots=max_results,
        )
        for s in slots:
            results.append({
                "start_time_local": local_iso(s, ctx.tz),
                "staff_id": str(staff_doc["_id"]),
                "staff_name": staff_doc["name"],
            })

    results.sort(key=lambda r: r["start_time_local"])
    return {
        "service_id": service_id,
        "service_name": service["name"],
        "duration_minutes": service["duration_minutes"],
        "slots": results[:max_results],
    }


async def list_staff_available_at(
    ctx: ToolContext, service_id: str, start_time: str
) -> dict:
    sid = await _resolve_service_oid(ctx, service_id)
    if not sid:
        return {"error": "service_not_found", "value": service_id}
    service = await ctx.db.services.find_one(
        {"_id": sid, "business_id": ctx.business["_id"]}
    )
    if not service:
        return {"error": "service_not_found"}

    try:
        local_dt = datetime.strptime(start_time.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        return {"error": "invalid_start_time"}

    staff_docs = await booking.find_staff_available_at(
        ctx.db, ctx.business, service,
        local_dt.date(), local_dt.hour, local_dt.minute,
    )
    available = [
        {"staff_id": str(st["_id"]), "name": st["name"], "role": st.get("role")}
        for st in staff_docs
    ]
    return {
        "service_name": service["name"],
        "start_time_local": start_time,
        "available": available,
    }


async def create_appointment(
    ctx: ToolContext,
    service_id: str,
    staff_id: str,
    start_time: str,
    notes: str | None = None,
) -> dict:
    if not ctx.customer.get("name"):
        return {"error": "customer_name_required",
                "message": "Önce müşterinin adını sor ve update_customer_name ile kaydet."}

    sid = await _resolve_service_oid(ctx, service_id)
    if not sid:
        return {"error": "service_not_found", "value": service_id}
    service = await ctx.db.services.find_one(
        {"_id": sid, "business_id": ctx.business["_id"]}
    )
    if not service:
        return {"error": "service_not_found"}

    st_id = await _resolve_staff_oid(ctx, staff_id)
    if not st_id:
        return {"error": "staff_not_found", "value": staff_id}
    staff = await ctx.db.staff.find_one(
        {"_id": st_id, "business_id": ctx.business["_id"]}
    )
    if not staff:
        return {"error": "staff_not_found"}

    result = await booking.create_appointment(
        ctx.db, ctx.business, ctx.customer, ctx.conversation,
        service, staff, start_time, notes=notes, created_by="ai",
    )
    if result.get("error") == "slot_taken":
        result["message"] = "Bu saat artık dolu. list_available_slots ile yeni saat öner."
    return result


async def cancel_appointment(
    ctx: ToolContext, appointment_id: str, reason: str | None = None
) -> dict:
    apt = await ctx.db.appointments.find_one({
        "_id": to_oid(appointment_id),
        "business_id": ctx.business["_id"],
        "customer_id": ctx.customer["_id"],
    })
    if not apt:
        return {"error": "appointment_not_found"}
    if apt["status"] in ("cancelled", "completed", "no_show"):
        return {"error": "already_finalized", "status": apt["status"]}

    ai = ctx.business.get("ai_settings") or {}
    window_min = int(ai.get("customer_cancel_window_minutes", 60))
    now = datetime.now(timezone.utc)
    deadline = apt["start_time"] - timedelta(minutes=window_min)
    if now > deadline:
        return {
            "error": "cancel_window_passed",
            "message": (
                f"İptal süresi geçti (randevudan en az {window_min} dk önce "
                "iptal edebilirsiniz). Lütfen bizi arayın."
            ),
            "deadline": deadline.isoformat(),
        }

    await ctx.db.appointments.update_one(
        {"_id": apt["_id"]},
        {"$set": {
            "status": "cancelled",
            "cancelled_reason": reason,
            "updated_at": now,
        }},
    )

    cancel_block_limit = int(ai.get("cancel_block_limit", 5))
    upd = await ctx.db.customers.find_one_and_update(
        {"_id": ctx.customer["_id"]},
        {"$inc": {"cancel_count": 1}},
        return_document=True,
        projection={"cancel_count": 1, "is_blocked": 1},
    )
    new_count = (upd or {}).get("cancel_count", 0)
    blocked_now = False
    if new_count >= cancel_block_limit and not (upd or {}).get("is_blocked"):
        await ctx.db.customers.update_one(
            {"_id": ctx.customer["_id"]},
            {"$set": {
                "is_blocked": True,
                "blocked_at": now,
                "blocked_reason": "cancel_limit",
            }},
        )
        blocked_now = True

    return {
        "appointment_id": appointment_id,
        "status": "cancelled",
        "cancel_count": new_count,
        "blocked": blocked_now,
    }


async def get_customer_appointments(
    ctx: ToolContext, include_past: bool = False
) -> dict:
    q: dict = {
        "business_id": ctx.business["_id"],
        "customer_id": ctx.customer["_id"],
    }
    if not include_past:
        q["start_time"] = {"$gte": datetime.now(timezone.utc)}
        q["status"] = {"$in": ["pending", "confirmed"]}

    cursor = ctx.db.appointments.find(q).sort("start_time", 1).limit(10)
    items = []
    async for a in cursor:
        items.append({
            "appointment_id": str(a["_id"]),
            "start_time_local": local_iso(a["start_time"], ctx.tz),
            "status": a["status"],
            "services": [s["name"] for s in a["services"]],
            "total_price": money_str(a["total_price"]),
        })
    return {"appointments": items}


async def update_customer_name(ctx: ToolContext, name: str) -> dict:
    name = name.strip()
    if not name:
        return {"error": "empty_name"}
    await ctx.db.customers.update_one(
        {"_id": ctx.customer["_id"]}, {"$set": {"name": name}}
    )
    ctx.customer["name"] = name
    return {"ok": True, "name": name}


async def escalate_to_human(ctx: ToolContext, reason: str) -> dict:
    await ctx.db.conversations.update_one(
        {"_id": ctx.conversation["_id"]},
        {"$set": {"state": "human_handoff",
                  "context.handoff_reason": reason}},
    )
    # Operasyon kuyruğuna yaz + uyarı logla (insan ajan giriş yolu açık kalsın).
    await record_escalation(
        ctx.business["_id"], ctx.conversation["_id"],
        ctx.customer.get("_id"), reason,
        ctx.conversation.get("channel", "instagram"),
    )
    log.warning("[handoff] biz=%s conv=%s sebep=%s — insana aktarıldı",
                ctx.business.get("business_id"), ctx.conversation["_id"], reason)
    phone = (ctx.business.get("contact") or {}).get("phone")
    return {"ok": True, "state": "human_handoff", "phone": phone}


# ---------- Dispatcher ----------

TOOL_REGISTRY = {
    "get_business_info": get_business_info,
    "list_services": list_services,
    "list_staff": list_staff,
    "list_available_slots": list_available_slots,
    "list_staff_available_at": list_staff_available_at,
    "create_appointment": create_appointment,
    "cancel_appointment": cancel_appointment,
    "get_customer_appointments": get_customer_appointments,
    "update_customer_name": update_customer_name,
    "escalate_to_human": escalate_to_human,
}


async def dispatch(ctx: ToolContext, name: str, arguments: dict) -> dict:
    fn = TOOL_REGISTRY.get(name)
    if fn is None:
        return {"error": "unknown_tool", "name": name}
    # Model bazen şemada olmayan argüman uydurur (ör. list_services'e service_id=None).
    # Bunları TypeError'la patlatıp bir tool turunu (ve Groq çağrısını) boşa harcamak
    # yerine, fonksiyonun gerçekten kabul ettiği parametrelere göre filtreleyip atıyoruz.
    args = arguments or {}
    params = inspect.signature(fn).parameters
    if not any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()):
        accepted = {k: v for k, v in args.items() if k in params}
        dropped = set(args) - set(accepted)
        if dropped:
            log.warning("Tool %s — bilinmeyen argüman(lar) atlandı: %s", name, dropped)
        args = accepted
    try:
        return await fn(ctx, **args)
    except TypeError as e:
        log.exception("Tool %s argümanları geçersiz", name)
        return {"error": "invalid_arguments", "detail": str(e)}
    except Exception as e:
        log.exception("Tool %s hata fırlattı", name)
        return {"error": "internal_error", "detail": str(e)}


# ---------- Tool setleri ----------
# Instagram "Müşteri Temsilcisi" modu: bilgi + müsaitlik odaklı (randevu web'de
# tamamlanır → booking_url). create/cancel_appointment ve get_customer_appointments
# bilinçli olarak dışarıda: bu kanalda randevu oluşturma/iptal/LİSTELEME yapılmaz;
# mevcut/geçmiş/yaklaşan randevu ve iptal için müşteri booking_url'e yönlendirilir
# (DM'de kimlik doğrulanamadığından randevu listelemek hem güvensiz hem yanıltıcı).
CUSTOMER_SERVICE_TOOL_NAMES = (
    "get_business_info",
    "list_services",
    "list_staff",
    "list_available_slots",
    "list_staff_available_at",
    "escalate_to_human",
)


def schemas_for(names: Iterable[str]) -> list[dict]:
    """Verilen tool adları için OpenAI/Groq şema alt kümesini döner."""
    wanted = set(names)
    return [s for s in TOOL_SCHEMAS if s["function"]["name"] in wanted]
