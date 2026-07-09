from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from bson import ObjectId

from app.channels.whatsapp.flow_crypto import decrypt_request, encrypt_response
from app.channels.whatsapp.flow_sender import (
    get_flow_private_key,
    parse_flow_token,
)
from app.core import booking
from app.core.format import money_str as _money_str
from app.core.availability import (
    WEEKDAY_NAMES,
    compute_available_slots,
    is_in_time_off,
    is_special_closure,
    windows_for_day,
)
from app.core.config import get_settings
from app.core.db import (
    find_business_by_id,
    find_business_by_slug,
    get_db,
    try_oid,
)
from app.core.format import truncate as _truncate

log = logging.getLogger(__name__)

DAY_LABELS_TR = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
MONTH_TR = ["", "Oca", "Şub", "Mar", "Nis", "May", "Haz",
            "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
DAYS_TO_SCAN_MAX = 90      # business.ai_settings.max_advance_days üst sınırı
MAX_DROPDOWN_ROWS = 200
MAX_VISIBLE_ROWS = 20
DEFAULT_SLOT_STEP_MIN = 30
NOTES_MAX_CHARS = 200


# ---------- Endpoint istek işleyici ----------

async def handle_endpoint_request(body: dict) -> tuple[int, str | dict]:
    settings = get_settings()
    pem = get_flow_private_key()
    if not pem:
        log.error("Flow private key ayarlı değil; endpoint kullanılamaz")
        return 500, {"error": "private_key_not_configured"}

    try:
        decrypted = decrypt_request(
            body,
            private_key_pem=pem,
            private_key_passphrase=settings.wa_flow_private_key_passphrase,
        )
    except Exception:
        log.exception("Flow request decrypt başarısız — 421 dönülüyor")
        return 421, {"error": "decryption_failed"}

    payload = decrypted.payload
    action = payload.get("action")
    log.info("Flow endpoint action=%s screen=%s", action, payload.get("screen"))

    if action == "ping":
        return 200, encrypt_response({"data": {"status": "active"}},
                                     decrypted.aes_key, decrypted.iv)

    if isinstance(payload.get("data"), dict) and payload["data"].get("error"):
        log.warning("Flow client error notification: %s", payload["data"])
        return 200, encrypt_response({"data": {"acknowledged": True}},
                                     decrypted.aes_key, decrypted.iv)

    flow_token = payload.get("flow_token") or ""
    if flow_token.startswith("flows-builder-"):
        s = get_settings()
        slug = s.wa_flow_preview_business_slug or "berber_mehmet_kutahya"
        business = await find_business_by_slug(slug)
        if not business:
            log.warning("Flow preview için business bulunamadı: %s", slug)
            return 427, {"error_msg": "Preview test işletmesi bulunamadı."}
        conv_oid = ObjectId()
        log.info("Flow Builder preview modu: business=%s", slug)
    else:
        parsed = parse_flow_token(flow_token)
        if not parsed:
            log.warning("Geçersiz flow_token; 427 dönülüyor (token=%r)", flow_token)
            return 427, {"error_msg": "Bu randevu oturumu artık geçerli değil, lütfen baştan deneyin."}
        business_oid, conv_oid = parsed
        business = await find_business_by_id(business_oid)
        if not business:
            log.warning("Flow business bulunamadı: %s", business_oid)
            return 427, {"error_msg": "İşletme bilgisi bulunamadı."}

    response_obj = await _route(business, conv_oid, payload)
    return 200, encrypt_response(response_obj, decrypted.aes_key, decrypted.iv)


async def _route(business: dict, conv_oid: ObjectId, payload: dict) -> dict:
    action = payload.get("action")
    screen = payload.get("screen")
    data = payload.get("data") or {}
    for k in ("service_id", "staff_id", "day", "time"):
        v = data.get(k)
        if isinstance(v, list):
            data[k] = v[0] if v else ""
    flow_token = payload.get("flow_token") or ""

    if action == "data_exchange":
        if screen == "AD_SOYAD":
            return await _build_service_screen(business, data)
        if screen == "SERVICE":
            return await _build_staff_screen(business, data)
        if screen == "STAFF":
            return await _build_day_screen(business, data)
        if screen == "DAY":
            return await _build_time_screen(business, data)
        if screen == "TIME":
            return await _build_confirm_screen(business, data)
        if screen == "CONFIRM":
            return await _confirm_complete(business, conv_oid, data, flow_token)

    if action == "BACK":
        return await _refresh_screen(business, screen, data)

    log.warning("Bilinmeyen Flow action: %s screen=%s", action, screen)
    return _err_to_screen(screen or "AD_SOYAD", "İstek anlaşılamadı.")


async def _build_service_screen(business: dict, data: dict) -> dict:
    db = get_db()
    cursor = db.services.find(
        {"business_id": business["_id"], "is_active": True}
    )
    services_raw = [s async for s in cursor]
    log.info("SERVICE build: business=%s active_services=%d",
             business.get("business_id"), len(services_raw))
    services = []
    for s in services_raw[:MAX_DROPDOWN_ROWS]:
        price = _money_str(s.get("price"))
        price_max = _money_str(s.get("price_max"))
        desc = f"{s['duration_minutes']} dk"
        if price:
            price_label = f"{price}–{price_max}" if price_max else price
            desc += f" · {price_label}₺"
        services.append({
            "id": str(s["_id"]),
            "title": _truncate(s["name"], 30),
            "description": _truncate(desc, 300),
        })

    if not services:
        return _err_to_screen("AD_SOYAD", "Şu an aktif hizmet bulunmuyor.")

    return {
        "screen": "SERVICE",
        "data": {
            "first_name": (data.get("first_name") or "").strip(),
            "last_name": (data.get("last_name") or "").strip(),
            "services": services,
        },
    }


async def _build_staff_screen(business: dict, data: dict) -> dict:
    db = get_db()
    sid = try_oid(data.get("service_id"))
    if not sid:
        return _err_to_screen("SERVICE", "Hizmet seçimi anlaşılamadı.")
    service = await db.services.find_one(
        {"_id": sid, "business_id": business["_id"]}
    )
    if not service:
        return _err_to_screen("SERVICE", "Hizmet bulunamadı.")

    cursor = db.staff.find({
        "business_id": business["_id"],
        "is_active": True,
        "service_ids": sid,
    })
    staff_list = [s async for s in cursor]
    if not staff_list:
        return _err_to_screen("SERVICE", "Bu hizmeti verecek personel yok.")

    if len(staff_list) == 1:
        only = staff_list[0]
        return await _build_day_screen(business, {
            **data,
            "service_id": str(sid),
            "service_name": service["name"],
            "staff_id":   str(only["_id"]),
            "staff_name": only["name"],
        })

    options: list[dict] = [{"id": "any", "title": "Fark etmez"}]
    for st in staff_list[:MAX_VISIBLE_ROWS - 1]:
        options.append({
            "id": str(st["_id"]),
            "title": _truncate(st["name"], 30),
        })

    return {
        "screen": "STAFF",
        "data": {
            "first_name": data.get("first_name", ""),
            "last_name":  data.get("last_name", ""),
            "service_id": str(sid),
            "service_name": service["name"],
            "staff_options": options,
        },
    }


async def _build_day_screen(business: dict, data: dict) -> dict:
    db = get_db()
    sid = try_oid(data.get("service_id"))
    if not sid:
        return _err_to_screen("SERVICE", "Hizmet seçimi anlaşılamadı.")
    service = await db.services.find_one(
        {"_id": sid, "business_id": business["_id"]}
    )
    if not service:
        return _err_to_screen("SERVICE", "Hizmet bulunamadı.")

    raw_staff = data.get("staff_id") or "any"
    staff_list, staff_name = await _resolve_staff_list(
        db, business, service, raw_staff
    )
    if not staff_list:
        return _err_to_screen("STAFF", "Personel bulunamadı.")

    tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
    today = datetime.now(tz).date()
    ai = business.get("ai_settings") or {}
    days_to_scan = min(int(ai.get("max_advance_days", 60)), DAYS_TO_SCAN_MAX)
    days = []
    for i in range(days_to_scan):
        d = today + timedelta(days=i)
        if not await _day_has_any_slot(db, business, service, staff_list, d):
            continue
        days.append({"id": d.isoformat(),
                     "title": _truncate(_format_day_label(d), 30)})
        if len(days) >= MAX_VISIBLE_ROWS:
            break

    if not days:
        return _err_to_screen(
            "STAFF",
            f"Bu personel için {days_to_scan} gün içinde müsait gün yok.",
        )

    return {
        "screen": "DAY",
        "data": {
            "first_name": data.get("first_name", ""),
            "last_name":  data.get("last_name", ""),
            "service_id": str(sid),
            "service_name": service["name"],
            "staff_id":   raw_staff,
            "staff_name": staff_name,
            "caption":    f"{service['name']} · {staff_name}",
            "days": days,
        },
    }


async def _build_time_screen(business: dict, data: dict) -> dict:
    db = get_db()
    sid = try_oid(data.get("service_id"))
    day_iso = data.get("day") or ""
    try:
        target = date.fromisoformat(day_iso)
    except Exception:
        return _err_to_screen("DAY", "Gün anlaşılamadı.")

    service = await db.services.find_one(
        {"_id": sid, "business_id": business["_id"]}
    ) if sid else None
    if not service:
        return _err_to_screen("SERVICE", "Hizmet bulunamadı.")

    raw_staff = data.get("staff_id") or "any"
    staff_list, staff_name = await _resolve_staff_list(
        db, business, service, raw_staff
    )
    if not staff_list:
        return _err_to_screen("STAFF", "Personel bulunamadı.")

    tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
    ai = business.get("ai_settings") or {}
    step = max(5, int(ai.get("online_slot_step_minutes", DEFAULT_SLOT_STEP_MIN)))

    times_set: set[str] = set()
    for st in staff_list:
        if is_in_time_off(st, target):
            continue
        slots = await compute_available_slots(
            db, business, service, st, target, step_minutes=step,
        )
        for s in slots:
            local = s.astimezone(tz)
            total_min = local.hour * 60 + local.minute
            if total_min % step != 0:
                continue
            times_set.add(f"{local.hour:02d}:{local.minute:02d}")

    times_list = sorted(times_set)[:MAX_VISIBLE_ROWS]
    if not times_list:
        return _err_to_screen("DAY", "Bu gün için saat kalmamış.")

    times = [{"id": t, "title": t} for t in times_list]
    day_label = _format_day_label(target)
    return {
        "screen": "TIME",
        "data": {
            "first_name": data.get("first_name", ""),
            "last_name":  data.get("last_name", ""),
            "service_id": str(sid),
            "service_name": service["name"],
            "staff_id":   raw_staff,
            "staff_name": staff_name,
            "day": day_iso,
            "day_label": day_label,
            "caption":   f"{service['name']} · {staff_name} · {day_label}",
            "times": times,
        },
    }


async def _build_confirm_screen(business: dict, data: dict) -> dict:
    db = get_db()
    sid = try_oid(data.get("service_id"))
    service = await db.services.find_one(
        {"_id": sid, "business_id": business["_id"]}
    ) if sid else None
    if not service:
        return _err_to_screen("SERVICE", "Hizmet bulunamadı.")

    raw_staff = data.get("staff_id") or "any"
    staff_name = data.get("staff_name") or "Fark etmez"
    if raw_staff != "any":
        st_oid = try_oid(raw_staff)
        if st_oid:
            st = await db.staff.find_one(
                {"_id": st_oid, "business_id": business["_id"]}
            )
            if st:
                staff_name = st["name"]

    day_iso = data.get("day") or ""
    time_str = data.get("time") or ""
    duration = int(service.get("duration_minutes") or 0)
    try:
        target = date.fromisoformat(day_iso)
        day_label = _format_day_label(target)
        hh, mm = (int(p) for p in time_str.split(":"))
        end_local = datetime(target.year, target.month, target.day, hh, mm) \
            + timedelta(minutes=duration)
        end_label = f"{end_local.hour:02d}:{end_local.minute:02d}"
    except Exception:
        day_label = day_iso
        end_label = ""

    full_name = f"{data.get('first_name','').strip()} {data.get('last_name','').strip()}".strip()
    time_range = f"{time_str} – {end_label}" if end_label else time_str
    return {
        "screen": "CONFIRM",
        "data": {
            "first_name":   data.get("first_name", ""),
            "last_name":    data.get("last_name", ""),
            "full_name":    full_name,
            "service_id":   str(sid),
            "service_name": service["name"],
            "staff_id":     raw_staff,
            "staff_name":   staff_name,
            "day":          day_iso,
            "day_label":    day_label,
            "time":         time_str,
            "end_time":     end_label,
            "time_range":   time_range,
            "duration_minutes": duration,
            "notes":        (data.get("notes") or "")[:NOTES_MAX_CHARS],
        },
    }


async def _refresh_screen(business: dict, screen: str | None, data: dict) -> dict:
    if screen == "SERVICE":
        return await _build_service_screen(business, data)
    if screen == "STAFF":
        return await _build_staff_screen(business, data)
    if screen == "DAY":
        return await _build_day_screen(business, data)
    if screen == "TIME":
        return await _build_time_screen(business, data)
    if screen == "CONFIRM":
        return await _build_confirm_screen(business, data)
    return {"screen": "AD_SOYAD", "data": {}}


async def _resolve_staff_list(
    db, business: dict, service: dict, raw_staff: str,
) -> tuple[list[dict], str]:
    if raw_staff == "any":
        cursor = db.staff.find({
            "business_id": business["_id"],
            "is_active": True,
            "service_ids": service["_id"],
        })
        staff_list = [s async for s in cursor]
        return staff_list, "Fark etmez"
    st_oid = try_oid(raw_staff)
    if not st_oid:
        return [], ""
    st = await db.staff.find_one(
        {"_id": st_oid, "business_id": business["_id"], "is_active": True}
    )
    if not st or service["_id"] not in (st.get("service_ids") or []):
        return [], ""
    return [st], st["name"]


async def _confirm_complete(
    business: dict, conv_oid: ObjectId, data: dict, flow_token: str,
) -> dict:
    db = get_db()

    first_name = (data.get("first_name") or "").strip()
    last_name  = (data.get("last_name") or "").strip()
    full_name  = f"{first_name} {last_name}".strip()
    sid        = try_oid(data.get("service_id"))
    day_iso    = data.get("day") or ""
    time_str   = data.get("time") or ""
    raw_staff  = data.get("staff_id") or "any"
    notes_raw  = (data.get("notes") or "").strip()
    notes      = notes_raw[:NOTES_MAX_CHARS] or None

    if not (sid and day_iso and time_str and full_name):
        return _confirm_error(data, "Randevu bilgileri eksik, lütfen baştan deneyin.")

    service = await db.services.find_one(
        {"_id": sid, "business_id": business["_id"]}
    )
    if not service:
        return _confirm_error(data, "Seçilen hizmet bulunamadı.")

    try:
        target = date.fromisoformat(day_iso)
        hh, mm = (int(p) for p in time_str.split(":"))
    except Exception:
        return _confirm_error(data, "Tarih/saat anlaşılamadı.")

    if raw_staff == "any":
        candidates = await booking.find_staff_available_at(
            db, business, service, target, hh, mm
        )
        if not candidates:
            return _confirm_error(
                data, "Bu saate uygun personel kalmadı, lütfen başka saat seçin.")
        staff = candidates[0]
    else:
        st_oid = try_oid(raw_staff)
        staff = await db.staff.find_one(
            {"_id": st_oid, "business_id": business["_id"]}
        ) if st_oid else None
        if not staff:
            return _confirm_error(data, "Seçilen personel bulunamadı.")

    if flow_token.startswith("flows-builder-"):
        log.info("Flow Builder preview CONFIRM: dry-run (mongo'ya yazılmaz)")
        return {
            "screen": "SUCCESS",
            "data": {
                "extension_message_response": {
                    "params": {
                        "flow_token": flow_token,
                        "preview": True,
                        "service_name": service["name"],
                        "staff_name": staff["name"],
                        "day": day_iso,
                        "time": time_str,
                    },
                },
            },
        }

    conversation = await db.conversations.find_one({"_id": conv_oid})
    if not conversation:
        return _confirm_error(data, "Oturum bulunamadı, lütfen baştan deneyin.")
    customer = await db.customers.find_one({"_id": conversation["customer_id"]})
    if not customer:
        return _confirm_error(data, "Müşteri kaydı bulunamadı.")

    if customer.get("name") != full_name:
        await db.customers.update_one(
            {"_id": customer["_id"]}, {"$set": {"name": full_name}}
        )
        customer["name"] = full_name

    result = await booking.create_appointment(
        db, business, customer, conversation, service, staff,
        start_local=f"{day_iso} {time_str}",
        notes=notes,
        created_by="whatsapp_flow",
    )
    if result.get("error"):
        if result["error"] == "slot_taken":
            return _confirm_error(
                data,
                "Bu saat az önce dolmuş, lütfen başka saat seçin.")
        log.warning("create_appointment hata: %s", result)
        return _confirm_error(
            data, "Randevu oluşturulamadı, lütfen tekrar deneyin.")

    await db.conversations.update_one(
        {"_id": conv_oid},
        {"$unset": {"context.flow_token": ""},
         "$set": {"state": "booked",
                  "context.booked_appointment_id": result["appointment_id"]}},
    )

    return {
        "screen": "SUCCESS",
        "data": {
            "extension_message_response": {
                "params": {
                    "flow_token": flow_token,
                    "appointment_id": result["appointment_id"],
                    "service_name": result["service_name"],
                    "staff_name": result["staff_name"],
                    "start_time_local": result["start_time_local"],
                    "duration_minutes": result["duration_minutes"],
                    "price": str(result.get("price") or ""),
                    "currency": result.get("currency", "TRY"),
                },
            },
        },
    }


def _confirm_error(data: dict, message: str) -> dict:
    first = (data.get("first_name") or "").strip()
    last = (data.get("last_name") or "").strip()
    end = data.get("end_time") or ""
    t = data.get("time") or ""
    return {
        "screen": "CONFIRM",
        "data": {
            "first_name":       data.get("first_name", ""),
            "last_name":        data.get("last_name", ""),
            "full_name":        f"{first} {last}".strip(),
            "service_id":       data.get("service_id", ""),
            "service_name":     data.get("service_name", ""),
            "staff_id":         data.get("staff_id", "any"),
            "staff_name":       data.get("staff_name", ""),
            "day":              data.get("day", ""),
            "day_label":        data.get("day_label", data.get("day", "")),
            "time":             t,
            "end_time":         end,
            "time_range":       f"{t} – {end}" if end else t,
            "duration_minutes": data.get("duration_minutes", 0),
            "notes":            (data.get("notes") or "")[:NOTES_MAX_CHARS],
            "error_message":    message,
        },
    }


async def _day_has_any_slot(db, business, service, staff_list, d: date) -> bool:
    closure = is_special_closure(business, d)
    if closure and closure.get("closed"):
        return False
    biz_w = windows_for_day(business["working_hours"], WEEKDAY_NAMES[d.weekday()])
    if not biz_w and not (closure and closure.get("open") and closure.get("close")):
        return False
    for st in staff_list:
        if is_in_time_off(st, d):
            continue
        slots = await compute_available_slots(db, business, service, st, d)
        if slots:
            return True
    return False


def _err_to_screen(screen: str, message: str) -> dict:
    return {"screen": screen, "data": {"error_message": message}}


def _format_day_label(d: date) -> str:
    return f"{DAY_LABELS_TR[d.weekday()]} {d.day:02d} {MONTH_TR[d.month]}"
