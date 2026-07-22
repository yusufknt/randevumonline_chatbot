from __future__ import annotations

import asyncio
import os
import subprocess
import wave
from pathlib import Path

from app.core.db import close_client, get_db
from app.voice.config import get_voice_settings
from app.voice.tts import TextToSpeechEngine


def _spoken_names(names: list[str]) -> str:
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " ve " + names[-1]


def _validate_wav(path: Path) -> None:
    with wave.open(str(path), "rb") as audio:
        value = (
            audio.getnchannels(),
            audio.getsampwidth(),
            audio.getframerate(),
            audio.getcomptype(),
        )
        frames = audio.getnframes()
    if value != (1, 2, 8000, "NONE") or frames <= 0:
        raise RuntimeError(f"Geçersiz telefon WAV dosyası: {path.name}")


async def main() -> None:
    cfg = get_voice_settings()
    slug = cfg.voice_default_business_slug or "berber_mehmet_kutahya"
    db = get_db()
    business = await db.businesses.find_one({"business_id": slug}, {"_id": 1})
    if not business:
        raise RuntimeError("Ses anonsları için işletme bulunamadı")
    staff = await db.staff.find(
        {"business_id": business["_id"], "is_active": True}, {"name": 1}
    ).to_list(100)
    names = [str(item.get("name", "")).split()[0] for item in staff[:4]]
    if not names:
        raise RuntimeError("Ses anonsları için aktif berber bulunamadı")

    prompts = {
        "greeting": (
            "Merhaba. Randevum Online sistemine hoş geldiniz. "
            "Uygun berberlerimiz:"
        ),
        "opening": f"{_spoken_names(names)}. Hangisini tercih edersiniz?",
        "booking_success": "Randevunuz oluşturuldu. İyi günler.",
    }
    assets = Path(__file__).resolve().parent / "app" / "voice" / "assets"
    token = str(os.getpid())
    temporary: list[Path] = []
    completed: dict[str, Path] = {}
    engine = TextToSpeechEngine(request_read_timeout_s=60)
    try:
        for name, text in prompts.items():
            slin_tmp = assets / f".{name}.{token}.slin.tmp"
            wav_tmp = assets / f".{name}.{token}.wav.tmp"
            temporary.extend((slin_tmp, wav_tmp))
            with slin_tmp.open("wb") as output:
                async for chunk in engine.synthesize_stream(text):
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            if slin_tmp.stat().st_size < 3200:
                raise RuntimeError(f"{name} anonsu beklenenden kısa üretildi")
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error",
                    "-f", "s16le", "-ar", "8000", "-ac", "1",
                    "-i", str(slin_tmp),
                    "-ar", "8000", "-ac", "1", "-c:a", "pcm_s16le",
                    "-f", "wav", "-y", str(wav_tmp),
                ],
                check=True,
            )
            _validate_wav(wav_tmp)
            completed[name] = wav_tmp

        # Üç dosya da üretildikten ve doğrulandıktan sonra birlikte etkinleşir.
        for name, wav_tmp in completed.items():
            os.replace(wav_tmp, assets / f"{name}.wav")
        print(
            "voice_prompts=ok "
            + " ".join(f"{name}={text}" for name, text in prompts.items())
        )
    finally:
        await TextToSpeechEngine.shutdown()
        await close_client()
        for path in temporary:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
