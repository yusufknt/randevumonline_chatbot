from __future__ import annotations

import unittest

import numpy as np

from app.voice.stt import SpeechToTextEngine


class VoiceSTTPreprocessTests(unittest.TestCase):
    def test_trims_long_phone_silence_but_keeps_speech_and_padding(self) -> None:
        silence = np.zeros(4000, dtype="<i2")
        speech = np.full(4000, 3000, dtype="<i2")
        pcm = np.concatenate((silence, speech, silence)).tobytes()

        audio = SpeechToTextEngine._to_16k(pcm)

        # Ham 1.5 saniye ses 16 kHz'de 24.000 örnek olurdu. Sessizlik kırpılır,
        # ancak konuşma ve iki taraftaki 120 ms Whisper dolgusu korunur.
        self.assertLess(len(audio), 16000)
        self.assertGreater(len(audio), 8000)
        self.assertGreater(float(np.max(np.abs(audio))), 0.01)


if __name__ == "__main__":
    unittest.main()
