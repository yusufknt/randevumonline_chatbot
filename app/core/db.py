from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from app.core.config import get_settings

log = logging.getLogger(__name__)

_client: AsyncIOMotorClient | None = None


def to_oid(value: str | ObjectId) -> ObjectId:
    """str/ObjectId → ObjectId (geçersizse ValueError fırlatır)."""
    return value if isinstance(value, ObjectId) else ObjectId(value)


def try_oid(value: str | ObjectId | None) -> ObjectId | None:
    """24 haneli hex str ya da ObjectId → ObjectId; aksi halde None."""
    if isinstance(value, ObjectId):
        return value
    if not isinstance(value, str) or len(value) != 24:
        return None
    try:
        return ObjectId(value)
    except Exception:
        return None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(settings.mongodb_url, tz_aware=True)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    return get_client()[get_settings().mongodb_db]


async def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


async def init_indexes() -> None:
    db = get_db()

    await db.businesses.create_index("business_id", unique=True)
    await db.businesses.create_index("business_type")
    await db.businesses.create_index(
        "contact.whatsapp_number", unique=True, sparse=True,
    )
    await db.businesses.create_index("channels.whatsapp.phone_number_id",
                                     sparse=True)
    await db.businesses.create_index("channels.instagram.ig_user_id",
                                     sparse=True)
    await db.businesses.create_index(
        "channels.voice.dids",
        unique=True,
        partialFilterExpression={"channels.voice.dids": {"$type": "array"}},
    )

    await db.staff.create_index([("business_id", 1), ("is_active", 1)])
    await db.staff.create_index([
        ("business_id", 1), ("is_active", 1), ("service_ids", 1),
    ])

    await db.services.create_index([("business_id", 1), ("is_active", 1)])
    await db.services.create_index([("business_id", 1), ("category", 1)])

    # sparse yerine partialFilterExpression: her iki alan opsiyonel ama unique
    # olmalı — Mongo aynı indekste ikisini kabul etmez.
    await db.customers.create_index(
        [("business_id", 1), ("whatsapp_id", 1)],
        unique=True,
        partialFilterExpression={"whatsapp_id": {"$type": "string"}},
    )
    await db.customers.create_index(
        [("business_id", 1), ("instagram_user_id", 1)],
        unique=True,
        partialFilterExpression={"instagram_user_id": {"$type": "string"}},
    )
    await db.customers.create_index([("business_id", 1), ("phone", 1)])
    await db.customers.create_index([("business_id", 1), ("is_blocked", 1)])

    await db.appointments.create_index([
        ("business_id", 1), ("staff_id", 1), ("start_time", 1),
    ])
    await db.appointments.create_index([
        ("business_id", 1), ("staff_id", 1), ("status", 1),
        ("start_time", 1), ("end_time", 1),
    ])
    await db.appointments.create_index([
        ("business_id", 1), ("status", 1), ("room_id", 1),
        ("start_time", 1), ("end_time", 1),
    ])
    await db.appointments.create_index([
        ("business_id", 1), ("status", 1), ("start_time", 1),
    ])
    await db.appointments.create_index([("customer_id", 1), ("start_time", -1)])
    await db.appointments.create_index([("status", 1), ("start_time", 1)])

    await db.conversations.create_index(
        [("business_id", 1), ("channel", 1), ("channel_thread_id", 1)],
        unique=True,
    )
    await db.conversations.create_index(
        [("business_id", 1), ("state", 1), ("last_active_at", -1)],
    )

    # Webhook tekrarlarına karşı idempotency: işlenen mesaj id'leri 24 saat tutulur.
    await db.processed_messages.create_index("created_at", expireAfterSeconds=86400)
    await db.voice_calls.create_index("created_at", expireAfterSeconds=2592000)
    await db.voice_calls.create_index([("business_id", 1), ("created_at", -1)])

    # İnsana aktarma (handoff) kuyruğu — açık (resolved=False) kayıtlar bir
    # operasyon panelinden/cron'dan okunabilir.
    await db.escalations.create_index([("business_id", 1), ("resolved", 1),
                                       ("created_at", -1)])


async def find_business_by_id(business_id: ObjectId | str) -> dict | None:
    db = get_db()
    if isinstance(business_id, str) and ObjectId.is_valid(business_id):
        business_id = ObjectId(business_id)
    return await db.businesses.find_one({"_id": business_id})


async def find_business_by_slug(slug: str) -> dict | None:
    return await get_db().businesses.find_one({"business_id": slug})


async def find_business_by_wa_phone_number_id(phone_number_id: str) -> dict | None:
    return await get_db().businesses.find_one(
        {"channels.whatsapp.phone_number_id": phone_number_id}
    )


async def find_business_by_ig_user_id(ig_user_id: str) -> dict | None:
    return await get_db().businesses.find_one(
        {"channels.instagram.ig_user_id": ig_user_id}
    )


async def list_active_services(business_id: ObjectId) -> list[dict]:
    cursor = get_db().services.find(
        {"business_id": business_id, "is_active": True}
    ).sort([("category", 1), ("name", 1)])
    return [s async for s in cursor]


async def upsert_customer_by_whatsapp(
    business_id: ObjectId, wa_id: str, name: str | None = None
) -> dict:
    db = get_db()
    now = datetime.now(timezone.utc)
    res = await db.customers.find_one_and_update(
        {"business_id": business_id, "whatsapp_id": wa_id},
        {
            "$setOnInsert": {
                "business_id": business_id,
                "whatsapp_id": wa_id,
                "phone": "+" + wa_id if not wa_id.startswith("+") else wa_id,
                "name": name,
                "tags": [],
                "total_appointments": 0,
                "no_show_count": 0,
                "cancel_count": 0,
                "is_blocked": False,
                "consent": {"marketing_sms": False, "kvkk_accepted_at": None},
                "created_at": now,
            }
        },
        upsert=True,
        return_document=True,
    )
    return res


async def upsert_customer_by_instagram(
    business_id: ObjectId, ig_user_id: str, username: str | None = None
) -> dict:
    db = get_db()
    now = datetime.now(timezone.utc)
    res = await db.customers.find_one_and_update(
        {"business_id": business_id, "instagram_user_id": ig_user_id},
        {
            "$setOnInsert": {
                "business_id": business_id,
                "instagram_user_id": ig_user_id,
                "instagram_username": username,
                "tags": [],
                "total_appointments": 0,
                "no_show_count": 0,
                "cancel_count": 0,
                "is_blocked": False,
                "consent": {"marketing_sms": False, "kvkk_accepted_at": None},
                "created_at": now,
            }
        },
        upsert=True,
        return_document=True,
    )
    return res


async def upsert_customer_by_phone(
    business_id: ObjectId, phone: str, name: str | None = None
) -> dict:
    db = get_db()
    now = datetime.now(timezone.utc)
    return await db.customers.find_one_and_update(
        {"business_id": business_id, "phone": phone},
        {
            "$setOnInsert": {
                "business_id": business_id,
                "phone": phone,
                "name": name or "Telefon Müşterisi",
                "tags": [],
                "total_appointments": 0,
                "no_show_count": 0,
                "cancel_count": 0,
                "is_blocked": False,
                "consent": {"marketing_sms": False, "kvkk_accepted_at": None},
                "created_at": now,
            }
        },
        upsert=True,
        return_document=True,
    )


async def upsert_conversation(
    business_id: ObjectId,
    channel: str,
    channel_thread_id: str,
    customer_id: ObjectId | None = None,
) -> dict:
    db = get_db()
    now = datetime.now(timezone.utc)
    res = await db.conversations.find_one_and_update(
        {
            "business_id": business_id,
            "channel": channel,
            "channel_thread_id": channel_thread_id,
        },
        {
            "$setOnInsert": {
                "business_id": business_id,
                "channel": channel,
                "channel_thread_id": channel_thread_id,
                "customer_id": customer_id,
                "state": "greeting",
                "context": {},
                "messages": [],
                "created_at": now,
                "closed_at": None,
            },
            "$set": {"last_active_at": now},
        },
        upsert=True,
        return_document=True,
    )
    if customer_id is not None and res.get("customer_id") is None:
        await db.conversations.update_one(
            {"_id": res["_id"]}, {"$set": {"customer_id": customer_id}}
        )
        res["customer_id"] = customer_id
    return res


async def append_conversation_message(conv_id: ObjectId, message: dict) -> None:
    await get_db().conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {"messages": message},
            "$set": {"last_active_at": message["timestamp"]},
        },
    )


async def append_conversation_messages(
    conv_id: ObjectId, messages: list[dict]
) -> None:
    """Bir konuşma mesaj grubunu tek MongoDB güncellemesiyle sıralı ekle."""
    if not messages:
        return
    await get_db().conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {"messages": {"$each": messages}},
            "$set": {"last_active_at": messages[-1]["timestamp"]},
        },
    )


async def update_conversation_context(
    conv_id: ObjectId, context_patch: dict, state: str | None = None
) -> None:
    set_op = {f"context.{k}": v for k, v in context_patch.items()}
    if state is not None:
        set_op["state"] = state
    if set_op:
        await get_db().conversations.update_one({"_id": conv_id}, {"$set": set_op})


async def claim_inbound_message(channel: str, message_id: str | None) -> bool:
    """Bir webhook mesajının tek kez işlenmesini garanti eder (idempotency).

    Döner: True → ilk kez görüldü, işlenmeli; False → tekrar, atlanmalı.
    message_id yoksa (ör. bazı referral/postback olayları) dedup yapılamaz ve
    True döner.
    """
    if not message_id:
        return True
    try:
        await get_db().processed_messages.insert_one({
            "_id": f"{channel}:{message_id}",
            "created_at": datetime.now(timezone.utc),
        })
        return True
    except DuplicateKeyError:
        return False


async def record_escalation(
    business_id: ObjectId,
    conversation_id: ObjectId,
    customer_id: ObjectId | None,
    reason: str | None,
    channel: str,
) -> None:
    """İnsana aktarma talebini kuyruğa yazar (operasyon paneli/cron için)."""
    await get_db().escalations.insert_one({
        "business_id": business_id,
        "conversation_id": conversation_id,
        "customer_id": customer_id,
        "channel": channel,
        "reason": reason,
        "resolved": False,
        "created_at": datetime.now(timezone.utc),
    })


def get_secret(ref: str) -> str:
    """vault://wa/<slug>/token → WA_<SLUG>_TOKEN env; prod'da vault ile değiştir."""
    if not ref:
        raise ValueError("Boş secret ref")
    if ref.startswith("vault://"):
        env_key = ref.removeprefix("vault://").replace("/", "_").upper()
        val = os.getenv(env_key)
        if not val:
            raise RuntimeError(f"Secret bulunamadı: {ref} (env {env_key})")
        return val
    return ref
