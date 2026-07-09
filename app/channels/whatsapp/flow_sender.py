from __future__ import annotations

import json
import logging
import secrets
from datetime import datetime, timezone

import httpx
from bson import ObjectId

from app.core.config import get_settings
from app.core.db import get_secret, update_conversation_context
from app.core.format import truncate as _truncate

log = logging.getLogger(__name__)

FLOW_TOKEN_NONCE_BYTES = 16  # 128-bit; Meta: "should not be predictable"


def make_flow_token(business_oid: ObjectId, conversation_oid: ObjectId) -> str:
    nonce = secrets.token_hex(FLOW_TOKEN_NONCE_BYTES)
    return f"biz:{business_oid}:conv:{conversation_oid}:{nonce}"


def parse_flow_token(token: str) -> tuple[ObjectId, ObjectId] | None:
    try:
        parts = token.split(":")
        if len(parts) != 5 or parts[0] != "biz" or parts[2] != "conv":
            return None
        return ObjectId(parts[1]), ObjectId(parts[3])
    except Exception:
        return None


def get_flow_private_key() -> str | None:
    settings = get_settings()
    if settings.wa_flow_private_key:
        return settings.wa_flow_private_key
    if settings.wa_flow_private_key_path:
        try:
            with open(settings.wa_flow_private_key_path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            log.exception("Flow private key dosyası okunamadı: %s",
                          settings.wa_flow_private_key_path)
    return None


async def send_booking_flow(business: dict, conversation: dict, wa_id: str) -> dict:
    wa_cfg = (business.get("channels") or {}).get("whatsapp") or {}
    flow_id = wa_cfg.get("flow_id")
    if not flow_id:
        return {"error": "flow_not_configured"}

    token = make_flow_token(business["_id"], conversation["_id"])
    settings = get_settings()
    phone_number_id = wa_cfg["phone_number_id"]
    access_token = get_secret(wa_cfg["access_token_ref"])
    url = f"{settings.wa_graph_base_url}/{phone_number_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": wa_id,
        "type": "interactive",
        "interactive": {
            "type": "flow",
            "header": {"type": "text",
                       "text": _truncate(f"{business['name']}", 60)},
            "body": {"text": (
                f"Merhaba! {business['name']}'a hoş geldiniz.\n"
                "Randevu almak için aşağıdaki butona dokunmanız yeterli."
            )},
            "footer": {"text": "Birkaç adımda biter."},
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_message_version": "3",
                    "flow_token": token,
                    "flow_id": str(flow_id),
                    "flow_cta": "Randevu Al",
                    "flow_action": "navigate",
                    "flow_action_payload": {
                        "screen": "AD_SOYAD",
                    },
                    **({"mode": settings.wa_flow_mode}
                       if settings.wa_flow_mode else {}),
                },
            },
        },
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {access_token}",
                     "Content-Type": "application/json"},
            json=payload,
        )
        if resp.status_code >= 400:
            log.error("WA Flow CTA HTTP %s: %s", resp.status_code, resp.text)
            resp.raise_for_status()
        data = resp.json()

    await update_conversation_context(
        conversation["_id"],
        {"flow_token": token, "flow_started_at": datetime.now(timezone.utc)},
        state="selecting_service",
    )
    return {
        "ok": True,
        "flow_token": token,
        "wa_message_id": data.get("messages", [{}])[0].get("id"),
    }


def summary_text_from_nfm_reply(response_json: str) -> str:
    try:
        p = json.loads(response_json)
    except Exception:
        log.exception("nfm_reply response_json parse hatası")
        return "Randevunuz alındı. Detayları kontrol ediyoruz."

    parts = ["✅ Randevunuz onaylandı."]
    if p.get("service_name"):
        parts.append(f"• {p['service_name']}")
    if p.get("start_time_local"):
        parts.append(f"• {p['start_time_local']}")
    if p.get("staff_name"):
        parts.append(f"• Personel: {p['staff_name']}")
    if p.get("duration_minutes"):
        parts.append(f"• Süre: {p['duration_minutes']} dk")
    if p.get("price"):
        parts.append(f"• Ücret: {p['price']}₺")
    parts.append("")
    parts.append("Görüşmek üzere!")
    return "\n".join(parts)
