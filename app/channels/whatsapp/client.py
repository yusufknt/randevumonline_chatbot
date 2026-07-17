from __future__ import annotations

import hashlib
import hmac
import logging
from dataclasses import dataclass

import httpx

from app.core.config import get_settings
from app.core.db import get_secret

log = logging.getLogger(__name__)


@dataclass
class WhatsAppInboundMessage:
    phone_number_id: str
    wa_id: str
    profile_name: str | None
    text: str
    message_id: str
    interactive_type: str | None = None
    nfm_response_json: str | None = None


def verify_signature(body: bytes, signature_header: str | None) -> bool:
    settings = get_settings()
    if not settings.wa_app_secret:
        log.warning("WA_APP_SECRET ayarlı değil — signature doğrulama atlanıyor.")
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(
        settings.wa_app_secret.encode(), body, hashlib.sha256
    ).hexdigest()
    received = signature_header.split("=", 1)[1]
    return hmac.compare_digest(expected, received)


def parse_inbound(payload: dict) -> list[WhatsAppInboundMessage]:
    out: list[WhatsAppInboundMessage] = []
    for entry in payload.get("entry") or []:
        for change in entry.get("changes") or []:
            value = change.get("value") or {}
            metadata = value.get("metadata") or {}
            phone_number_id = metadata.get("phone_number_id")
            contacts = {c["wa_id"]: c.get("profile", {}).get("name")
                        for c in (value.get("contacts") or [])}
            for msg in value.get("messages") or []:
                msg_type = msg.get("type")
                wa_id = msg.get("from")
                base = dict(
                    phone_number_id=phone_number_id,
                    wa_id=wa_id,
                    profile_name=contacts.get(wa_id),
                    message_id=msg.get("id"),
                )
                if msg_type == "text":
                    out.append(WhatsAppInboundMessage(
                        **base,
                        text=(msg.get("text") or {}).get("body", ""),
                    ))
                elif msg_type == "interactive":
                    inter = msg.get("interactive") or {}
                    if inter.get("type") == "nfm_reply":
                        nr = inter.get("nfm_reply") or {}
                        out.append(WhatsAppInboundMessage(
                            **base,
                            text=nr.get("body", ""),
                            interactive_type="nfm_reply",
                            nfm_response_json=nr.get("response_json"),
                        ))
    return out


def _wa_endpoint(business: dict) -> tuple[str, str]:
    settings = get_settings()
    wa_cfg = (business.get("channels") or {}).get("whatsapp") or {}
    if not wa_cfg.get("enabled"):
        raise RuntimeError("Bu işletme için WhatsApp kanalı kapalı.")
    phone_number_id = wa_cfg["phone_number_id"]
    token = get_secret(wa_cfg["access_token_ref"])
    url = f"{settings.wa_graph_base_url}/{phone_number_id}/messages"
    return url, token


async def send_text(business: dict, wa_id: str, text: str) -> dict:
    url, token = _wa_endpoint(business)
    payload = {
        "messaging_product": "whatsapp",
        "to": wa_id,
        "type": "text",
        "text": {"body": text[:4096]},
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()


