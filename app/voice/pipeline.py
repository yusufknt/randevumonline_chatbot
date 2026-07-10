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
        """Gelen ses paketini alır, gerekirse barge-in kesmesi yapar ve akışı yürütür."""
        if not pcm_audio:
            return

        # 1. BARGE-IN KONTROLÜ: Eğer asistan konuşurken müşteri konuşmaya başlarsa TTS görevini kes
        if self.session.state == SessionState.SPEAKING and self._tts_task and not self._tts_task.done():
            logger.info("[Barge-in] Müşteri araya girdi, asistan susuyor: session_id=%s", self.session.session_id)
            self._tts_task.cancel()
            self.session.update_state(SessionState.LISTENING)

        self.session.update_state(SessionState.LISTENING)

        # 2. STT: Konuşmayı metne dök
        transcribed_text = await self.stt.transcribe(pcm_audio)
        if not transcribed_text:
            return

        logger.info("Müşteri konuştu: '%s' (session_id=%s)", transcribed_text, self.session.session_id)
        self.session.update_state(SessionState.PROCESSING)

        # 3. LLM: Cevap üret
        assistant_reply = await self.llm.generate_response(transcribed_text)
        logger.info("Asistan cevabı: '%s' (session_id=%s)", assistant_reply, self.session.session_id)

        # 4. TTS: Sese çevir ve gönder
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
                self.session.total_audio_frames_sent += 1
            self.session.update_state(SessionState.LISTENING)
        except asyncio.CancelledError:
            logger.debug("TTS yayını iptal edildi (Barge-in tetiklendi)")
            raise
