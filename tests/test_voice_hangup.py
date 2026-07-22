from __future__ import annotations

import asyncio
import tempfile
import unittest
import wave
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.voice.audio_socket import AudioSocketCall


class _Writer:
    def __init__(self) -> None:
        self.writes: list[bytes] = []
        self.closed = False

    def write(self, data: bytes) -> None:
        self.writes.append(data)

    async def drain(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        return None


class _TwoFrameTTS:
    async def synthesize_stream(self, _text: str):
        yield b"\x01" * 320
        yield b"\x02" * 320


class VoiceHangupTests(unittest.IsolatedAsyncioTestCase):
    async def test_pending_speech_queue_is_bounded_to_latest_four_parts(self) -> None:
        writer = _Writer()
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            writer,
        )
        call.current_turn = asyncio.create_task(asyncio.sleep(10))
        try:
            for index in range(7):
                call._queue_utterance(bytes([index]) * 3200)
            self.assertEqual(len(call.pending_utterances), 4)
            self.assertEqual(call.pending_utterances[0][0], 3)
            self.assertEqual(call.pending_utterances[-1][0], 6)
        finally:
            call.current_turn.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await call.current_turn

    async def test_opening_prefetch_plays_staff_prompt_after_one_greeting(self) -> None:
        writer = _Writer()
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            writer,
        )
        call.dialog = SimpleNamespace(
            closed=False,
            opening_prompt=lambda: "Berberlerimiz: Mehmet ve Yusuf.",
        )

        async def finish_locked_intro() -> None:
            self.assertEqual(call.phase, call.LOCKED_INTRO)
            call.phase = call.INTERRUPTIBLE_DIALOG

        call._play_greeting = AsyncMock(side_effect=finish_locked_intro)
        original_send = call._send_audio

        async def assert_opening_is_interruptible(chunk: bytes) -> None:
            self.assertEqual(call.phase, call.INTERRUPTIBLE_DIALOG)
            await original_send(chunk)

        call._send_audio = assert_opening_is_interruptible

        settings = SimpleNamespace(voice_opening_pcm="")
        with (
            patch("app.voice.audio_socket.TextToSpeechEngine", _TwoFrameTTS),
            patch("app.voice.audio_socket.get_voice_settings", return_value=settings),
        ):
            await call._play_opening()

        call._play_greeting.assert_awaited_once()
        self.assertEqual([frame[0] for frame in writer.writes], [0x10, 0x10])

    async def test_speech_during_stt_keeps_every_piece_in_fifo_order(self) -> None:
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            _Writer(),
        )
        call.current_turn = asyncio.create_task(asyncio.sleep(10))

        call._queue_utterance(b"first")
        call._queue_utterance(b"latest")

        self.assertEqual(list(call.pending_utterances), [b"first", b"latest"])
        self.assertEqual(call.turn_revision, 0)
        call.terminating = True
        call.phase = call.TERMINATING
        task = call.current_turn
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task

    async def test_ready_wav_greeting_stays_non_interruptible_until_complete(self) -> None:
        writer = _Writer()
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            writer,
        )
        call.phase = call.LOCKED_INTRO

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "greeting.wav"
            with wave.open(str(path), "wb") as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(8000)
                audio.writeframes(b"\x01\x00" * 320)

            settings = SimpleNamespace(voice_greeting_pcm=str(path))
            original_send = call._send_audio

            async def assert_greeting_active(chunk: bytes) -> None:
                self.assertEqual(call.phase, call.LOCKED_INTRO)
                await original_send(chunk)

            call._send_audio = assert_greeting_active
            with patch("app.voice.audio_socket.get_voice_settings", return_value=settings):
                await call._play_greeting()

        self.assertEqual(call.phase, call.INTERRUPTIBLE_DIALOG)
        self.assertEqual([frame[0] for frame in writer.writes], [0x10, 0x10])

    async def test_booking_success_wav_finishes_before_audiosocket_hangup(self) -> None:
        writer = _Writer()
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            writer,
        )
        call.dialog = SimpleNamespace(closed=True, completion_kind="booking_success")
        call.phase = call.TERMINATING

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "booking_success.wav"
            with wave.open(str(path), "wb") as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(8000)
                audio.writeframes(b"\x01\x00" * 320)
            settings = SimpleNamespace(voice_booking_success_pcm=str(path))
            with patch(
                "app.voice.audio_socket.get_voice_settings", return_value=settings
            ):
                await call._play_booking_success()

        self.assertEqual([frame[0] for frame in writer.writes], [0x10, 0x10, 0x00])
        self.assertTrue(writer.closed)
        self.assertEqual(call.result, "assistant_hangup")

    async def test_audiosocket_terminate_is_after_all_final_tts_frames(self) -> None:
        writer = _Writer()
        call = AudioSocketCall(
            "00000000-0000-0000-0000-000000000001",
            asyncio.StreamReader(),
            writer,
        )
        call.dialog = SimpleNamespace(closed=True)

        with patch("app.voice.audio_socket.TextToSpeechEngine", _TwoFrameTTS):
            await call._speak("İyi günler.", asyncio.get_running_loop().time())

        packet_types = [frame[0] for frame in writer.writes]
        self.assertEqual(packet_types, [0x10, 0x10, 0x00])
        self.assertTrue(writer.closed)
        self.assertEqual(call.result, "assistant_hangup")

if __name__ == "__main__":
    unittest.main()
