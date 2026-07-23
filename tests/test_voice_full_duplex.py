from __future__ import annotations

import asyncio
import contextlib
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.voice.audio_socket import AudioSocketCall, _QueuedSpeech
from app.voice.dialog import DialogManager


class _Writer:
    def write(self, _data: bytes) -> None:
        return None

    async def drain(self) -> None:
        return None

    def close(self) -> None:
        return None

    async def wait_closed(self) -> None:
        return None


class _SpeechStartSegmenter:
    def __init__(self) -> None:
        self.speech_started = False
        self.speech_finished = False
        self.speaking = False
        self.speech = bytearray()
        self.last_probability = 0.9
        self.last_rms = 900.0
        self.noise_floor = 100.0

    def feed(self, _data: bytes, _assistant_speaking: bool):
        self.speech_started = True
        self.speaking = True
        self.speech.extend(b"\x01" * 512)
        return False, []


class VoiceFullDuplexTests(unittest.IsolatedAsyncioTestCase):
    async def test_voice_start_invalidates_llm_and_stops_playback(self) -> None:
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            _Writer(),
        )
        call.segmenter = _SpeechStartSegmenter()
        call.current_turn = asyncio.create_task(asyncio.sleep(10))
        call.current_turn_generation = 0
        call.llm_cancel_event = asyncio.Event()
        call.playback = asyncio.create_task(asyncio.sleep(10))
        worker = asyncio.create_task(call._audio_worker())
        try:
            call.audio_queue.put_nowait(b"\x00" * 320)
            await asyncio.sleep(0.02)

            self.assertEqual(call.stream_generation, 1)
            self.assertTrue(call.llm_cancel_event.is_set())
            self.assertTrue(call.playback.done())
        finally:
            worker.cancel()
            call.current_turn.cancel()
            await asyncio.gather(worker, call.current_turn, return_exceptions=True)

    async def test_stale_tts_generation_never_starts(self) -> None:
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            _Writer(),
        )
        call.stream_generation = 2
        call._speak = AsyncMock()
        worker = asyncio.create_task(call._tts_worker())
        try:
            call.tts_queue.put_nowait(
                _QueuedSpeech("eski cevap", 0.0, generation=1)
            )
            await asyncio.sleep(0.02)
            call._speak.assert_not_awaited()
            self.assertIsNone(call.playback)
        finally:
            worker.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await worker

    async def test_barge_start_emits_only_one_interrupt(self) -> None:
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            _Writer(),
        )
        call.segmenter = _SpeechStartSegmenter()
        def barge_feed(_data, _assistant):
            call.segmenter.speech_started = True
            call.segmenter.speaking = True
            return True, []

        call.segmenter.feed = barge_feed
        call.playback = asyncio.create_task(asyncio.sleep(10))
        call._interrupt_response = AsyncMock()
        worker = asyncio.create_task(call._audio_worker())
        try:
            call.audio_queue.put_nowait(b"\x00" * 320)
            await asyncio.sleep(0.02)
            call._interrupt_response.assert_awaited_once()
        finally:
            worker.cancel()
            call.playback.cancel()
            await asyncio.gather(worker, call.playback, return_exceptions=True)

    async def test_tts_is_not_started_while_customer_is_speaking(self) -> None:
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            _Writer(),
        )
        call.stream_generation = 1
        call.segmenter.speaking = True
        call._speak = AsyncMock()
        worker = asyncio.create_task(call._tts_worker())
        try:
            call.tts_queue.put_nowait(
                _QueuedSpeech("kullanıcının üstüne binme", 0.0, generation=1)
            )
            await asyncio.sleep(0.02)
            call._speak.assert_not_awaited()
        finally:
            worker.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await worker

    async def test_interrupted_utterance_is_marked_for_contextual_retry(self) -> None:
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            _Writer(),
        )
        call.segmenter = _SpeechStartSegmenter()
        call.queue_mode = True
        call.playback = asyncio.create_task(asyncio.sleep(10))
        call._interrupt_response = AsyncMock()
        worker = asyncio.create_task(call._audio_worker())
        try:
            call.audio_queue.put_nowait(b"\x00" * 320)
            await asyncio.sleep(0.02)
            call.segmenter.speech_started = False
            call.segmenter.speaking = False
            call.segmenter.feed = lambda *_args: (
                False,
                [b"\x01" * 1600],
            )
            call.audio_queue.put_nowait(b"\x00" * 320)
            item = await asyncio.wait_for(call.llm_queue.get(), timeout=0.2)

            self.assertTrue(item.interrupted)
            self.assertEqual(item.generation, 1)
        finally:
            worker.cancel()
            call.playback.cancel()
            await asyncio.gather(worker, call.playback, return_exceptions=True)

    async def test_deepseek_request_is_cancelable_without_dialog_refactor(self) -> None:
        dialog = DialogManager.__new__(DialogManager)
        dialog.history = []
        dialog._llm_state = lambda: "{}"
        dialog._llm_recent_history = lambda: []
        cancel_event = asyncio.Event()
        request_started = asyncio.Event()

        async def slow_post(*_args, **_kwargs):
            request_started.set()
            await asyncio.Future()

        fake_http = SimpleNamespace(post=slow_post)
        settings = SimpleNamespace(
            deepseek_api_key="test",
            deepseek_base_url="https://example.invalid",
            deepseek_model="test",
            ai_request_timeout_s=8.0,
        )
        previous_http = DialogManager._http
        DialogManager._http = fake_http
        try:
            with patch(
                "app.voice.dialog.get_voice_settings", return_value=settings
            ):
                task = asyncio.create_task(
                    dialog._interpret("merhaba", cancel_event=cancel_event)
                )
                await request_started.wait()
                cancel_event.set()
                with self.assertRaises(asyncio.CancelledError):
                    await task
        finally:
            DialogManager._http = previous_http


if __name__ == "__main__":
    unittest.main()
