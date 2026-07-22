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
            voice_vad_energy_floor=250.0,
            voice_vad_barge_energy_floor=450.0,
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

    def test_quiet_customer_speech_starts_normal_listening(self) -> None:
        self.segmenter.vad.value = 0.80
        for _ in range(self.segmenter.start_frames):
            self.segmenter.feed(_frame(150), assistant_speaking=False)
        self.assertTrue(self.segmenter.speaking)


if __name__ == "__main__":
    unittest.main()
