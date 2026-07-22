#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import hashlib
import os
import socket
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.db import close_client, get_db
from app.core.session_cache import close_voice_session_cache, get_voice_session_cache
from app.voice.config import get_voice_settings


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:12]


def valid_phone_wav(value: str) -> bool:
    path = Path(value)
    if not path.is_file() or path.suffix.lower() != ".wav":
        return False
    try:
        with wave.open(str(path), "rb") as audio:
            return (
                audio.getnchannels(),
                audio.getsampwidth(),
                audio.getframerate(),
                audio.getcomptype(),
            ) == (1, 2, 8000, "NONE") and audio.getnframes() > 0
    except (OSError, EOFError, wave.Error):
        return False


async def main() -> None:
    cfg = get_voice_settings()
    missing = cfg.validate_critical_connections()
    checks = {
        "critical_env": not missing,
        "native_sip_acl": bool(cfg.voice_sip_allowed_hosts.strip()),
        "native_sip_port": 0 < cfg.voice_server_port < 65536,
        "native_rtp_range": (
            0 < cfg.rtp_start_port <= cfg.rtp_end_port < 65536
            and cfg.rtp_start_port % 2 == 0
        ),
        "silero_model": Path(cfg.voice_vad_model).is_file(),
        "greeting_pcm": valid_phone_wav(cfg.voice_greeting_pcm),
        "opening_pcm": valid_phone_wav(cfg.voice_opening_pcm),
        "booking_success_pcm": valid_phone_wav(cfg.voice_booking_success_pcm),
        "wireguard": Path("/sys/class/net/wg0").exists(),
    }
    db = get_db()
    await db.command("ping")
    checks["mongo"] = True
    checks["redis"] = await get_voice_session_cache().ping()
    checks["voice_did"] = await db.businesses.count_documents({
        "channels.voice.enabled": True,
        "channels.voice.dids.0": {"$exists": True},
    }) > 0
    print("checks=" + ",".join(f"{k}:{'ok' if v else 'fail'}" for k, v in checks.items()))
    print(
        "connection_fingerprints="
        f"mongo:{fingerprint(os.getenv('MONGODB_URL', ''))},"
        f"redis:{fingerprint(os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0'))},"
        f"deepseek:{fingerprint(cfg.deepseek_base_url)},"
        f"tts:{fingerprint(cfg.tts_api_base_url)}"
    )
    await close_voice_session_cache()
    await close_client()
    if not all(checks.values()):
        raise SystemExit("preflight=failed missing=" + ",".join(missing))
    print("preflight=ok")


if __name__ == "__main__":
    asyncio.run(main())
