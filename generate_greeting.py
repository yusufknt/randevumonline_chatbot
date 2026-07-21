from __future__ import annotations

import asyncio
import os
import subprocess
from pathlib import Path

from app.core.db import close_client, get_db
from app.voice.tts import TextToSpeechEngine


async def greeting_text() -> str:
    db = get_db()
    business = await db.businesses.find_one(
        {"business_id": "berber_mehmet_kutahya"}, {"_id": 1}
    )
    if not business:
        raise RuntimeError("Karşılama için işletme bulunamadı")
    staff = await db.staff.find(
        {"business_id": business["_id"], "is_active": True}, {"name": 1}
    ).to_list(20)
    first_names = [str(item["name"]).split()[0] for item in staff if item.get("name")]
    if not first_names:
        raise RuntimeError("Karşılama için aktif berber bulunamadı")
    if len(first_names) == 1:
        spoken_names = first_names[0]
    else:
        spoken_names = ", ".join(first_names[:-1]) + " ve " + first_names[-1]
    return (
        "Merhaba. Randevum Online sistemine hoş geldiniz. "
        f"Uygun berberlerimiz: {spoken_names}. "
        "Hangisini tercih edersiniz?"
    )


async def main() -> None:
    assets = Path(__file__).resolve().parent / "app" / "voice" / "assets"
    pcm_path = assets / "greeting.slin"
    pcm_tmp = assets / ".greeting.slin.tmp"
    alaw_path = assets / "greeting.alaw"
    alaw_tmp = assets / ".greeting.alaw.tmp"

    engine = TextToSpeechEngine()
    try:
        text = await greeting_text()
        with pcm_tmp.open("wb") as output:
            async for chunk in engine.synthesize_stream(text):
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        if pcm_tmp.stat().st_size < 3200:
            raise RuntimeError("Karşılama sesi beklenenden kısa üretildi")
        os.replace(pcm_tmp, pcm_path)

        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-f", "s16le", "-ar", "8000", "-ac", "1", "-i", str(pcm_path),
                "-f", "alaw", "-ar", "8000", "-ac", "1", "-y", str(alaw_tmp),
            ],
            check=True,
        )
        os.replace(alaw_tmp, alaw_path)
        print(f"greeting=ok pcm_bytes={pcm_path.stat().st_size}")
    finally:
        await TextToSpeechEngine.shutdown()
        await close_client()
        pcm_tmp.unlink(missing_ok=True)
        alaw_tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
