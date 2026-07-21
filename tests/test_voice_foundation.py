from __future__ import annotations

import asyncio
import struct
import unittest

from app.voice.audio_socket import encode_frame, read_frame
from app.voice.identity import normalize_phone
from app.voice.stt import (
    Transcript,
    _looks_like_hallucination,
    choose_transcript,
)


class VoiceFoundationTests(unittest.IsolatedAsyncioTestCase):
    def test_normalize_phone(self) -> None:
        self.assertEqual(normalize_phone("sip:05321112233@example"), "+905321112233")
        self.assertEqual(normalize_phone("00905321112233"), "+905321112233")
        self.assertEqual(normalize_phone(None), "")

    def test_repetitive_stt_hallucination_is_rejected(self) -> None:
        self.assertTrue(
            _looks_like_hallucination("İdris, " * 40, audio_seconds=0.6)
        )
        self.assertFalse(
            _looks_like_hallucination(
                "Haftaya çarşamba günü randevu istiyorum", audio_seconds=2.0
            )
        )
        self.assertTrue(_looks_like_hallucination("Altyazı M.K.", 1.2))

    def test_context_can_keep_better_fast_transcript(self) -> None:
        fast = Transcript("Saç kesimi", 0.26, "small", 0.1)
        accurate = Transcript("Başka bir şey", 0.40, "large-v3-turbo", 0.1)
        chosen = choose_transcript(
            fast, accurate, "Beklenen hizmet adı: Saç Kesimi, Sakal Tıraşı."
        )
        self.assertEqual(chosen.model, "small")

    async def test_audiosocket_fragmented_frame(self) -> None:
        reader = asyncio.StreamReader()
        frame = encode_frame(0x10, b"sample")
        reader.feed_data(frame[:2])
        reader.feed_data(frame[2:5])
        reader.feed_data(frame[5:])
        packet_type, payload = await read_frame(reader)
        self.assertEqual(packet_type, 0x10)
        self.assertEqual(payload, b"sample")

    async def test_audiosocket_coalesced_frames(self) -> None:
        reader = asyncio.StreamReader()
        reader.feed_data(encode_frame(0x03, b"5") + encode_frame(0x00))
        first = await read_frame(reader)
        second = await read_frame(reader)
        self.assertEqual(first, (0x03, b"5"))
        self.assertEqual(second, (0x00, b""))
