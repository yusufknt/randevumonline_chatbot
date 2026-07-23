from __future__ import annotations

import asyncio
import contextlib
import hashlib
import logging
import struct
import time
import uuid
import wave
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from prometheus_client import Counter, Gauge, Histogram

from app.core.db import get_db
from app.voice.config import get_voice_settings
from app.voice.dialog import DialogManager
from app.voice.identity import normalize_phone
from app.voice.registry import registry
from app.voice.stt import SpeechToTextEngine, choose_transcript, transcript_quality
from app.voice.tts import TextToSpeechEngine
from app.voice.vad import UtteranceSegmenter

log = logging.getLogger(__name__)

ACTIVE_CALLS = Gauge("voice_active_calls", "Aktif telefon çağrısı")
CALLS = Counter("voice_calls_total", "Telefon çağrıları", ["result"])
STT_SECONDS = Histogram("voice_stt_seconds", "Yerel STT süresi", buckets=(.2, .4, .7, 1, 1.5, 3, 6))
TURN_SECONDS = Histogram("voice_turn_seconds", "Söz sonundan ilk ses paketine süre", buckets=(.5, 1, 1.5, 2, 3, 5, 10))
BARGE_INS = Counter("voice_barge_ins_total", "Kullanıcının asistan sözünü kesmesi")


@dataclass(slots=True)
class _QueuedUtterance:
    pcm: bytes
    generation: int
    interrupted: bool = False


@dataclass(slots=True)
class _QueuedSpeech:
    text: str
    turn_started: float
    generation: int
    booking_success: bool = False


def encode_frame(packet_type: int, payload: bytes = b"") -> bytes:
    return bytes((packet_type,)) + struct.pack(">H", len(payload)) + payload


async def read_frame(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    header = await reader.readexactly(3)
    packet_type = header[0]
    length = struct.unpack(">H", header[1:])[0]
    payload = await reader.readexactly(length) if length else b""
    return packet_type, payload


async def resolve_business(did: str) -> dict | None:
    db = get_db()
    variants = {did, normalize_phone(did), did.lstrip("+")}
    business = await db.businesses.find_one({
        "channels.voice.enabled": True,
        "channels.voice.dids": {"$in": list(variants)},
    })
    if business:
        return business
    fallback = get_voice_settings().voice_default_business_slug
    if fallback:
        return await db.businesses.find_one({"business_id": fallback})
    return None


class AudioSocketCall:
    LOCKED_INTRO = "locked_intro"
    INTERRUPTIBLE_DIALOG = "interruptible_dialog"
    TERMINATING = "terminating"

    def __init__(
        self, call_uuid: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self.uuid = call_uuid
        self.reader = reader
        self.writer = writer
        self.stt = SpeechToTextEngine()
        self.segmenter = UtteranceSegmenter()
        self.dialog: DialogManager | None = None
        self.playback: asyncio.Task | None = None
        self.current_turn: asyncio.Task | None = None
        self.turn_pcm = bytearray()
        self.pending_utterances: deque[bytes] = deque()
        self.turn_revision = 0
        # Çağrı başına coroutine-safe kuyruklar. RTP okuma, STT/LLM ve TTS
        # birbirini bloklamaz; eski generation hiçbir zaman yeni sese karışmaz.
        self.audio_queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=200)
        self.llm_queue: asyncio.Queue[_QueuedUtterance] = asyncio.Queue(maxsize=4)
        self.tts_queue: asyncio.Queue[_QueuedSpeech] = asyncio.Queue(maxsize=4)
        self.workers: list[asyncio.Task] = []
        self.queue_mode = False
        self.stream_generation = 0
        self.current_turn_generation = 0
        self.current_speech_interrupted = False
        self.llm_cancel_event: asyncio.Event | None = None
        self.turn_stage = "idle"
        self.started = time.monotonic()
        self.first_audio_at: float | None = None
        self.frames_in = 0
        self.frames_out = 0
        self.result = "completed"
        self.business_id = None
        self.terminating = False
        self.phase = self.INTERRUPTIBLE_DIALOG

    async def run(self) -> None:
        context = await registry.wait(self.uuid)
        if context is None:
            raise RuntimeError("FastAGI çağrı bağlamı bulunamadı")
        business = await resolve_business(context.did)
        if business is None:
            raise RuntimeError("Aranan numara için etkin işletme bulunamadı")
        self.business_id = business["_id"]
        self.dialog = DialogManager(business, context.caller, self.uuid)
        await self.dialog.initialize()
        ACTIVE_CALLS.inc()
        self.queue_mode = True
        self.workers = [
            asyncio.create_task(self._audio_worker(), name=f"voice-audio-{self.uuid}"),
            asyncio.create_task(self._turn_worker(), name=f"voice-llm-{self.uuid}"),
            asyncio.create_task(self._tts_worker(), name=f"voice-tts-{self.uuid}"),
        ]
        # Karşılama dahil tüm diyalog sesleri insan konuşmasıyla kesilebilir.
        # Bayrağı playback task'ından önce açarak ilk ses paketindeki yarışı önle.
        self.phase = self.INTERRUPTIBLE_DIALOG
        self._start_playback(self._play_opening())
        try:
            while True:
                packet_type, payload = await read_frame(self.reader)
                if packet_type == 0x00:
                    break
                if packet_type == 0x03:
                    log.info("DTMF alındı uuid=%s digit=%s", self.uuid, payload[:1].decode(errors="ignore"))
                    continue
                if packet_type != 0x10:
                    continue
                self.frames_in += 1
                # Başarılı işlemden sonra kapanış anonsu kesilmesin ve yeni bir
                # STT/LLM turu başlamasın.
                if self.phase == self.TERMINATING or self.terminating or (
                    self.dialog and self.dialog.closed
                ):
                    continue
                if self.audio_queue.full():
                    # Gecikmeyi büyütmek yerine en eski 20 ms kareyi bırak.
                    # Normal çalışmada bu kuyruk dolmaz; yalnız event-loop uzun
                    # süre bloke olursa çağrının gerisinden sürüklenmeyi önler.
                    with contextlib.suppress(asyncio.QueueEmpty):
                        self.audio_queue.get_nowait()
                self.audio_queue.put_nowait(payload)
        except asyncio.IncompleteReadError:
            pass
        finally:
            await self.close()

    def _response_active(self) -> bool:
        return bool(
            (self.playback and not self.playback.done())
            or (self.current_turn and not self.current_turn.done())
            or not self.tts_queue.empty()
        )

    async def _audio_worker(self) -> None:
        while True:
            payload = await self.audio_queue.get()
            assistant_speaking = bool(self.playback and not self.playback.done())
            barge, utterances = self.segmenter.feed(payload, assistant_speaking)
            interrupted_on_start = False

            if self.segmenter.speech_started:
                interrupted = self._response_active()
                self.current_speech_interrupted = interrupted
                self.stream_generation += 1
                log.info(
                    "Voice detected uuid=%s generation=%d vad=%.2f rms=%.0f "
                    "ac_rms=%.0f zcr=%.2f",
                    self.uuid,
                    self.stream_generation,
                    self.segmenter.last_probability,
                    self.segmenter.last_rms,
                    getattr(self.segmenter, "last_ac_rms", 0.0),
                    getattr(self.segmenter, "last_zero_crossing_rate", 0.0),
                )
                log.info(
                    "Streaming STT started uuid=%s generation=%d",
                    self.uuid,
                    self.stream_generation,
                )
                if interrupted:
                    await self._interrupt_response()
                    interrupted_on_start = True

            # Bot, kullanıcı konuşmaya başladıktan sonra TTS'e geçmiş olabilir.
            # Bu durumda VAD başlangıç anında assistant_speaking=False idi; seviye
            # kontrolü eski cevabın kullanıcının üzerine binmesini engeller.
            if not interrupted_on_start:
                if (
                    self.segmenter.speaking
                    and self.playback
                    and not self.playback.done()
                    and not self.terminating
                ):
                    await self._interrupt_response()
                elif barge:
                    await self._interrupt_response()

            for utterance in utterances:
                self._queue_utterance(
                    utterance,
                    self.stream_generation,
                    interrupted=self.current_speech_interrupted,
                )
                self.current_speech_interrupted = False

    async def _interrupt_response(self) -> None:
        interrupt_started = time.monotonic()
        BARGE_INS.inc()
        log.info(
            "Interrupt detected uuid=%s generation=%d vad=%.2f rms=%.0f "
            "ac_rms=%.0f zcr=%.2f noise=%.0f",
            self.uuid,
            self.stream_generation,
            self.segmenter.last_probability,
            self.segmenter.last_rms,
            getattr(self.segmenter, "last_ac_rms", 0.0),
            getattr(self.segmenter, "last_zero_crossing_rate", 0.0),
            self.segmenter.noise_floor,
        )
        if self.llm_cancel_event and not self.llm_cancel_event.is_set():
            log.info(
                "Canceling LLM uuid=%s generation=%d",
                self.uuid,
                self.current_turn_generation,
            )
            self.llm_cancel_event.set()
        while not self.tts_queue.empty():
            with contextlib.suppress(asyncio.QueueEmpty):
                self.tts_queue.get_nowait()
        if self.playback and not self.playback.done():
            log.info(
                "Stopping TTS uuid=%s generation=%d",
                self.uuid,
                self.current_turn_generation,
            )
            await self._cancel_playback()
        log.info(
            "Restarting conversation uuid=%s generation=%d stop_ms=%d",
            self.uuid,
            self.stream_generation,
            round((time.monotonic() - interrupt_started) * 1000),
        )

    async def _turn_worker(self) -> None:
        while True:
            item = await self.llm_queue.get()
            if item.generation != self.stream_generation:
                continue
            self.current_turn_generation = item.generation
            self.llm_cancel_event = asyncio.Event()
            self.current_turn = asyncio.create_task(
                self._process_turn(
                    item.pcm,
                    generation=item.generation,
                    cancel_event=self.llm_cancel_event,
                    interrupted=item.interrupted,
                )
            )
            try:
                await self.current_turn
            except asyncio.CancelledError:
                if self.phase == self.TERMINATING:
                    raise
            finally:
                self.current_turn = None
                self.llm_cancel_event = None
                self.turn_stage = "idle"

    async def _tts_worker(self) -> None:
        while True:
            item = await self.tts_queue.get()
            if item.generation != self.stream_generation or self.segmenter.speaking:
                continue
            log.info(
                "New stream created uuid=%s generation=%d",
                self.uuid,
                item.generation,
            )
            awaitable = (
                self._play_booking_success()
                if item.booking_success
                else self._speak(item.text, item.turn_started, item.generation)
            )
            self._start_playback(awaitable)
            task = self.playback
            if task:
                with contextlib.suppress(asyncio.CancelledError):
                    await task

    async def _cancel_playback(self) -> None:
        if self.playback and not self.playback.done():
            self.playback.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.playback

    def _start_playback(self, awaitable) -> None:
        task = asyncio.create_task(awaitable)
        task.add_done_callback(self._playback_finished)
        self.playback = task

    def _playback_finished(self, task: asyncio.Task) -> None:
        if task.cancelled():
            return
        error = task.exception()
        if error is not None:
            log.error(
                "Ses oynatma görevi başarısız uuid=%s type=%s",
                self.uuid,
                type(error).__name__,
                exc_info=(type(error), error, error.__traceback__),
            )

    def _turn_finished(self, task: asyncio.Task) -> None:
        if self.current_turn is not task:
            return
        self.current_turn = None
        error = None if task.cancelled() else task.exception()
        if error is not None:
            log.error(
                "Konuşma turu başarısız uuid=%s type=%s",
                self.uuid,
                type(error).__name__,
            )
        if self.pending_utterances and self.phase != self.TERMINATING:
            self._start_next_turn()

    def _start_turn(self, pcm: bytes) -> None:
        self.turn_pcm = bytearray(pcm)
        self.turn_revision += 1
        self.current_turn = asyncio.create_task(self._process_turn(pcm))
        self.current_turn.add_done_callback(self._turn_finished)

    def _start_next_turn(self) -> None:
        if not self.pending_utterances:
            return
        pcm = self.pending_utterances.popleft()
        log.info(
            "Sıradaki kullanıcı konuşması işleniyor uuid=%s audio_ms=%d queue=%d",
            self.uuid,
            len(pcm) // 16,
            len(self.pending_utterances),
        )
        self._start_turn(pcm)

    def _queue_utterance(
        self,
        utterance: bytes,
        generation: int | None = None,
        *,
        interrupted: bool = False,
    ) -> None:
        """STT sürerken gelen ifadeyi mevcut sesi bozmayacak ayrı turda tutar."""
        if self.queue_mode:
            item = _QueuedUtterance(
                bytes(utterance),
                self.stream_generation if generation is None else generation,
                interrupted,
            )
            if self.llm_queue.full():
                with contextlib.suppress(asyncio.QueueEmpty):
                    dropped = self.llm_queue.get_nowait()
                    log.info(
                        "Eski LLM queue öğesi düşürüldü uuid=%s generation=%d",
                        self.uuid,
                        dropped.generation,
                    )
            self.llm_queue.put_nowait(item)
            return
        active = bool(self.current_turn and not self.current_turn.done())
        if active or self.pending_utterances:
            # Her tamamlanan ifade kendi sırasını korur. Böylece kullanıcı
            # "Yusuf", "saç kesimi", "yarın", "beş" diye hızlı ve parçalı
            # konuştuğunda ara parçalar ezilmez veya tek uzun sese eklenmez.
            limit = max(1, get_voice_settings().voice_max_pending_utterances)
            if len(self.pending_utterances) >= limit:
                dropped = self.pending_utterances.popleft()
                log.info(
                    "Eski konuşma parçası kuyruk sınırında düşürüldü uuid=%s "
                    "audio_ms=%d limit=%d",
                    self.uuid,
                    len(dropped) // 16,
                    limit,
                )
            self.pending_utterances.append(bytes(utterance))
            log.info(
                "Kullanıcı konuşması FIFO sırasına alındı uuid=%s "
                "audio_ms=%d queue=%d",
                self.uuid,
                len(utterance) // 16,
                len(self.pending_utterances),
            )
            return
        log.info(
            "Konuşma algılandı uuid=%s audio_ms=%d vad=%.2f rms=%.0f",
            self.uuid,
            len(utterance) // 16,
            self.segmenter.last_probability,
            self.segmenter.last_rms,
        )
        self._start_turn(bytes(utterance))

    async def _play_greeting(self) -> None:
        path = Path(get_voice_settings().voice_greeting_pcm)
        try:
            if not path.is_file():
                log.error("Hazır karşılama dosyası bulunamadı path=%s", path)
                return
            data = self._read_greeting_pcm(path)
            log.info(
                "Hazır karşılama başladı uuid=%s file=%s audio_ms=%d",
                self.uuid,
                path.name,
                len(data) // 16,
            )
            for offset in range(0, len(data), 320):
                chunk = data[offset:offset + 320].ljust(320, b"\0")
                await self._send_audio(chunk)
                await asyncio.sleep(.02)
            log.info("Hazır karşılama tamamlandı uuid=%s", self.uuid)
        finally:
            if self.phase != self.TERMINATING:
                self.phase = self.INTERRUPTIBLE_DIALOG

    async def _play_opening(self) -> None:
        """Kesilemez hazır karşılamayı, ardından kesilebilir ilk soruyu oynatır."""
        if not self.dialog:
            await self._play_greeting()
            return
        prompt = self.dialog.opening_prompt()
        opening_path_value = getattr(
            get_voice_settings(), "voice_opening_pcm", ""
        )
        opening_path = Path(opening_path_value) if opening_path_value else None

        if opening_path and opening_path.is_file():
            await self._play_greeting()
            if self.dialog.closed or self.terminating:
                return
            data = self._read_greeting_pcm(opening_path)
            chunks_sent = 0
            try:
                for offset in range(0, len(data), 320):
                    await self._send_audio(
                        data[offset:offset + 320].ljust(320, b"\0")
                    )
                    chunks_sent += 1
                    await asyncio.sleep(.02)
                log.info(
                    "Hazır kesilebilir personel sorusu tamamlandı uuid=%s chunks=%d",
                    self.uuid,
                    chunks_sent,
                )
            except asyncio.CancelledError:
                log.info(
                    "Hazır personel sorusu kullanıcı konuşmasıyla kesildi "
                    "uuid=%s chunks=%d",
                    self.uuid,
                    chunks_sent,
                )
                raise
            return

        async def prepare() -> list[bytes]:
            tts = TextToSpeechEngine()
            return [chunk async for chunk in tts.synthesize_stream(prompt)]

        # TTS üretimini 4 saniyelik hazır WAV çalarken başlat. WAV kesilemez;
        # fakat hazırlanan personel sorusu WAV biter bitmez normal biçimde
        # oynar ve kullanıcı konuşunca iptal edilebilir.
        prepared = asyncio.create_task(prepare())
        chunks_sent = 0
        try:
            await self._play_greeting()
            if self.dialog.closed or self.terminating:
                return
            chunks = await prepared
            if not chunks:
                log.error("Açılış personel TTS sesi üretilemedi uuid=%s", self.uuid)
                return
            for chunk in chunks:
                await self._send_audio(chunk)
                chunks_sent += 1
                await asyncio.sleep(.02)
            log.info(
                "Açılış personel TTS tamamlandı uuid=%s chunks=%d",
                self.uuid,
                chunks_sent,
            )
        except asyncio.CancelledError:
            log.info(
                "Açılış personel TTS kullanıcı konuşmasıyla kesildi uuid=%s chunks=%d",
                self.uuid,
                chunks_sent,
            )
            raise
        finally:
            if not prepared.done():
                prepared.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await prepared

    @staticmethod
    def _read_greeting_pcm(path: Path) -> bytes:
        """8 kHz mono 16-bit WAV veya eski ham SLIN dosyasını okur."""
        if path.suffix.lower() != ".wav":
            return path.read_bytes()
        with wave.open(str(path), "rb") as audio:
            audio_format = (
                audio.getnchannels(),
                audio.getsampwidth(),
                audio.getframerate(),
                audio.getcomptype(),
            )
            if audio_format != (1, 2, 8000, "NONE"):
                raise ValueError(
                    "Karşılama WAV dosyası 8 kHz mono 16-bit PCM olmalı"
                )
            return audio.readframes(audio.getnframes())

    def _generation_is_current(self, generation: int | None) -> bool:
        return generation is None or generation == self.stream_generation

    async def _schedule_speech(
        self,
        text: str,
        turn_started: float,
        generation: int | None,
        *,
        booking_success: bool = False,
    ) -> None:
        if not self._generation_is_current(generation):
            return
        if not self.queue_mode:
            self._start_playback(
                self._play_booking_success()
                if booking_success
                else self._speak(text, turn_started)
            )
            return
        item = _QueuedSpeech(
            text=text,
            turn_started=turn_started,
            generation=self.stream_generation if generation is None else generation,
            booking_success=booking_success,
        )
        if self.tts_queue.full():
            with contextlib.suppress(asyncio.QueueEmpty):
                self.tts_queue.get_nowait()
        self.tts_queue.put_nowait(item)

    async def _process_turn(
        self,
        pcm: bytes,
        generation: int | None = None,
        cancel_event: asyncio.Event | None = None,
        interrupted: bool = False,
    ) -> None:
        started = time.monotonic()
        assert self.dialog is not None
        expected_state, domain_prompt = self.dialog.stt_context()
        self.turn_stage = "stt"
        with STT_SECONDS.time():
            transcript = await self.stt.transcribe(pcm, domain_prompt=domain_prompt)
        if not self._generation_is_current(generation):
            return
        cfg = get_voice_settings()
        if (
            transcript.confidence < cfg.voice_stt_context_retry_confidence
            and expected_state != "general"
            and cfg.voice_stt_accurate_model != cfg.voice_stt_fast_model
        ):
            contextual = await self.stt.transcribe(
                pcm,
                domain_prompt=domain_prompt,
                contextual=True,
            )
            if not self._generation_is_current(generation):
                return
            selected = choose_transcript(transcript, contextual, domain_prompt)
            log.info(
                "STT bağlamsal ikinci geçiş uuid=%s state=%s "
                "first=%s/%.2f contextual=%s/%.2f selected=%s",
                self.uuid,
                expected_state,
                " ".join(transcript.text.split())[:120],
                transcript_quality(transcript, domain_prompt),
                " ".join(contextual.text.split())[:120],
                transcript_quality(contextual, domain_prompt),
                "contextual" if selected is contextual else "first",
            )
            transcript = selected
        if not transcript.text:
            self.turn_pcm.clear()
            answer = (
                self.dialog.interruption_retry_prompt()
                if interrupted
                else self.dialog.low_confidence_retry_prompt()
            )
            log.info(
                "STT boş sonuç; durum korunarak tekrar soruluyor uuid=%s state=%s",
                self.uuid,
                expected_state,
            )
            if self.pending_utterances:
                log.info(
                    "Boş STT tekrar sorusu kuyruk bitene kadar ertelendi "
                    "uuid=%s queue=%d",
                    self.uuid,
                    len(self.pending_utterances),
                )
                return
            await self._cancel_playback()
            await self._schedule_speech(answer, started, generation)
            return
        # Aynı modeli aynı ayarlarla ikinci kez çalıştırmak yalnızca gecikmeyi
        # artırır. Doğrulama modeli gerçekten farklıysa düşük güveni doğrula.
        if (
            transcript.confidence < cfg.voice_stt_accurate_confidence_threshold
            and len(pcm) >= 12800
            and cfg.voice_stt_accurate_model != cfg.voice_stt_fast_model
        ):
            log.info(
                "STT güçlü modelle doğrulanıyor uuid=%s fast_model=%s "
                "confidence=%.2f",
                self.uuid,
                transcript.model,
                transcript.confidence,
            )
            accurate = await self.stt.transcribe(
                pcm, accurate=True, domain_prompt=domain_prompt
            )
            if not self._generation_is_current(generation):
                return
            selected = choose_transcript(transcript, accurate, domain_prompt)
            log.info(
                "STT aday seçimi uuid=%s fast=%s/%.2f accurate=%s/%.2f "
                "selected=%s",
                self.uuid,
                " ".join(transcript.text.split())[:160],
                transcript_quality(transcript, domain_prompt),
                " ".join(accurate.text.split())[:160],
                transcript_quality(accurate, domain_prompt),
                selected.model,
            )
            transcript = selected
        stt_done = time.monotonic()
        raw_transcript = transcript.text
        normalized_transcript = self.dialog.normalize_stt_text(raw_transcript)
        if self.dialog.is_probable_playback_echo(normalized_transcript):
            self.turn_pcm.clear()
            log.info(
                "Okunan liste yankısı reddedildi uuid=%s state=%s text=%s",
                self.uuid,
                expected_state,
                " ".join(normalized_transcript.split())[:160],
            )
            return
        expected_entity_recognized = self.dialog.accepts_low_confidence_transcript(
            normalized_transcript
        )
        if (
            transcript.confidence < cfg.voice_stt_absolute_min_confidence
            and not expected_entity_recognized
        ):
            self.turn_pcm.clear()
            answer = (
                self.dialog.interruption_retry_prompt()
                if interrupted
                else self.dialog.low_confidence_retry_prompt()
            )
            log.info(
                "Mutlak düşük güvenli STT reddedildi uuid=%s state=%s "
                "confidence=%.2f text=%s",
                self.uuid,
                expected_state,
                transcript.confidence,
                " ".join(normalized_transcript.split())[:160],
            )
            if self.pending_utterances:
                log.info(
                    "Tekrar sorusu kuyruk bitene kadar ertelendi uuid=%s queue=%d",
                    self.uuid,
                    len(self.pending_utterances),
                )
                return
            await self._cancel_playback()
            await self._schedule_speech(answer, started, generation)
            return
        if (
            transcript.confidence < cfg.voice_stt_min_actionable_confidence
            and not expected_entity_recognized
        ):
            self.turn_pcm.clear()
            answer = (
                self.dialog.interruption_retry_prompt()
                if interrupted
                else self.dialog.low_confidence_retry_prompt()
            )
            log.info(
                "Düşük güvenli STT reddedildi uuid=%s state=%s confidence=%.2f "
                "text=%s",
                self.uuid,
                expected_state,
                transcript.confidence,
                " ".join(normalized_transcript.split())[:160],
            )
            await self._cancel_playback()
            if self.pending_utterances:
                log.info(
                    "Düşük güven tekrar sorusu kuyruk bitene kadar ertelendi "
                    "uuid=%s queue=%d",
                    self.uuid,
                    len(self.pending_utterances),
                )
                return
            await self._schedule_speech(answer, started, generation)
            return
        if (
            transcript.confidence < cfg.voice_stt_min_actionable_confidence
            and expected_entity_recognized
        ):
            sanitized = self.dialog.sanitize_low_confidence_transcript(
                normalized_transcript
            )
            log.info(
                "Düşük güvenli STT yalnız kesin alanla sınırlandı uuid=%s "
                "state=%s raw=%s sanitized=%s",
                self.uuid,
                expected_state,
                " ".join(normalized_transcript.split())[:160],
                sanitized,
            )
            normalized_transcript = sanitized
        log.info(
            "STT tamam uuid=%s state=%s model=%s confidence=%.2f chars=%d ms=%d",
            self.uuid,
            expected_state,
            transcript.model,
            transcript.confidence,
            len(transcript.text),
            round((stt_done - started) * 1000),
        )
        log.info(
            "Streaming STT finished uuid=%s generation=%d",
            self.uuid,
            self.stream_generation if generation is None else generation,
        )
        if normalized_transcript != raw_transcript:
            log.info(
                "STT bağlamsal düzeltme uuid=%s state=%s raw=%s normalized=%s",
                self.uuid,
                expected_state,
                " ".join(raw_transcript.split())[:250],
                " ".join(normalized_transcript.split())[:250],
            )
        safe_transcript = " ".join(normalized_transcript.split())[:500]
        log.info(
            "ALGILANAN KULLANICI KONUŞMASI uuid=%s :: %s",
            self.uuid,
            safe_transcript,
        )
        self.turn_stage = "llm"
        try:
            answer = await self.dialog.respond(
                normalized_transcript,
                cancel_event=cancel_event,
            )
        except asyncio.CancelledError:
            log.info(
                "LLM response canceled uuid=%s generation=%d",
                self.uuid,
                self.stream_generation if generation is None else generation,
            )
            return
        if not self._generation_is_current(generation):
            log.info(
                "Eski cevap generation nedeniyle atıldı uuid=%s "
                "generation=%d current=%d",
                self.uuid,
                self.stream_generation if generation is None else generation,
                self.stream_generation,
            )
            return
        if self.dialog.closed:
            self.terminating = True
            self.phase = self.TERMINATING
            self.pending_utterances.clear()
        self.turn_pcm.clear()
        safe_answer = " ".join(answer.split())[:500]
        log.info(
            "ASİSTAN CEVABI uuid=%s :: %s",
            self.uuid,
            safe_answer,
        )
        log.info(
            "Diyalog tamam uuid=%s answer_chars=%d ms=%d",
            self.uuid,
            len(answer),
            round((time.monotonic() - stt_done) * 1000),
        )
        await self._cancel_playback()
        if self.pending_utterances and not self.dialog.closed:
            log.info(
                "Ara asistan cevabı kuyruk bitene kadar seslendirilmedi "
                "uuid=%s queue=%d",
                self.uuid,
                len(self.pending_utterances),
            )
            return
        if getattr(self.dialog, "completion_kind", None) == "booking_success":
            await self._schedule_speech(
                answer, started, generation, booking_success=True
            )
        else:
            await self._schedule_speech(answer, started, generation)

    async def _speak(
        self, text: str, turn_started: float, generation: int | None = None
    ) -> None:
        tts = TextToSpeechEngine()
        first = True
        chunks_sent = 0
        log.info(
            "Streaming TTS started uuid=%s generation=%d",
            self.uuid,
            self.stream_generation if generation is None else generation,
        )
        try:
            async for chunk in tts.synthesize_stream(text):
                if not self._generation_is_current(generation):
                    raise asyncio.CancelledError
                if first:
                    TURN_SECONDS.observe(time.monotonic() - turn_started)
                    log.info(
                        "İlk cevap sesi uuid=%s latency_ms=%d",
                        self.uuid,
                        round((time.monotonic() - turn_started) * 1000),
                    )
                    first = False
                await self._send_audio(chunk)
                chunks_sent += 1
                await asyncio.sleep(.02)
        except asyncio.CancelledError:
            log.info(
                "Streaming TTS stopped uuid=%s generation=%d chunks=%d",
                self.uuid,
                self.stream_generation if generation is None else generation,
                chunks_sent,
            )
            raise
        except Exception as exc:
            log.error(
                "TTS cevabı oynatılamadı uuid=%s type=%s",
                self.uuid,
                type(exc).__name__,
            )
        if first:
            log.error(
                "TTS cevabı üretilemedi uuid=%s; farklı konuşmacı sesi oynatılmadı",
                self.uuid,
            )
        else:
            log.info(
                "TTS stream tamamlandı uuid=%s chunks=%d audio_ms=%d",
                self.uuid,
                chunks_sent,
                chunks_sent * 20,
            )
            log.info(
                "Streaming TTS stopped uuid=%s generation=%d reason=completed",
                self.uuid,
                self.stream_generation if generation is None else generation,
            )
        if self.dialog and self.dialog.closed:
            await self._finish_assistant_hangup()

    async def _play_booking_success(self) -> None:
        """Başarılı kayıt kapanışını hazır sesten eksiksiz oynatıp hattı kapatır."""
        path = Path(get_voice_settings().voice_booking_success_pcm)
        if not path.is_file():
            log.error(
                "Hazır başarılı randevu kapanışı bulunamadı uuid=%s path=%s",
                self.uuid,
                path,
            )
            # Ön kontrol bu durumu canlıdan önce engeller. Yine de çağrıyı sessiz
            # kapatmamak için aynı metni mevcut ana TTS sağlayıcısıyla dene.
            await self._speak("Randevunuz oluşturuldu. İyi günler.", time.monotonic())
            return
        data = self._read_greeting_pcm(path)
        chunks_sent = 0
        for offset in range(0, len(data), 320):
            chunk = data[offset:offset + 320].ljust(320, b"\0")
            await self._send_audio(chunk)
            chunks_sent += 1
            await asyncio.sleep(.02)
        log.info(
            "Başarılı randevu kapanış WAV tamamlandı uuid=%s chunks=%d audio_ms=%d",
            self.uuid,
            chunks_sent,
            chunks_sent * 20,
        )
        await self._finish_assistant_hangup()

    async def _finish_assistant_hangup(self) -> None:
        self.result = "assistant_hangup"
        log.info("Kapanış anonsu tamamlandı, çağrı sonlandırılıyor uuid=%s", self.uuid)
        with contextlib.suppress(ConnectionError):
            self.writer.write(encode_frame(0x00))
            await self.writer.drain()
        # AudioSocket TCP kapanınca Asterisk uygulaması döner ve dialplan'daki
        # Hangup çalışır. Küçük gecikme sonlandırma çerçevesinin iletilmesini sağlar.
        await asyncio.sleep(.15)
        self.writer.close()
        with contextlib.suppress(Exception):
            await asyncio.wait_for(self.writer.wait_closed(), timeout=2)

    async def _send_audio(self, chunk: bytes) -> None:
        self.writer.write(encode_frame(0x10, chunk))
        await self.writer.drain()
        self.frames_out += 1
        if self.first_audio_at is None:
            self.first_audio_at = time.monotonic()

    async def close(self) -> None:
        # İptal edilen STT görevinin callback'i bekleyen FIFO turunu yeniden
        # başlatmasın; çağrı kapanırken artık hiçbir yeni iş kabul edilmez.
        self.phase = self.TERMINATING
        if self.llm_cancel_event:
            self.llm_cancel_event.set()
        await self._cancel_playback()
        if self.current_turn and not self.current_turn.done():
            self.current_turn.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.current_turn
        current_task = asyncio.current_task()
        for worker in self.workers:
            if worker is not current_task and not worker.done():
                worker.cancel()
        if self.workers:
            await asyncio.gather(
                *(worker for worker in self.workers if worker is not current_task),
                return_exceptions=True,
            )
        self.workers.clear()
        self.queue_mode = False
        self.pending_utterances.clear()
        await registry.remove(self.uuid)
        if self.dialog:
            await self.dialog.shutdown()
        self.writer.close()
        with contextlib.suppress(Exception):
            await self.writer.wait_closed()
        ACTIVE_CALLS.dec()
        CALLS.labels(self.result).inc()
        context_hash = hashlib.sha256(self.uuid.encode()).hexdigest()[:16]
        with contextlib.suppress(Exception):
            await get_db().voice_calls.insert_one({
                "call_hash": context_hash,
                "business_id": self.business_id,
                "duration_ms": round((time.monotonic() - self.started) * 1000),
                "frames_in": self.frames_in,
                "frames_out": self.frames_out,
                "result": self.result,
                "created_at": datetime.now(timezone.utc),
            })


async def handle_audiosocket(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    cfg = get_voice_settings()
    if ACTIVE_CALLS._value.get() >= cfg.voice_max_concurrent_calls:
        writer.write(encode_frame(0xFF, b"\x04"))
        await writer.drain()
        writer.close()
        return
    try:
        packet_type, payload = await asyncio.wait_for(read_frame(reader), 3)
        if packet_type != 0x01 or len(payload) != 16:
            raise ValueError("İlk AudioSocket paketi UUID olmalı")
        call_uuid = str(uuid.UUID(bytes=payload))
        await AudioSocketCall(call_uuid, reader, writer).run()
    except Exception as exc:
        CALLS.labels("error").inc()
        log.warning("AudioSocket çağrı hatası type=%s", type(exc).__name__)
        writer.close()
        with contextlib.suppress(Exception):
            await writer.wait_closed()


async def start_audiosocket() -> asyncio.Server:
    settings = get_voice_settings()
    return await asyncio.start_server(
        handle_audiosocket,
        settings.voice_audiosocket_host,
        settings.voice_audiosocket_port,
        limit=1024 * 1024,
    )
