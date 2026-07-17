"""
WhatsApp Manager "Send flow" diyaloğu için geçerli bir test flow_token üretir.

CLI:
    python -m scripts gen-test-token <business_slug>
    → biz:<biz_oid>:conv:<conv_oid>:<nonce>

Token, ilgili business'ın seed'den gelen veya yeni yaratılan boş bir
'preview' conversation'ına bağlanır. `flow.py:parse_flow_token` bunu
çözebilir; ekran submit'leri 200 döner ve gerçek endpoint logic'i
(slot kontrol + create_appointment) çalışır.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from app.channels.whatsapp.flow_sender import make_flow_token
from app.core.db import get_db


async def _build_token(slug: str) -> str | None:
    db = get_db()
    biz = await db.businesses.find_one({"business_id": slug})
    if not biz:
        return None

    preview_thread = f"preview_{biz['business_id']}"
    conv = await db.conversations.find_one({
        "business_id": biz["_id"],
        "channel": "whatsapp",
        "channel_thread_id": preview_thread,
    })
    if not conv:
        cust = await db.customers.find_one({
            "business_id": biz["_id"],
            "whatsapp_id": preview_thread,
        })
        now = datetime.now(timezone.utc)
        if not cust:
            cust_res = await db.customers.insert_one({
                "business_id": biz["_id"],
                "whatsapp_id": preview_thread,
                "phone": "+0000000000",
                "name": "Preview Tester",
                "tags": ["preview"],
                "total_appointments": 0,
                "no_show_count": 0,
                "cancel_count": 0,
                "is_blocked": False,
                "consent": {"marketing_sms": False, "kvkk_accepted_at": None},
                "created_at": now,
            })
            cust_id = cust_res.inserted_id
        else:
            cust_id = cust["_id"]

        conv_res = await db.conversations.insert_one({
            "business_id": biz["_id"],
            "customer_id": cust_id,
            "channel": "whatsapp",
            "channel_thread_id": preview_thread,
            "state": "selecting_service",
            "context": {},
            "messages": [],
            "created_at": now,
            "last_active_at": now,
            "closed_at": None,
        })
        conv_oid = conv_res.inserted_id
    else:
        conv_oid = conv["_id"]

    return make_flow_token(biz["_id"], conv_oid)


def gen_test_token(slug: str) -> str | None:
    """Synchronous wrapper. Returns token string veya None (business yoksa)."""
    return asyncio.run(_build_token(slug))
