"""Instagram (Instagram-login API) uzun ömürlü erişim token'ı yenileme.

IG-login long-lived token'ları ~60 günde sona erer. Bu script mevcut token'ı
`graph.instagram.com/refresh_access_token` ile yeniler ve yeni token + kalan
süreyi yazdırır. Token env/vault'ta tutulduğundan otomatik yazma yapılmaz;
operatör çıktıyı ilgili `IG_<SLUG>_ACCESS_TOKEN` değişkenine kopyalar.

Not: Yenileme için token en az 24 saatlik ve hâlâ geçerli olmalıdır.
"""
from __future__ import annotations

import sys

import httpx

from app.core.config import get_settings
from app.core.db import close_client, find_business_by_slug, get_secret


def _refresh_host() -> str:
    # Versiyon yolu olmadan host; ig_graph_base_url'den ana host'u türet.
    base = get_settings().ig_graph_base_url
    # "https://graph.instagram.com/v25.0" → "https://graph.instagram.com"
    parts = base.split("/")
    return "/".join(parts[:3]) if len(parts) >= 3 else "https://graph.instagram.com"


async def cmd_refresh(slug: str) -> int:
    business = await find_business_by_slug(slug)
    if not business:
        print(f"❌ İşletme bulunamadı: {slug}", file=sys.stderr)
        return 2

    ig_cfg = (business.get("channels") or {}).get("instagram") or {}
    if not ig_cfg.get("enabled"):
        print("❌ Instagram kanalı kapalı.", file=sys.stderr)
        return 2

    ref = ig_cfg.get("access_token_ref")
    try:
        token = get_secret(ref)
    except Exception as e:
        print(f"❌ Token okunamadı ({ref}): {e}", file=sys.stderr)
        return 1

    url = f"{_refresh_host()}/refresh_access_token"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params={
            "grant_type": "ig_refresh_token",
            "access_token": token,
        })
    if resp.status_code >= 400:
        print(f"❌ HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        return 1

    data = resp.json()
    new_token = data.get("access_token")
    expires_in = data.get("expires_in")
    days = round(expires_in / 86400, 1) if isinstance(expires_in, int) else "?"
    env_key = (ref or "").removeprefix("vault://").replace("/", "_").upper()

    print(f"✅ {slug}: token yenilendi (geçerlilik ~{days} gün).")
    print(f"   Yeni token'ı şu değişkene yazın:\n")
    print(f"   {env_key or 'IG_<SLUG>_ACCESS_TOKEN'}={new_token}")
    return 0


async def run(slug: str) -> int:
    try:
        return await cmd_refresh(slug)
    finally:
        try:
            await close_client()
        except RuntimeError:
            pass
