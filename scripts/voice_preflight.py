#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import hashlib
import os
import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.db import close_client, get_db
from app.voice.config import get_voice_settings


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:12]


async def main() -> None:
    cfg = get_voice_settings()
    missing = cfg.validate_critical_connections()
    checks = {
        "critical_env": not missing,
        "asterisk_audiosocket": Path(
            "/usr/lib/x86_64-linux-gnu/asterisk/modules/app_audiosocket.so"
        ).is_file(),
        "silero_model": Path(cfg.voice_vad_model).is_file(),
        "greeting_pcm": Path(cfg.voice_greeting_pcm).is_file(),
        "wireguard": Path("/sys/class/net/wg0").exists(),
    }
    db = get_db()
    await db.command("ping")
    checks["mongo"] = True
    checks["voice_did"] = await db.businesses.count_documents({
        "channels.voice.enabled": True,
        "channels.voice.dids.0": {"$exists": True},
    }) > 0
    print("checks=" + ",".join(f"{k}:{'ok' if v else 'fail'}" for k, v in checks.items()))
    print(
        "connection_fingerprints="
        f"mongo:{fingerprint(os.getenv('MONGODB_URL', ''))},"
        f"deepseek:{fingerprint(cfg.deepseek_base_url)},"
        f"tts:{fingerprint(cfg.tts_api_base_url)}"
    )
    await close_client()
    if not all(checks.values()):
        raise SystemExit("preflight=failed missing=" + ",".join(missing))
    print("preflight=ok")


if __name__ == "__main__":
    asyncio.run(main())
