#!/usr/bin/env python3
"""Çalışan SIP logundaki aranan numarayı değerini yazdırmadan işletmeye bağlar."""
from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.db import close_client, get_db
from app.voice.identity import normalize_phone


async def main() -> None:
    candidates: list[str] = []
    for path in Path("/root/.pm2/logs").glob("randevumonline-*.log"):
        if not path.is_file():
            continue
        text = path.read_text(errors="ignore")[-2_000_000:]
        candidates.extend(re.findall(r"INVITE\s+sip:(\+?\d{7,15})@", text, re.I))
    dids = {normalize_phone(value) for value in candidates if normalize_phone(value)}
    if len(dids) != 1:
        raise SystemExit(f"Güvenli DID keşfi başarısız: distinct_count={len(dids)}")
    did = dids.pop()
    db = get_db()
    existing = await db.businesses.find_one(
        {"channels.voice.dids": did}, {"business_id": 1}
    )
    if existing and existing.get("business_id") != "berber_mehmet_kutahya":
        raise SystemExit("DID başka bir işletmeye bağlı; değişiklik yapılmadı")
    result = await db.businesses.update_one(
        {"business_id": "berber_mehmet_kutahya"},
        {"$set": {"channels.voice.enabled": True, "channels.voice.dids": [did]}},
    )
    if result.matched_count != 1:
        raise SystemExit("Hedef işletme bulunamadı; değişiklik yapılmadı")
    print("voice_did_migration=ok did_count=1 value=redacted")
    await close_client()


if __name__ == "__main__":
    asyncio.run(main())
