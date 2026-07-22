from __future__ import annotations

import asyncio
import unittest
from types import SimpleNamespace

from app.voice.models import SessionState, VoiceSession
from app.voice.pipeline import VoicePipeline, _HANGUP_SENTINEL
from app.voice.stt import Transcript


class _FakeTTS:
    async def synthesize_stream(self, text: str):
        self.last_text = text
        yield b"\0" * 320


class VoicePipelineDirectHangupTests(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def _stt_pipeline(transcript: Transcript) -> VoicePipeline:
        class _FakeSTT:
            async def transcribe(self, _pcm: bytes, **kwargs):
                self.domain_prompt = kwargs.get("domain_prompt")
                return transcript

        pipeline = VoicePipeline.__new__(VoicePipeline)
        pipeline.session = VoiceSession(session_id="test-stt")
        pipeline.llm = SimpleNamespace(is_session_closed=False)
        pipeline.stt = _FakeSTT()
        pipeline.llm_queue = asyncio.Queue()
        pipeline.tts_queue = asyncio.Queue()
        pipeline.interrupt_event = asyncio.Event()
        pipeline._interrupt_generation = 0
        pipeline._stt_domain_prompt = "Beklenen kelimeler: Yusuf, Saç Kesimi"
        pipeline._stt_context_task = None
        return pipeline

    async def test_low_confidence_stt_never_reaches_llm(self) -> None:
        pipeline = self._stt_pipeline(
            Transcript("Tak haltırışı takım", 0.20, "large-v3-turbo")
        )

        await pipeline._process_stt(b"\0" * 8000)

        self.assertTrue(pipeline.llm_queue.empty())
        self.assertIn("net anlayamadım", await pipeline.tts_queue.get())

    async def test_stt_receives_booking_catalog_context(self) -> None:
        pipeline = self._stt_pipeline(
            Transcript("Yusuf saç kesimi", 0.80, "large-v3-turbo")
        )

        await pipeline._process_stt(b"\0" * 8000)

        self.assertEqual(await pipeline.llm_queue.get(), "Yusuf saç kesimi")
        self.assertIn("Yusuf", pipeline.stt.domain_prompt)

    async def test_final_tts_completes_before_direct_sip_hangup(self) -> None:
        pipeline = VoicePipeline.__new__(VoicePipeline)
        pipeline.session = VoiceSession(
            session_id="test-call",
            caller_number="+905000000000",
            business_slug="test-business",
        )
        pipeline.llm = SimpleNamespace(is_session_closed=True)
        pipeline.tts = _FakeTTS()
        pipeline.tts_queue = asyncio.Queue()
        pipeline.interrupt_event = asyncio.Event()
        pipeline._interrupt_generation = 0
        pipeline._hangup_started = False
        pipeline._is_running = True

        events: list[str] = []

        async def send_audio(_chunk: bytes) -> None:
            events.append("audio")

        async def hangup() -> None:
            events.append("hangup")
            pipeline._is_running = False

        pipeline.send_audio_cb = send_audio
        pipeline.on_hangup = hangup
        await pipeline.tts_queue.put("İyi günler.")
        await pipeline.tts_queue.put(_HANGUP_SENTINEL)

        await asyncio.wait_for(pipeline._tts_worker(), timeout=2)

        self.assertEqual(events, ["audio", "hangup"])
        self.assertEqual(pipeline.session.state, SessionState.CLOSED)

    async def test_direct_sip_hangup_is_idempotent(self) -> None:
        pipeline = VoicePipeline.__new__(VoicePipeline)
        pipeline.session = VoiceSession(session_id="test-call")
        pipeline._hangup_started = False
        calls = 0

        async def hangup() -> None:
            nonlocal calls
            calls += 1

        pipeline.on_hangup = hangup
        await pipeline._finish_assistant_hangup()
        await pipeline._finish_assistant_hangup()

        self.assertEqual(calls, 1)


if __name__ == "__main__":
    unittest.main()
