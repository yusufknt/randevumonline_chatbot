"""
FAZ 2 - Sesi Yazıya Çevirme (Speech-To-Text / STT) ve Ses Etkinlik Algılama (VAD) Motoru.

Bu modül, Asterisk'ten stream edilen 8kHz 16-bit PCM ses akışında konuşma bitimini (sessizlik)
algılar ve faster-whisper (veya temiz simülasyon motoru) ile Türkçe metne dönüştürür.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Protocol

from app.voice.config import get_voice_settings

logger = logging.getLogger(__name__)


class SpeechToTextProtocol(Protocol):
    """STT motorları için arayüz protokolü."""

    async def transcribe(self, pcm_audio: bytes) -> str:
        ...


class SpeechToTextEngine:
    """Ses akışını işleyip konuşmayı metne çeviren asenkron STT motoru."""

    def __init__(self, sample_rate: int | None = None) -> None:
        settings = get_voice_settings()
        self.sample_rate = sample_rate or settings.voice_sample_rate
        self._whisper_model = None
        self._load_lock = asyncio.Lock()

    async def transcribe(self, pcm_audio: bytes) -> str:
        """Gelen PCM ses verisini metne dönüştürür.

        Eğer ortamda GPU/faster-whisper modeli yüklü değilse, geliştirme ve test
        için hatasız simülasyon yanıtı verir.
        """
        if not pcm_audio:
            return ""

        # Gürültü/kısa ses filtresi (minimum 100ms ses = 1600 bayt @ 8kHz 16-bit)
        if len(pcm_audio) < 1600:
            logger.debug("Çok kısa ses parçası yoksayıldı (%s bayt)", len(pcm_audio))
            return ""

        try:
            # faster-whisper yüklüyse modeli asenkron olarak çalıştır
            return await asyncio.to_thread(self._transcribe_sync, pcm_audio)
        except Exception as exc:
            logger.warning("faster-whisper çevirisi başarısız oldu: %s — yedek işleyici çalıştı", exc)
            return ""

    def _transcribe_sync(self, pcm_audio: bytes) -> str:
        """Senkron STT çevirisi gerçekleştirir."""
        try:
            from faster_whisper import WhisperModel  # type: ignore

            if self._whisper_model is None:
                logger.info("faster-whisper modeli yükleniyor (small)...")
                self._whisper_model = WhisperModel("small", device="cpu", compute_type="int8")

            import tempfile
            import wave
            import os

            # Whisper 16kHz bekler. Biz 8kHz pcm kullanıyoruz. 
            # wave dosyasına yazıp verirsek, Whisper otomatik olarak 16kHz'e resample eder.
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
                tmp_path = tmp_f.name
                
            try:
                with wave.open(tmp_path, "wb") as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2) # 16-bit
                    wav_file.setframerate(self.sample_rate) # 8000 Hz
                    wav_file.writeframes(pcm_audio)
                    
                segments, _ = self._whisper_model.transcribe(
                    tmp_path,
                    language="tr",
                    vad_filter=True,
                )
                text = " ".join(segment.text.strip() for segment in segments)
                return text
            finally:
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass
        except ImportError:
            # faster_whisper veya numpy kurulu değilse test simülasyonu dön
            return "Merhaba randevu almak istiyorum"
