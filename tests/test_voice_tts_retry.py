from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.voice.tts import TextToSpeechEngine


class _RetryTTS(TextToSpeechEngine):
    def __init__(self) -> None:
        self.attempts = 0

    async def _voice_api_audio(self, _text, _settings):
        if False:
            yield b""

    async def _decode_mp3(self, _source):
        self.attempts += 1
        if self.attempts == 1:
            raise OSError("empty stream")
        yield b"\x01" * 320


class VoiceTTSRetryTests(unittest.IsolatedAsyncioTestCase):
    async def test_empty_stream_retries_same_voice_provider(self) -> None:
        tts = _RetryTTS()
        with patch("app.voice.tts.get_voice_settings", return_value=SimpleNamespace()):
            chunks = [chunk async for chunk in tts.synthesize_stream("Merhaba")]
        self.assertEqual(tts.attempts, 2)
        self.assertEqual(chunks, [b"\x01" * 320])


if __name__ == "__main__":
    unittest.main()
