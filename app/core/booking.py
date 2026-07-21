from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from bson import ObjectId
from bson.decimal128 import Decimal128
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from app.core.availability import (
    WEEKDAY_NAMES,
    is_in_time_off,
    windows_for_day,
)
from app.core.format import local_iso, money_str

log = logging.getLogger(__name__)


def _guard_ids(
    business_id: ObjectId,
    staff_id: ObjectId,
    start_utc: datetime,
    end_utc: datetime,
) -> list[str]:
    cursor = start_utc.replace(second=0, microsecond=0)
    cursor -= timedelta(minutes=cursor.minute % 5)
    keys: list[str] = []
    while cursor < end_utc:
        keys.append(f"{business_id}:{staff_id}:{int(cursor.timestamp())}")
        cursor += timedelta(minutes=5)
    return keys


async def _reserve_guards(
    db: AsyncIOMotorDatabase,
    appointment_id: ObjectId,
    business_id: ObjectId,
    staff_id: ObjectId,
    start_utc: datetime,
    end_utc: datetime,
) -> list[str] | None:
    """Standalone MongoDB'de de eşzamanlı çakışmayı engelleyen dilim kilidi."""
    keys = _guard_ids(business_id, staff_id, start_utc, end_utc)
    inserted: list[str] = []
    try:
        for key in keys:
            current = await db.appointment_guards.find_one({"_id": key}, {"owner": 1})
            if current:
                if current.get("owner") == appointment_id:
                    continue
                raise DuplicateKeyError("slot reserved")
            await db.appointment_guards.insert_one({
                "_id": key,
                "owner": appointment_id,
                "business_id": business_id,
                "staff_id": staff_id,
                "created_at": datetime.now(timezone.utc),
            })
            inserted.append(key)
    except DuplicateKeyError:
        if inserted:
            await db.appointment_guards.delete_many(
                {"_id": {"$in": inserted}, "owner": appointment_id}
            )
        return None
    return keys


def _to_money_decimal128(v: Any) -> Decimal128:
    if isinstance(v, Decimal128):
        return v
    return Decimal128(Decimal(str(v)))


def _parse_local(dt_str: str, tz_name: str) -> datetime:
    """'YYYY-MM-DD HH:MM' lokal -> UTC datetime."""
    naive = datetime.strptime(dt_str.strip(), "%Y-%m-%d %H:%M")
    return naive.replace(tzinfo=ZoneInfo(tz_name)).astimezone(timezone.utc)


async def create_appointment(
    db: AsyncIOMotorDatabase,
    business: dict,
    customer: dict,
    conversation: dict,
    service: dict,
    staff: dict,
    start_local: str,
    notes: str | None = None,
    source: str | None = None,
    created_by: str = "ai",
) -> dict:
    if service["_id"] not in (staff.get("service_ids") or []):
        return {"error": "staff_cannot_perform_service"}

    tz = business.get("timezone", "Europe/Istanbul")
    try:
        start_utc = _parse_local(start_local, tz)
    except ValueError:
        return {"error": "invalid_start_time"}
    duration = int(service["duration_minutes"])
    end_utc = start_utc + timedelta(minutes=duration)

    # Atomik çakışma kontrolü
    conflict = await db.appointments.find_one({
        "business_id": business["_id"],
        "staff_id": staff["_id"],
        "status": {"$in": ["pending", "confirmed"]},
        "start_time": {"$lt": end_utc},
        "end_time": {"$gt": start_utc},
    })
    if conflict:
        return {"error": "slot_taken"}

    # Oda gerektiriyorsa, en az bir oda boş olmalı
    room_id: str | None = None
    if service.get("requires_room") and business.get("rooms"):
        rooms = business["rooms"]
        cursor = db.appointments.find({
            "business_id": business["_id"],
            "room_id": {"$ne": None},
            "status": {"$in": ["pending", "confirmed"]},
            "start_time": {"$lt": end_utc},
            "end_time": {"$gt": start_utc},
        }, {"room_id": 1})
        used_rooms = {a.get("room_id") async for a in cursor}
        free = next((r for r in rooms if r["room_id"] not in used_rooms), None)
        if not free:
            return {"error": "no_free_room"}
        room_id = free["room_id"]

    now = datetime.now(timezone.utc)
    appointment_id = ObjectId()
    guard_ids = await _reserve_guards(
        db, appointment_id, business["_id"], staff["_id"], start_utc, end_utc
    )
    if guard_ids is None:
        return {"error": "slot_taken"}
    price = _to_money_decimal128(service["price"])
    doc = {
        "business_id": business["_id"],
        "customer_id": customer["_id"],
        "staff_id": staff["_id"],
        "room_id": room_id,
        "services": [{
            "service_id": service["_id"],
            "name": service["name"],
            "duration_minutes": duration,
            "price": price,
        }],
        "start_time": start_utc,
        "end_time": end_utc,
        "status": "confirmed",
        "source": source or conversation.get("channel", "whatsapp"),
        "total_price": price,
        "payment_status": "unpaid",
        "notes": notes,
        "created_by": created_by,
        "conversation_id": conversation["_id"],
        "reminders_sent": [],
        "cancelled_reason": None,
        "created_at": now,
        "updated_at": now,
    }
    doc["_id"] = appointment_id
    try:
        res = await db.appointments.insert_one(doc)
    except Exception:
        await db.appointment_guards.delete_many({"owner": appointment_id})
        raise

    await db.customers.update_one(
        {"_id": customer["_id"]},
        {"$inc": {"total_appointments": 1}, "$set": {"last_visit": start_utc}},
    )
    await db.conversations.update_one(
        {"_id": conversation["_id"]},
        {"$set": {"state": "booked",
                  "context.booked_appointment_id": str(res.inserted_id)}},
    )

    return {
        "appointment_id": str(res.inserted_id),
        "service_name": service["name"],
        "staff_name": staff["name"],
        "start_time_local": local_iso(start_utc, tz),
        "duration_minutes": duration,
        "price": money_str(price),
        "currency": service.get("currency", "TRY"),
    }


async def find_staff_available_at(
    db: AsyncIOMotorDatabase,
    business: dict,
    service: dict,
    target: date,
    hh: int,
    mm: int,
) -> list[dict]:
    duration = int(service["duration_minutes"])
    tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
    start_local = datetime(target.year, target.month, target.day, hh, mm, tzinfo=tz)
    start_utc = start_local.astimezone(timezone.utc)
    end_utc = start_utc + timedelta(minutes=duration)

    cursor = db.staff.find({
        "business_id": business["_id"],
        "is_active": True,
        "service_ids": service["_id"],
    })
    staff_list = [s async for s in cursor]
    if not staff_list:
        return []

    apt_cursor = db.appointments.find({
        "business_id": business["_id"],
        "staff_id": {"$in": [s["_id"] for s in staff_list]},
        "status": {"$in": ["pending", "confirmed"]},
        "start_time": {"$lt": end_utc},
        "end_time": {"$gt": start_utc},
    }, {"staff_id": 1})
    busy_ids = {a["staff_id"] async for a in apt_cursor}

    s_t = start_local.time()
    e_t = (start_local + timedelta(minutes=duration)).time()
    out: list[dict] = []
    for st in staff_list:
        if st["_id"] in busy_ids or is_in_time_off(st, target):
            continue
        wh = st.get("working_hours") or business["working_hours"]
        windows = windows_for_day(wh, WEEKDAY_NAMES[target.weekday()])
        if any(w_s <= s_t and e_t <= w_e for (w_s, w_e) in windows):
            out.append(st)
    return out


async def cancel_appointment(
    db: AsyncIOMotorDatabase,
    appointment_id: str,
    reason: str = "customer_cancelled"
) -> bool:
    try:
        oid = ObjectId(appointment_id)
    except Exception:
        return False

    now = datetime.now(timezone.utc)
    res = await db.appointments.update_one(
        {"_id": oid, "status": {"$in": ["pending", "confirmed"]}},
        {"$set": {
            "status": "cancelled",
            "cancelled_reason": reason,
            "cancelled_at": now,
            "updated_at": now,
        }},
    )
    if res.modified_count:
        await db.appointment_guards.delete_many({"owner": oid})
        return True
    return False


async def reschedule_appointment(
    db: AsyncIOMotorDatabase,
    appointment_id: str,
    new_start_local: str | None,
    business: dict,
    new_service: dict | None = None,
    new_staff: dict | None = None,
) -> dict:
    try:
        oid = ObjectId(appointment_id)
    except Exception:
        return {"error": "invalid_appointment_id"}

    apt = await db.appointments.find_one({"_id": oid, "status": {"$in": ["pending", "confirmed"]}})
    if not apt:
        return {"error": "appointment_not_found"}

    tz = business.get("timezone", "Europe/Istanbul")
    
    # Yeni zaman
    target_start_utc = apt["start_time"]
    if new_start_local:
        try:
            target_start_utc = _parse_local(new_start_local, tz)
        except ValueError:
            return {"error": "invalid_start_time"}
            
    # Yeni personel
    target_staff_id = new_staff["_id"] if new_staff else apt["staff_id"]
    
    # Yeni hizmet
    service_doc = apt["services"][0]
    if new_service:
        service_doc = {
            "service_id": new_service["_id"],
            "name": new_service["name"],
            "duration_minutes": int(new_service["duration_minutes"]),
            "price": _to_money_decimal128(new_service["price"]),
        }
        
    duration = service_doc["duration_minutes"]
    target_end_utc = target_start_utc + timedelta(minutes=duration)

    # Atomik çakışma kontrolü (Kendi ID'si hariç)
    conflict = await db.appointments.find_one({
        "business_id": apt["business_id"],
        "staff_id": target_staff_id,
        "_id": {"$ne": oid},
        "status": {"$in": ["pending", "confirmed"]},
        "start_time": {"$lt": target_end_utc},
        "end_time": {"$gt": target_start_utc},
    })
    if conflict:
        return {"error": "slot_taken"}

    guard_ids = await _reserve_guards(
        db, oid, apt["business_id"], target_staff_id, target_start_utc, target_end_utc
    )
    if guard_ids is None:
        return {"error": "slot_taken"}

    update_data = {
        "start_time": target_start_utc,
        "end_time": target_end_utc,
        "staff_id": target_staff_id,
        "services": [service_doc],
        "total_price": service_doc["price"],
        "updated_at": datetime.now(timezone.utc)
    }

    await db.appointments.update_one({"_id": oid}, {"$set": update_data})
    await db.appointment_guards.delete_many(
        {"owner": oid, "_id": {"$nin": guard_ids}}
    )

    return {
        "status": "rescheduled",
        "appointment_id": appointment_id,
        "new_start_local": local_iso(target_start_utc, tz)
    }
