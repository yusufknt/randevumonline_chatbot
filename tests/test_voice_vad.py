from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from app.voice.vad import UtteranceSegmenter


class _FakeVAD:
    def __init__(self) -> None:
        self.value = 0.0

    def probability(self, _pcm: bytes) -> float:
        return self.value

    def reset(self) -> None:
        return None


def _frame(amplitude: int) -> bytes:
    return np.full(256, amplitude, dtype="<i2").tobytes()


def _speech_like_frame(amplitude: int) -> bytes:
    samples = np.arange(256, dtype=np.float32)
    wave = np.sin(2 * np.pi * 180 * samples / 8000) * amplitude
    return wave.astype("<i2").tobytes()


class VoiceVADTests(unittest.TestCase):
    def setUp(self) -> None:
        settings = SimpleNamespace(
            voice_vad_start_ms=64,
            voice_vad_barge_ms=128,
            voice_vad_end_silence_ms=576,
            voice_max_utterance_s=12.0,
            voice_vad_preroll_ms=256,
            voice_vad_start_probability=0.50,
            voice_vad_barge_probability=0.60,
            voice_vad_energy_floor=350.0,
            voice_vad_barge_energy_floor=700.0,
            voice_vad_energy_multiplier=3.0,
            voice_vad_min_voiced_ms=192,
        )
        with (
            patch("app.voice.vad.get_voice_settings", return_value=settings),
            patch("app.voice.vad.SileroVAD", _FakeVAD),
        ):
            self.segmenter = UtteranceSegmenter()

    def test_loud_non_speech_does_not_stop_stream(self) -> None:
        self.segmenter.vad.value = 0.10
        stopped = any(
            self.segmenter.feed(_frame(5000), assistant_speaking=True)[0]
            for _ in range(self.segmenter.barge_frames + 2)
        )
        self.assertFalse(stopped)

    def test_distant_background_speech_does_not_stop_stream(self) -> None:
        self.segmenter.vad.value = 0.90
        stopped = any(
            self.segmenter.feed(_frame(300), assistant_speaking=True)[0]
            for _ in range(self.segmenter.barge_frames + 2)
        )
        self.assertFalse(stopped)

    def test_near_sustained_speech_stops_stream(self) -> None:
        self.segmenter.vad.value = 0.80
        results = [
            self.segmenter.feed(_frame(900), assistant_speaking=True)[0]
            for _ in range(self.segmenter.barge_frames)
        ]
        self.assertFalse(any(results[:-1]))
        self.assertTrue(results[-1])

    def test_strong_phone_speech_can_barge_when_silero_is_low(self) -> None:
        self.segmenter.vad.value = 0.10
        results = [
            self.segmenter.feed(
                _speech_like_frame(3200),
                assistant_speaking=True,
            )[0]
            for _ in range(self.segmenter.barge_frames)
        ]
        self.assertFalse(any(results[:-1]))
        self.assertTrue(results[-1])

    def test_barge_in_keeps_listening_until_customer_finishes(self) -> None:
        self.segmenter.vad.value = 0.80
        for _ in range(self.segmenter.barge_frames):
            barge, completed = self.segmenter.feed(
                _frame(900), assistant_speaking=True
            )
        self.assertTrue(barge)
        self.assertFalse(completed)

        for _ in range(self.segmenter.min_voice_frames):
            self.segmenter.feed(_frame(900), assistant_speaking=False)
        self.segmenter.vad.value = 0.0
        completed = []
        for _ in range(self.segmenter.end_frames):
            _, completed = self.segmenter.feed(
                _frame(0), assistant_speaking=False
            )

        self.assertEqual(len(completed), 1)
        self.assertGreater(len(completed[0]), 0)

    def test_distant_quiet_speech_does_not_start_normal_listening(self) -> None:
        self.segmenter.vad.value = 0.80
        for _ in range(self.segmenter.start_frames):
            self.segmenter.feed(_frame(150), assistant_speaking=False)
        self.assertFalse(self.segmenter.speaking)

    def test_near_customer_speech_starts_normal_listening(self) -> None:
        self.segmenter.vad.value = 0.80
        for _ in range(self.segmenter.start_frames):
            self.segmenter.feed(_frame(600), assistant_speaking=False)
        self.assertTrue(self.segmenter.speaking)

    def test_low_energy_line_noise_does_not_open_a_new_turn(self) -> None:
        self.segmenter.vad.value = 0.0
        for _ in range(self.segmenter.start_frames + 4):
            self.segmenter.feed(_frame(450), assistant_speaking=False)
        self.assertFalse(self.segmenter.speaking)
        self.assertFalse(self.segmenter.speech_started)


if __name__ == "__main__":
    unittest.main()
