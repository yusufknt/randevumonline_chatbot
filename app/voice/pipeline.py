"""
FAZ 4 - Sesli Asistan Orkestrasyonu, Akış Yönetimi ve Söz Kesme (Barge-In).

Bu modül STT -> LLM -> TTS bileşenlerini uçtan uca bağlar ve asistan konuşurken
müşterinin araya girmesi durumunda (barge-in) TTS ses akışını anında keser.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Coroutine

from app.voice.llm import VoiceLLMEngine
from app.voice.models import SessionState, VoiceSession
from app.voice.stt import SpeechToTextEngine
from app.voice.tts import TextToSpeechEngine

logger = logging.getLogger(__name__)


class VoicePipeline:
    """Ses oturumu için uçtan uca STT -> LLM -> TTS akış yöneticisi."""

    def __init__(self, session: VoiceSession) -> None:
        self.session = session
        self.stt = SpeechToTextEngine()
        self.llm = VoiceLLMEngine(business_slug=session.business_slug or "berber_mehmet_kutahya")
        self.tts = TextToSpeechEngine()
        self._tts_task: asyncio.Task | None = None
    async def handle_incoming_audio(
        self,
        pcm_audio: bytes,
        send_audio_cb: Callable[[bytes], Coroutine[Any, Any, None]],
    ) -> None:
        """Gelen ses paketini alır ve akışı yürütür."""
        if not pcm_audio:
            return

        self.session.update_state(SessionState.LISTENING)

        # 2. STT: Konuşmayı metne dök
        try:
            transcribed_text = await self.stt.transcribe(pcm_audio)
        except Exception as e:
            logger.error("❌ STT Hatası (Sistem Çökmeyecek): %s (session_id=%s)", str(e), self.session.session_id)
            transcribed_text = ""

        if not transcribed_text:
            return

        logger.info("✅ STT tamamlandı. Müşteri konuştu: '%s' (session_id=%s)", transcribed_text, self.session.session_id)
        self.session.update_state(SessionState.PROCESSING)

        # 3. LLM: Cevap üret
        logger.info("⏳ LLM'e istek gönderiliyor...")
        try:
            assistant_reply = await asyncio.wait_for(
                self.llm.generate_response(transcribed_text), 
                timeout=20.0
            )
            logger.info("🧠 LLM cevabı üretildi: '%s' (session_id=%s)", assistant_reply, self.session.session_id)
        except asyncio.TimeoutError:
            logger.warning("⚠️ LLM Timeout Hatası (session_id=%s). Fallback cevap gönderilecek.", self.session.session_id)
            assistant_reply = "Sistemde geçici bir yoğunluk var, lütfen biraz bekleyip tekrar söyleyebilir misiniz?"
        except Exception as e:
            logger.error("❌ LLM Hatası: %s (session_id=%s)", str(e), self.session.session_id)
            assistant_reply = "Bir hata oluştu, lütfen daha sonra tekrar deneyin."

        # 4. TTS: Sese çevir ve gönder
        logger.info("🗣️ TTS üretiliyor ve ses geri gönderiliyor...")
        self.session.update_state(SessionState.SPEAKING)
        self._tts_task = asyncio.create_task(self._stream_tts(assistant_reply, send_audio_cb))

    async def _stream_tts(
        self,
        text: str,
        send_audio_cb: Callable[[bytes], Coroutine[Any, Any, None]],
    ) -> None:
        """TTS ses parçalarını istemciye stream eder."""
        try:
            async for chunk in self.tts.synthesize_stream(text):
                await send_audio_cb(chunk)
                chunk_duration = len(chunk) / 8000.0
                await asyncio.sleep(chunk_duration)
                self.session.total_audio_frames_sent += 1
            logger.info("✅ TTS ses parçaları başarıyla müşteriye iletildi. (session_id=%s)", self.session.session_id)
            self.session.update_state(SessionState.LISTENING)
            
            # Eğer [KAPAT] etiketi alınmışsa çağrıyı sonlandır
            if hasattr(self.llm, "is_session_closed") and self.llm.is_session_closed:
                logger.info("📞 Görüşme tamamlandı, çağrı sonlandırılıyor (Session CLOSED).")
                self.session.update_state(SessionState.CLOSED)
                if hasattr(self, 'on_hangup') and self.on_hangup:
                    self.on_hangup()

        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error("❌ TTS Hatası: %s (session_id=%s)", str(e), self.session.session_id)
            self.session.update_state(SessionState.LISTENING)
