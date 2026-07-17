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
        import pygame
        import time

        logger.info("🎙️ Dinleniyor... Araya girmek için konuşabilirsiniz.")
        time.sleep(0.5)  # Hoparlörün ilk sesini mikrofonun algılamaması için çok kısa bir süre bekle
        
        threshold = 1000  # Ses algılama eşiği

        # BARGE-IN: Asistan konuşurken biri lafa girerse veya asistan susana kadar bekle
        for _ in range(100):  
            chunk = sd.rec(int(0.1 * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
            sd.wait()
            rms = np.sqrt(np.mean(chunk.astype(np.float32)**2))
            
            if rms > threshold:
                try:
                    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        if hasattr(pygame.mixer.music, 'unload'):
                            pygame.mixer.music.unload() 
                        logger.info("🛑 Söz kesildi! Asistan susturuldu.")
                except Exception:
                    pass
                break
                
            try:
                if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
                    if hasattr(pygame.mixer.music, 'unload'):
                        pygame.mixer.music.unload()
                    break 
            except Exception:
                pass

        logger.info("🎙️ Kayıt Başladı! Lütfen %s saniye boyunca Türkçe konuşun...", duration_sec)
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
            text = recognizer.recognize_google(audio_data, language="tr-TR")  # type: ignore
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
    """Metni Voice API (veya Edge TTS) ile okur ve pygame ile ASENKRON çalar (Barge-in desteği)."""
    logger.info("🔊 Hoparlörden Okunuyor: '%s'", text)
    temp_audio = "temp_voice.wav"
    try:
        import edge_tts
        import pygame
        from app.voice.config import get_voice_settings
        import httpx

        # Eski dosya varsa kilitleri bırak ve silmeyi dene
        if pygame.mixer.get_init():
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                if hasattr(pygame.mixer.music, 'unload'):
                    pygame.mixer.music.unload()
            except Exception:
                pass
                
        if os.path.exists(temp_audio):
            try:
                os.remove(temp_audio)
            except OSError:
                pass

        settings = get_voice_settings()
        audio_generated = False

        if settings.tts_api_key and settings.tts_api_base_url:
            try:
                base_url = settings.tts_api_base_url.rstrip('/')
                auth_url = f"{base_url}/auth"
                create_url = f"{base_url}/createvoice"

                with httpx.Client(timeout=5.0) as client:
                    client.post(auth_url, json={"key": settings.tts_api_key}).raise_for_status()
                    payload = {
                        "metin": text,
                        "language": "tr",
                        "cinsiyet": settings.tts_api_gender,
                        "sestype": settings.tts_api_emotion,
                        "exaggeration": 0.5,
                        "cfg_weight": 0.5,
                        "temperature": 0.8
                    }
                    response = client.post(create_url, json=payload)
                    response.raise_for_status()
                    with open(temp_audio, "wb") as f:
                        f.write(response.content)
                audio_generated = True
            except Exception as e:
                logger.error("Voice API başarısız oldu: %s, fallback: edge-tts", e)

        if not audio_generated:
            # Fallback
            temp_audio = "temp_voice.mp3"
            if os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except OSError:
                    pass
            async def _save_mp3():
                communicate = edge_tts.Communicate(text, "tr-TR-AhmetNeural", rate="+25%")
                await communicate.save(temp_audio)
            asyncio.run(_save_mp3())

        # Pygame ile asenkron (arka planda) çalmaya başla
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(temp_audio)
        pygame.mixer.music.play()
        # NOT: Burada block etmiyoruz (beklemiyoruz). Fonksiyon hemen döner 
        # ve mikrofon dinlemeye geçer. Böylece asistan konuşurken kullanıcı araya girebilir!

    except Exception as exc:
        logger.warning("Ses çalınamadı (%s)", exc)


async def run_live_mic_test(record_duration: int = 5) -> None:
    db = get_db()
    business = await db.businesses.find_one({"business_id": "berber_mehmet_kutahya"})
    if not business:
        logger.error("Veritabanında 'berber_mehmet_kutahya' işletmesi bulunamadı! Lütfen seed çalıştırın.")
        return

    logger.info("=== GERÇEK VERİTABANI BAĞLANTISI BAŞARILI (%s) ===", business["name"])
    logger.info("📞 SESLİ RANDEVU GÖRÜŞMESİ BAŞLADI (Çıkmak için 'kapat' deyin veya Ctrl+C yapın)")

    llm = VoiceLLMEngine(business_slug="berber_mehmet_kutahya")

    # Başlangıçta sessiz beklemek yerine kullanıcıyı karşıla
    initial_greeting = "Merhaba, Berber Mehmet'e hoş geldiniz. Size nasıl yardımcı olabilirim?"
    logger.info("🤖 Asistan (İlk Karşılama) : '%s'", initial_greeting)
    await asyncio.to_thread(speak_out_loud, initial_greeting)
    
    # Sistemin hafızasına asistanın ilk mesajını ekleyelim ki bağlam oluşsun
    llm.history.append({"role": "assistant", "content": initial_greeting})

    turn_count = 0
    while True:
        turn_count += 1
        logger.info("\n================= TUR %s =================", turn_count)

        # 1. Mikrofondan konuşmanızı al ve gerçek metne dönüştür
        user_text = await asyncio.to_thread(record_real_speech, record_duration)

        if not user_text.strip():
            msg = "Sizi tam olarak duyamadım. Lütfen tekrar eder misiniz?"
            logger.info("🤖 Asistan (Duyamadı): '%s'", msg)
            await asyncio.to_thread(speak_out_loud, msg)
            continue

        logger.info("🧑 Müşteri (Siz Konuştunuz): '%s'", user_text)

        # 2. Çıkış kelimesi kontrolü
        lower_text = user_text.replace("İ", "i").replace("I", "ı").lower()
        exit_keywords = ["kapat", "iyi günler", "hoşça kal", "çıkış", "bitti", "hayır", "başka isteğim yok", "yok", "teşekkür", "sağ ol", "sağol", "görüşürüz", "kolay gelsin"]
        if any(w in lower_text for w in exit_keywords):
            bye_msg = "Bizi aradığınız için teşekkür ederiz. İyi günler dileriz."
            logger.info("🤖 Asistan (Görüşme Sonu) : '%s'", bye_msg)
            await asyncio.to_thread(speak_out_loud, bye_msg)
            
            # Sesin bitmesini bekle ki kapanmadan önce hoparlörden duyulsun
            import pygame
            while pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
            logger.info("📞 Görüşme sonlandırıldı.")
            break

        # 3. LLM / Veritabanı ile yanıt üret
        reply = await llm.generate_response(user_text)
        logger.info("🤖 Asistan (Cevap Verdi)  : '%s'", reply)

        # 4. Canlı hoparlörden oku!
        await asyncio.to_thread(speak_out_loud, reply)

        # Randevu onaylandıysa döngüden hafif bekleme yapılabilir ancak şu an loglama llm.py içinde yapılıyor.


def main() -> None:
    parser = argparse.ArgumentParser(description="Sesli Asistan Canlı Mikrofon Testi")
    parser.add_argument("--duration", "-d", type=int, default=5, help="Kayıt süresi (saniye)")
    args = parser.parse_args()

    asyncio.run(run_live_mic_test(record_duration=args.duration))


if __name__ == "__main__":
    main()
