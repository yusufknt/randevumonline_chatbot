from __future__ import annotations

import asyncio
import os
import subprocess
from pathlib import Path

from app.voice.tts import TextToSpeechEngine


async def greeting_text() -> str:
    # Yalnızca kesilemez giriş cümlesi hazır dosyaya alınır. Personel ve hizmet
    # listeleri canlı TTS'te kalır; böylece kullanıcı seçimini söyleyince kesilir.
    return "Merhaba. Randevum Online sistemine hoş geldiniz."


async def main() -> None:
    assets = Path(__file__).resolve().parent / "app" / "voice" / "assets"
    pcm_path = assets / "greeting.slin"
    pcm_tmp = assets / ".greeting.slin.tmp"
    wav_path = assets / "greeting.wav"
    wav_tmp = assets / ".greeting.wav.tmp"
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
                "-ar", "8000", "-ac", "1", "-c:a", "pcm_s16le",
                "-f", "wav", "-y", str(wav_tmp),
            ],
            check=True,
        )
        os.replace(wav_tmp, wav_path)

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
        pcm_tmp.unlink(missing_ok=True)
        wav_tmp.unlink(missing_ok=True)
        alaw_tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    from generate_voice_prompts import main as generate_all_voice_prompts

    asyncio.run(generate_all_voice_prompts())
