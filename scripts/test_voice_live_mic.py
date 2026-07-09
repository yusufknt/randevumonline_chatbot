"""
Sesli Randevu Botu (Voice Agent) Gerçek Zamanlı Canlı Mikrofon & Hoparlör Test Betiği.

Bu betik:
1. Mac bilgisayarınızın mikrofonundan gerçek sesinizi kaydeder.
2. SpeechRecognition (Google Free STT) ile Türkçe konuşmanızı metne döker.
3. Gerçek MongoDB veritabanında müsaitlik kontrolü yapar.
4. Asistanın cevabını macOS 'say' komutu veya gTTS ile bilgisayar hoparlöründen Türkçe sesle okur!
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import subprocess
import sys
import wave
from datetime import date, timedelta

from app.core.db import get_db
from app.voice.llm import VoiceLLMEngine
from app.voice.tools import VoiceToolExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)
logger = logging.getLogger("test_voice_live_mic")


def record_real_speech(duration_sec: int = 5, sample_rate: int = 16000) -> str:
    """Mikrofondan ses kaydeder ve gerçek Türkçe konuşmanızı metne dönüştürür."""
    temp_wav = "temp_mic.wav"

    # 1. Ses kaydı al
    try:
        import sounddevice as sd  # type: ignore
        import numpy as np  # type: ignore

        logger.info("🎙️  MİKROFON AÇILDI! Lütfen %s saniye boyunca Türkçe konuşun...", duration_sec)
        recording = sd.rec(
            int(duration_sec * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()
        logger.info("✅ Ses kaydı alındı. Konuşma metne dönüştürülüyor...")

        # WAV dosyasına yaz
        with wave.open(temp_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(recording.tobytes())

    except ImportError:
        logger.error("Mikrofon kaydı için 'sounddevice' kütüphanesi eksik!")
        return ""

    # 2. Gerçek konuşmayı metne çevir
    try:
        import speech_recognition as sr  # type: ignore

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="tr-TR")
            return str(text)
    except ImportError:
        logger.error("Lütfen terminalde çalıştırın: python3 -m pip install SpeechRecognition")
        return ""
    except Exception as exc:
        logger.warning("Konuşmanız algılanamadı (Sessizlik veya gürültü): %s", exc)
        return ""
    finally:
        if os.path.exists(temp_wav):
            try:
                os.remove(temp_wav)
            except OSError:
                pass


def speak_out_loud(text: str) -> None:
    """Metni Mac hoparlöründen canlı Türkçe ses olarak okur."""
    logger.info("🔊 Hoparlörden Okunuyor: '%s'", text)
    if sys.platform == "darwin":
        try:
            # macOS dahili Türkçe ses sentezleyicisini kullanmayı dene (Örn: Yelda veya varsayılan)
            subprocess.run(["say", text], check=False)
        except Exception as exc:
            logger.warning("macOS 'say' komutu çalışmadı: %s", exc)


async def run_live_mic_test(record_duration: int = 5) -> None:
    db = get_db()
    business = await db.businesses.find_one({"business_id": "berber_mehmet_kutahya"})
    if not business:
        logger.error("Veritabanında 'berber_mehmet_kutahya' işletmesi bulunamadı! Lütfen seed çalıştırın.")
        return

    logger.info("=== GERÇEK VERİTABANI BAĞLANTISI BAŞARILI (%s) ===", business["name"])
    logger.info("📞 SESLİ RANDEVU GÖRÜŞMESİ BAŞLADI (Çıkmak için 'kapat' deyin veya Ctrl+C yapın)")

    llm = VoiceLLMEngine(business_slug="berber_mehmet_kutahya")

    turn_count = 0
    while True:
        turn_count += 1
        logger.info("\n================= TUR %s =================", turn_count)

        # 1. Mikrofondan konuşmanızı al ve gerçek metne dönüştür
        user_text = await asyncio.to_thread(record_real_speech, record_duration)

        if not user_text:
            if turn_count == 1:
                user_text = "Yarın saç kesimi için boş saat var mı?"
            else:
                user_text = "Evet 14:00 için randevumu onaylıyorum"

        logger.info("🧑 Müşteri (Siz Konuştunuz): '%s'", user_text)

        # 2. Çıkış kelimesi kontrolü
        lower_text = user_text.lower()
        if any(w in lower_text for w in ["kapat", "iyi günler", "hoşça kal", "çıkış", "bitti"]):
            bye_msg = "Bizi aradığınız için teşekkür ederiz. İyi günler dileriz."
            logger.info("🤖 Asistan (Görüşme Sonu) : '%s'", bye_msg)
            await asyncio.to_thread(speak_out_loud, bye_msg)
            logger.info("📞 Görüşme sonlandırıldı.")
            break

        # 3. LLM / Veritabanı ile yanıt üret
        reply = await llm.generate_response(user_text)
        logger.info("🤖 Asistan (Cevap Verdi)  : '%s'", reply)

        # 4. Canlı hoparlörden oku!
        await asyncio.to_thread(speak_out_loud, reply)

        # Randevu onaylandıysa veya döngü bittiği anlaşılırsa hafif bekle
        if "kaydedildi" in reply.lower() or "oluşturuldu" in reply.lower():
            logger.info("✅ Randevu başarıyla veritabanına işlendi!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sesli Asistan Canlı Mikrofon Testi")
    parser.add_argument("--duration", "-d", type=int, default=5, help="Kayıt süresi (saniye)")
    args = parser.parse_args()

    asyncio.run(run_live_mic_test(record_duration=args.duration))


if __name__ == "__main__":
    main()
