from __future__ import annotations

import asyncio
import json
import sys

import httpx

from app.channels.instagram.flow import (
    PB_BOOK,
    PB_HUMAN,
    PB_INFO,
    PB_SERVICES,
)
from app.core.config import get_settings
from app.core.db import close_client, find_business_by_slug, get_secret


def _profile_url(business: dict) -> tuple[str, str]:
    settings = get_settings()
    ig_cfg = (business.get("channels") or {}).get("instagram") or {}
    if not ig_cfg.get("enabled"):
        raise RuntimeError("Instagram kanalı kapalı.")
    ig_user_id = ig_cfg["ig_user_id"]
    token = get_secret(ig_cfg["access_token_ref"])
    url = f"{settings.ig_graph_base_url}/{ig_user_id}/messenger_profile"
    return url, token


def _build_persistent_menu(business: dict) -> dict:
    booking_url = (business.get("contact") or {}).get("booking_url")
    ctas: list[dict] = []
    if booking_url:
        ctas.append({
            "type": "web_url",
            "title": "📅 Randevu Al",
            "url": booking_url,
        })
    ctas.extend([
        {"type": "postback", "title": "💇 Hizmetler",          "payload": PB_SERVICES},
        {"type": "postback", "title": "ℹ️ Bilgi",              "payload": PB_INFO},
        {"type": "postback", "title": "💬 Müşteri Temsilcisi", "payload": PB_HUMAN},
    ])
    return {
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": False,
                "call_to_actions": ctas,
            }
        ]
    }


def _build_ice_breakers(business: dict) -> dict:
    return {
        "ice_breakers": [
            {
                "locale": "default",
                "call_to_actions": [
                    {"question": "📅 Nasıl randevu alabilirim?",    "payload": PB_BOOK},
                    {"question": "💇 Hizmetler ve fiyatlar neler?", "payload": PB_SERVICES},
                    {"question": "💬 Müşteri temsilcisine bağlan.", "payload": PB_HUMAN},
                ]
            }
        ]
    }


async def cmd_set(slug: str) -> int:
    business = await find_business_by_slug(slug)
    if not business:
        print(f"❌ İşletme bulunamadı: {slug}", file=sys.stderr)
        return 2
    url, token = _profile_url(business)

    payload = {"platform": "instagram"}
    payload.update(_build_persistent_menu(business))
    payload.update(_build_ice_breakers(business))

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json=payload,
        )
        if resp.status_code >= 400:
            print(f"❌ HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        print(f"✅ {slug}: persistent_menu + ice_breakers kuruldu.")
        print(resp.json())
    return 0


async def cmd_get(slug: str) -> int:
    business = await find_business_by_slug(slug)
    if not business:
        print(f"❌ İşletme bulunamadı: {slug}", file=sys.stderr)
        return 2
    url, token = _profile_url(business)

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            url,
            params={"fields": "persistent_menu,ice_breakers"},
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code >= 400:
            print(f"❌ HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    return 0


async def cmd_delete(slug: str) -> int:
    business = await find_business_by_slug(slug)
    if not business:
        print(f"❌ İşletme bulunamadı: {slug}", file=sys.stderr)
        return 2
    url, token = _profile_url(business)

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            "DELETE", url,
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json={"fields": ["persistent_menu", "ice_breakers"]},
        )
        if resp.status_code >= 400:
            print(f"❌ HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
            return 1
        print(f"✅ {slug}: persistent_menu + ice_breakers silindi.")
    return 0


async def run(action: str, slug: str) -> int:
    try:
        if action == "set":
            return await cmd_set(slug)
        elif action == "get":
            return await cmd_get(slug)
        elif action == "delete":
            return await cmd_delete(slug)
        else:
            print(f"Bilinmeyen aksiyon: {action}", file=sys.stderr)
            return 2
    finally:
        try:
            await close_client()
        except RuntimeError:
            pass
