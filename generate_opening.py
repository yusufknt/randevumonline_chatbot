from __future__ import annotations

import asyncio
import os
import subprocess
from pathlib import Path

from app.core.db import close_client, get_db
from app.voice.config import get_voice_settings
from app.voice.tts import TextToSpeechEngine


async def main() -> None:
    cfg = get_voice_settings()
    slug = cfg.voice_default_business_slug or "berber_mehmet_kutahya"
    db = get_db()
    business = await db.businesses.find_one({"business_id": slug}, {"_id": 1})
    if not business:
        raise RuntimeError("Personel anonsu için işletme bulunamadı")
    staff = await db.staff.find(
        {"business_id": business["_id"], "is_active": True}, {"name": 1}
    ).to_list(100)
    names = [str(item.get("name", "")).split()[0] for item in staff[:4]]
    if not names:
        raise RuntimeError("Personel anonsu için aktif berber bulunamadı")
    spoken = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " ve " + names[-1]
    text = f"Berberlerimiz: {spoken}. Hangisini tercih edersiniz?"

    assets = Path(__file__).resolve().parent / "app" / "voice" / "assets"
    slin_path = assets / "opening.slin"
    slin_tmp = assets / ".opening.slin.tmp"
    wav_path = assets / "opening.wav"
    wav_tmp = assets / ".opening.wav.tmp"
    engine = TextToSpeechEngine(request_read_timeout_s=60)
    try:
        with slin_tmp.open("wb") as output:
            async for chunk in engine.synthesize_stream(text):
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        if slin_tmp.stat().st_size < 3200:
            raise RuntimeError("Personel anonsu beklenenden kısa üretildi")
        os.replace(slin_tmp, slin_path)
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-f", "s16le", "-ar", "8000", "-ac", "1", "-i", str(slin_path),
                "-ar", "8000", "-ac", "1", "-c:a", "pcm_s16le",
                "-f", "wav", "-y", str(wav_tmp),
            ],
            check=True,
        )
        os.replace(wav_tmp, wav_path)
        print(f"opening=ok text={text} wav_bytes={wav_path.stat().st_size}")
    finally:
        await TextToSpeechEngine.shutdown()
        await close_client()
        slin_tmp.unlink(missing_ok=True)
        wav_tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    from generate_voice_prompts import main as generate_all_voice_prompts

    asyncio.run(generate_all_voice_prompts())
