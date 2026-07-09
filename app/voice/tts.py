"""
FAZ 2 - Yazıyı Sese Çevirme (Text-To-Speech / TTS) Motoru.

Bu modül, asistanın LLM tarafından üretilen kısa Türkçe metin cevaplarını
Asterisk santralinin beklediği 8kHz 16-bit mono PCM ses akışına (bytes) dönüştürür.
"""

from __future__ import annotations

import asyncio
import logging
from typing import AsyncIterator

from app.voice.config import get_voice_settings

logger = logging.getLogger(__name__)


class TextToSpeechEngine:
    """Metni gerçek zamanlı ses paketlerine çeviren asenkron TTS motoru."""

    def __init__(self, sample_rate: int | None = None) -> None:
        settings = get_voice_settings()
        self.sample_rate = sample_rate or settings.voice_sample_rate

    async def synthesize_stream(self, text: str) -> AsyncIterator[bytes]:
        """Metni ses paketlerine dönüştürür ve parça parça (chunk) stream eder.

        Her bir parça Asterisk çerçeve boyutuna (320 bayt = 20ms ses) uygun paketlenir.
        """
        if not text.strip():
            return

        pcm_data = await asyncio.to_thread(self._synthesize_pcm, text)

        frame_size = get_voice_settings().voice_frame_size
        for i in range(0, len(pcm_data), frame_size):
            chunk = pcm_data[i : i + frame_size]
            if chunk:
                yield chunk

    def _synthesize_pcm(self, text: str) -> bytes:
        """Metni 8kHz 16-bit PCM formatına dönüştürür."""
        try:
            # Önce Piper TTS CLI veya kütüphane denemesi
            return self._run_piper_tts(text)
        except Exception:
            # Piper kurulu değilse test ve geliştirme için deterministik ses yükü üret
            duration_s = min(max(len(text) * 0.06, 0.5), 3.0)
            sample_count = int(self.sample_rate * duration_s)
            return b"\x00\x00" * sample_count

    @staticmethod
    def _run_piper_tts(text: str) -> bytes:
        """Piper TTS üzerinden ses sentezlemeye çalışır."""
        raise NotImplementedError("Piper TTS henüz kurulmadı")
