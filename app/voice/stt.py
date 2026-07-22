from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass

import numpy as np
import soxr
from faster_whisper import WhisperModel
from rapidfuzz import fuzz

from app.voice.config import get_voice_settings

log = logging.getLogger(__name__)


@dataclass(slots=True)
class Transcript:
    text: str
    confidence: float
    model: str
    no_speech_probability: float = 1.0
    compression_ratio: float = 0.0


def _looks_like_hallucination(text: str, audio_seconds: float) -> bool:
    """Telefon gürültüsünden üretilen tekrarlı Whisper metinlerini reddeder."""
    turkish_lower = text.replace("İ", "i").replace("I", "ı").casefold()
    words = re.findall(r"\w+", turkish_lower, flags=re.UNICODE)
    if not words:
        return False
    normalized = " ".join(words)
    # Whisper'ın sessizlik ve telefon müziğinde sık ürettiği altyazı kalıpları.
    if any(
        phrase in normalized
        for phrase in (
            "altyazı", "izlediğiniz için teşekkür", "abone olmayı unutmayın",
            "çeviri m k", "sesli betimleme",
        )
    ):
        return True
    if len(words) >= 8:
        unique_ratio = len(set(words)) / len(words)
        most_repeated = max(words.count(word) for word in set(words))
        if unique_ratio < 0.35 or most_repeated >= 5:
            return True
    # Bir saniyeden kısa sesten paragraf çıkması gerçek konuşma değildir.
    return audio_seconds < 1.0 and len(text) > 80


def _domain_terms(domain_prompt: str | None) -> list[str]:
    if not domain_prompt:
        return []
    value = domain_prompt.split(":", 1)[-1]
    return [
        term.strip(" .")
        for term in re.split(r",|\s+veya\s+|\s+ve\s+", value, flags=re.IGNORECASE)
        if len(term.strip(" .")) >= 2
    ]


def transcript_quality(transcript: Transcript, domain_prompt: str | None) -> float:
    """Güven, sessizlik ve beklenen sözcüklerle STT adayını puanlar."""
    if not transcript.text:
        return -1.0
    score = transcript.confidence - (transcript.no_speech_probability * 0.15)
    terms = _domain_terms(domain_prompt)
    if terms:
        transcript_text = transcript.text.replace("İ", "i").replace("I", "ı").casefold()
        normalized_terms = [
            term.replace("İ", "i").replace("I", "ı").casefold()
            for term in terms
        ]
        relevance = max(
            fuzz.partial_ratio(term, transcript_text)
            for term in normalized_terms
        ) / 100.0
        exact = any(
            re.search(rf"(?<!\w){re.escape(term)}(?!\w)", transcript_text)
            for term in normalized_terms
        )
        score += relevance * 0.15
        if exact:
            score += 0.45
    return score


def choose_transcript(
    fast: Transcript, accurate: Transcript, domain_prompt: str | None
) -> Transcript:
    """Büyük modelin halüsinasyonunun iyi hızlı sonucu ezmesini engeller."""
    return (
        accurate
        if transcript_quality(accurate, domain_prompt)
        > transcript_quality(fast, domain_prompt)
        else fast
    )


class SpeechToTextEngine:
    """Bir kez ısınan, tüm çağrıların paylaştığı CPU-int8 Whisper motoru."""

    _fast: WhisperModel | None = None
    _accurate: WhisperModel | None = None
    _load_lock = asyncio.Lock()
    _fast_sem: asyncio.Semaphore | None = None
    _accurate_sem: asyncio.Semaphore | None = None

    def __init__(self) -> None:
        cfg = get_voice_settings()
        if self.__class__._fast_sem is None:
            self.__class__._fast_sem = asyncio.Semaphore(cfg.voice_stt_fast_workers)
            self.__class__._accurate_sem = asyncio.Semaphore(cfg.voice_stt_accurate_workers)

    async def warmup(self) -> None:
        await self._ensure_models()
        cfg = get_voice_settings()
        silence = np.zeros(1600, dtype=np.float32)
        await asyncio.to_thread(
            self._run, self._fast, silence, cfg.voice_stt_fast_model, None
        )

    async def _ensure_models(self) -> None:
        async with self._load_lock:
            cfg = get_voice_settings()
            if self.__class__._fast is None:
                log.info("Yerel hızlı STT modeli yükleniyor model=%s", cfg.voice_stt_fast_model)
                self.__class__._fast = await asyncio.to_thread(
                    WhisperModel,
                    cfg.voice_stt_fast_model,
                    device="cpu",
                    compute_type="int8",
                    cpu_threads=3,
                    num_workers=1,
                    local_files_only=True,
                )
            if self.__class__._accurate is None:
                if cfg.voice_stt_accurate_model == cfg.voice_stt_fast_model:
                    self.__class__._accurate = self.__class__._fast
                else:
                    log.info(
                        "Yerel doğrulama STT modeli yükleniyor model=%s",
                        cfg.voice_stt_accurate_model,
                    )
                    self.__class__._accurate = await asyncio.to_thread(
                        WhisperModel,
                        cfg.voice_stt_accurate_model,
                        device="cpu",
                        compute_type="int8",
                        cpu_threads=4,
                        num_workers=1,
                        local_files_only=True,
                    )

    @staticmethod
    def _to_16k(pcm: bytes) -> np.ndarray:
        samples = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
        # Segmenter konuşma sonunu anlayabilmek için yaklaşık 576 ms sessizliği
        # de ifadeye ekler. Özellikle tek kelimelik personel/saat cevaplarında bu
        # sessizlik sesin büyük bölümünü kaplayıp Whisper sonucunu bozabiliyor.
        # Yalnız belirgin konuşma enerjisi varsa baş/son sessizliği 120 ms payla
        # kırp; çok kısık kayıtta güvenli biçimde ham sesi koru.
        frame_samples = 80  # 10 ms @ 8 kHz
        if len(samples) >= frame_samples * 10:
            usable = len(samples) - (len(samples) % frame_samples)
            frames = samples[:usable].reshape(-1, frame_samples)
            frame_rms = np.sqrt(np.mean(frames * frames, axis=1))
            reference = float(np.percentile(frame_rms, 90))
            if reference >= 0.003:
                active = np.flatnonzero(frame_rms >= max(0.002, reference * 0.12))
                if active.size:
                    margin_frames = 12
                    start = max(0, int(active[0]) - margin_frames) * frame_samples
                    end = min(
                        len(frame_rms), int(active[-1]) + margin_frames + 1
                    ) * frame_samples
                    samples = samples[start:end]
        audio = soxr.resample(samples, 8000, 16000, quality="HQ").astype(np.float32)
        if not len(audio):
            return audio

        # Telefon hatlarında görülen DC kaymasını kaldır ve çok kısık konuşmayı
        # sınırlı biçimde yükselt. Kazancı sınırlamak sessiz hat gürültüsünün
        # konuşma seviyesine taşınmasını önler.
        audio -= float(np.mean(audio))
        rms = float(np.sqrt(np.mean(audio * audio)))
        if rms >= 0.003:
            gain = min(4.0, max(0.65, 0.08 / rms))
            audio = np.clip(audio * gain, -0.98, 0.98)

        # Kelime başı/sonu mel penceresine sıkışmasın.
        padding = np.zeros(1920, dtype=np.float32)  # 120 ms @ 16 kHz
        return np.concatenate((padding, audio, padding))

    @staticmethod
    def _run(
        model: WhisperModel | None,
        audio: np.ndarray,
        label: str,
        domain_prompt: str | None,
        contextual: bool = False,
    ) -> Transcript:
        if model is None:
            return Transcript("", 0.0, label)
        hotwords = domain_prompt.split(":", 1)[-1].strip() if domain_prompt else None
        turbo = "turbo" in label
        beam_size = 1 if turbo else (3 if contextual else 5)
        segments, _ = model.transcribe(
            audio,
            language="tr",
            # large-v3-turbo greedy decoding için eğitildi; beam=5 CPU'da
            # konuşma başına gereksiz 6-7 saniye ekliyordu.
            beam_size=beam_size,
            best_of=1 if turbo else 5,
            vad_filter=False,
            condition_on_previous_text=False,
            temperature=0,
            repetition_penalty=1.12,
            no_repeat_ngram_size=3,
            compression_ratio_threshold=2.2,
            log_prob_threshold=-1.0,
            no_speech_threshold=0.55,
            # Beklenen adları yalnız hotword olarak ver. Bunları initial_prompt'a
            # yazmak kısa telefon sesinde modelin müşteriyi değil prompt metnini
            # tekrar etmesine yol açıyordu.
            hotwords=hotwords,
            # İlk hızlı geçiş serbest konuşmayı olduğu gibi çözer. Düşük güvenli
            # ikinci geçiş yalnız beklenen ad/hizmet/tarih/saat kelimeleriyle
            # yönlendirilir; aynı model ve aynı gerçek ses kullanılır.
            initial_prompt=None,
        )
        items = list(segments)
        text = " ".join(item.text.strip() for item in items).strip()
        if not items:
            return Transcript("", 0.0, label)
        avg_logprob = sum(item.avg_logprob for item in items) / len(items)
        confidence = max(0.0, min(1.0, 1.0 + avg_logprob))
        no_speech = sum(item.no_speech_prob for item in items) / len(items)
        compression = max(item.compression_ratio for item in items)
        duration = len(audio) / 16000
        if (
            _looks_like_hallucination(text, duration)
            or compression > 2.2
            or (no_speech > 0.72 and confidence < 0.45)
        ):
            log.info(
                "STT gürültü/halüsinasyon sonucu reddedildi model=%s "
                "no_speech=%.2f compression=%.2f chars=%d",
                label,
                no_speech,
                compression,
                len(text),
            )
            return Transcript("", 0.0, label, no_speech, compression)
        return Transcript(text, confidence, label, no_speech, compression)

    async def transcribe(
        self,
        pcm: bytes,
        accurate: bool = False,
        domain_prompt: str | None = None,
        contextual: bool = False,
    ) -> Transcript:
        if len(pcm) < 3200:
            return Transcript("", 0.0, "none")
        await self._ensure_models()
        cfg = get_voice_settings()
        audio = self._to_16k(pcm)
        sem = self._accurate_sem if accurate else self._fast_sem
        model = self._accurate if accurate else self._fast
        assert sem is not None
        async with sem:
            return await asyncio.to_thread(
                self._run,
                model,
                audio,
                cfg.voice_stt_accurate_model if accurate else cfg.voice_stt_fast_model,
                domain_prompt,
                contextual,
            )
