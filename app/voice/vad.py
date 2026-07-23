from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
import onnxruntime as ort

from app.voice.config import get_voice_settings


class SileroVAD:
    """Silero ONNX v5 için çağrı-başına gizli durum tutan 8 kHz VAD."""

    def __init__(self) -> None:
        settings = get_voice_settings()
        model = Path(settings.voice_vad_model)
        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(
            str(model), sess_options=options, providers=["CPUExecutionProvider"]
        )
        self.state = np.zeros((2, 1, 128), dtype=np.float32)
        self.sr = np.array(8000, dtype=np.int64)

    def probability(self, pcm: bytes) -> float:
        audio = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
        if len(audio) < 256:
            audio = np.pad(audio, (0, 256 - len(audio)))
        elif len(audio) > 256:
            audio = audio[:256]
        output, self.state = self.session.run(
            None, {"input": audio[None, :], "state": self.state, "sr": self.sr}
        )
        return float(output.reshape(-1)[0])

    def reset(self) -> None:
        self.state.fill(0)


class UtteranceSegmenter:
    """32 ms karelerden konuşma başlangıç/bitiş ve pre-roll üretir."""

    frame_bytes = 512  # 256 sample, 8 kHz, signed 16-bit

    def __init__(self) -> None:
        cfg = get_voice_settings()
        self.vad = SileroVAD()
        self.start_frames = max(1, (cfg.voice_vad_start_ms + 31) // 32)
        self.barge_frames = max(1, (cfg.voice_vad_barge_ms + 31) // 32)
        self.end_frames = max(1, (cfg.voice_vad_end_silence_ms + 31) // 32)
        self.max_frames = max(1, int(cfg.voice_max_utterance_s * 1000 / 32))
        self.preroll = deque(maxlen=max(1, (cfg.voice_vad_preroll_ms + 31) // 32))
        self.start_probability = cfg.voice_vad_start_probability
        self.barge_probability = cfg.voice_vad_barge_probability
        self.energy_floor = cfg.voice_vad_energy_floor
        self.barge_energy_floor = cfg.voice_vad_barge_energy_floor
        self.energy_multiplier = cfg.voice_vad_energy_multiplier
        self.min_voice_frames = max(1, (cfg.voice_vad_min_voiced_ms + 31) // 32)
        self.noise_floor = 100.0
        self.buffer = bytearray()
        self.pending = bytearray()
        self.speech = bytearray()
        self.voice_frames = 0
        self.total_voice_frames = 0
        self.silence_frames = 0
        self.speaking = False
        self.speech_started = False
        self.speech_finished = False
        self.last_probability = 0.0
        self.last_rms = 0.0
        self.last_ac_rms = 0.0
        self.last_zero_crossing_rate = 0.0

    def feed(self, data: bytes, assistant_speaking: bool = False) -> tuple[bool, list[bytes]]:
        """(barge_in, tamamlanan_ifadeler) döndürür."""
        # Her feed çağrısı için edge-triggered olaylar. ``speaking`` seviye
        # bilgisidir; bunlar ise session coordinator'ın yalnız bir kez interrupt
        # üretmesini sağlar.
        self.speech_started = False
        self.speech_finished = False
        self.pending.extend(data)
        completed: list[bytes] = []
        barge = False
        while len(self.pending) >= self.frame_bytes:
            frame = bytes(self.pending[: self.frame_bytes])
            del self.pending[: self.frame_bytes]
            probability = self.vad.probability(frame)
            samples = np.frombuffer(frame, dtype="<i2").astype(np.float32)
            rms = float(np.sqrt(np.mean(samples * samples)))
            centered = samples - float(np.mean(samples))
            ac_rms = float(np.sqrt(np.mean(centered * centered)))
            zero_crossing_rate = float(
                np.mean(np.signbit(centered[1:]) != np.signbit(centered[:-1]))
            )
            self.last_probability = probability
            self.last_rms = rms
            self.last_ac_rms = ac_rms
            self.last_zero_crossing_rate = zero_crossing_rate
            threshold = self.barge_probability if assistant_speaking else self.start_probability
            energy_threshold = max(
                self.barge_energy_floor if assistant_speaking else self.energy_floor,
                self.noise_floor
                * (self.energy_multiplier + (1.5 if assistant_speaking else 0.0)),
            )
            if assistant_speaking:
                # AI konuşurken çevre sesi stream'i kesmesin: hem konuşma hem
                # yakınlık ve süre şartı birlikte aranır. 8 kHz telefon hattında
                # Silero bazı güçlü gerçek konuşmaları 0.00 olasılıkla kaçırıyor.
                # RTP korelasyon filtresinden geçen, DC/tone olmayan çok yakın
                # konuşmayı AC enerji ve sıfır geçişiyle ikinci güvenli yol olarak
                # kabul et.
                model_voice = probability >= threshold and rms >= energy_threshold
                strong_near_voice = (
                    ac_rms
                    >= max(
                        self.barge_energy_floor * 3.0,
                        self.noise_floor * 8.0,
                    )
                    and 0.01 <= zero_crossing_rate <= 0.55
                )
                voiced = model_voice or strong_near_voice
            else:
                # AI sustuktan sonra müşteri hiçbir cihaz kazancında kilitli
                # kalmasın. Silero konuşması düşük seviyede de dinlemeyi açar;
                # yalnız enerjiye dayanan fallback ise hat gürültüsünün her kısa
                # duraklamada yeni generation açmaması için belirgin yakın ses
                # ister.
                energy_only_threshold = max(
                    energy_threshold,
                    self.energy_floor * 4.0,
                )
                voiced = (
                    probability >= threshold and rms >= energy_threshold
                ) or rms >= energy_only_threshold
            if not self.speaking and not voiced and not assistant_speaking:
                self.noise_floor = (self.noise_floor * 0.97) + (rms * 0.03)
            if not self.speaking:
                self.preroll.append(frame)
                self.voice_frames = self.voice_frames + 1 if voiced else 0
                needed = self.barge_frames if assistant_speaking else self.start_frames
                if self.voice_frames >= needed:
                    self.speaking = True
                    self.speech_started = True
                    self.speech = bytearray().join(self.preroll)
                    self.silence_frames = 0
                    self.total_voice_frames = self.voice_frames
                    barge = assistant_speaking
            else:
                self.speech.extend(frame)
                if voiced:
                    self.silence_frames = 0
                    self.total_voice_frames += 1
                else:
                    self.silence_frames += 1
                frames = len(self.speech) // self.frame_bytes
                if self.silence_frames >= self.end_frames or frames >= self.max_frames:
                    if self.total_voice_frames >= self.min_voice_frames:
                        completed.append(bytes(self.speech))
                    self.speech_finished = True
                    self._reset_utterance()
        return barge, completed

    def _reset_utterance(self) -> None:
        self.speaking = False
        self.speech.clear()
        self.preroll.clear()
        self.voice_frames = 0
        self.total_voice_frames = 0
        self.silence_frames = 0
        self.vad.reset()
