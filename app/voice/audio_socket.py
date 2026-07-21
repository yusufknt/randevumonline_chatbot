from __future__ import annotations

import asyncio
import contextlib
import hashlib
import logging
import struct
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from prometheus_client import Counter, Gauge, Histogram

from app.core.db import get_db
from app.voice.config import get_voice_settings
from app.voice.dialog import DialogManager
from app.voice.identity import normalize_phone
from app.voice.registry import registry
from app.voice.stt import SpeechToTextEngine
from app.voice.tts import TextToSpeechEngine
from app.voice.vad import UtteranceSegmenter

log = logging.getLogger(__name__)

ACTIVE_CALLS = Gauge("voice_active_calls", "Aktif telefon çağrısı")
CALLS = Counter("voice_calls_total", "Telefon çağrıları", ["result"])
STT_SECONDS = Histogram("voice_stt_seconds", "Yerel STT süresi", buckets=(.2, .4, .7, 1, 1.5, 3, 6))
TURN_SECONDS = Histogram("voice_turn_seconds", "Söz sonundan ilk ses paketine süre", buckets=(.5, 1, 1.5, 2, 3, 5, 10))
BARGE_INS = Counter("voice_barge_ins_total", "Kullanıcının asistan sözünü kesmesi")


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
        self.turn_revision = 0
        self.started = time.monotonic()
        self.first_audio_at: float | None = None
        self.frames_in = 0
        self.frames_out = 0
        self.result = "completed"
        self.business_id = None

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
        self.playback = asyncio.create_task(self._play_greeting())
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
                barge, utterances = self.segmenter.feed(
                    payload, bool(self.playback and not self.playback.done())
                )
                if barge:
                    BARGE_INS.inc()
                    await self._cancel_playback()
                if utterances:
                    for utterance in utterances:
                        self._queue_utterance(utterance)
        except asyncio.IncompleteReadError:
            pass
        finally:
            await self.close()

    async def _cancel_playback(self) -> None:
        if self.playback and not self.playback.done():
            self.playback.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.playback

    def _turn_finished(self, task: asyncio.Task) -> None:
        if task.cancelled():
            return
        error = task.exception()
        if error:
            log.error(
                "Konuşma turu başarısız uuid=%s type=%s",
                self.uuid,
                type(error).__name__,
            )

    def _start_turn(self, pcm: bytes, revision: int) -> None:
        self.current_turn = asyncio.create_task(
            self._process_turn(pcm, revision)
        )
        self.current_turn.add_done_callback(self._turn_finished)

    def _queue_utterance(self, utterance: bytes) -> None:
        """STT sürerken gelen devam cümlesini kaybetmeden aynı tura ekler."""
        active = bool(self.current_turn and not self.current_turn.done())
        if active and self.turn_pcm:
            # Ayrı VAD parçaları Whisper tarafından tek kelime gibi
            # birleştirilmesin; araya 100 ms telefon sessizliği koy.
            self.turn_pcm.extend(b"\0" * 1600)
            self.turn_pcm.extend(utterance)
        else:
            self.turn_pcm = bytearray(utterance)
        self.turn_revision += 1
        revision = self.turn_revision
        log.info(
            "%s uuid=%s audio_ms=%d vad=%.2f rms=%.0f",
            "Konuşma devamı birleştirildi" if active else "Konuşma algılandı",
            self.uuid,
            len(self.turn_pcm) // 16,
            self.segmenter.last_probability,
            self.segmenter.last_rms,
        )
        if not active:
            self._start_turn(bytes(self.turn_pcm), revision)

    async def _play_greeting(self) -> None:
        path = Path(get_voice_settings().voice_greeting_pcm)
        if not path.is_file():
            return
        data = path.read_bytes()
        for offset in range(0, len(data), 320):
            chunk = data[offset:offset + 320].ljust(320, b"\0")
            await self._send_audio(chunk)
            await asyncio.sleep(.02)

    async def _process_turn(self, pcm: bytes, revision: int) -> None:
        started = time.monotonic()
        assert self.dialog is not None
        expected_state, domain_prompt = self.dialog.stt_context()
        with STT_SECONDS.time():
            transcript = await self.stt.transcribe(pcm, domain_prompt=domain_prompt)
        if revision != self.turn_revision:
            # STT çalışırken kullanıcı cümleye devam etti. Eksik ilk parçaya
            # cevap vermek yerine bütün parçaları birlikte çözümleriz.
            latest_revision = self.turn_revision
            latest_pcm = bytes(self.turn_pcm)
            log.info(
                "Birleştirilmiş konuşma yeniden çözümleniyor uuid=%s "
                "audio_ms=%d revision=%d",
                self.uuid,
                len(latest_pcm) // 16,
                latest_revision,
            )
            self._start_turn(latest_pcm, latest_revision)
            return
        if not transcript.text:
            self.turn_pcm.clear()
            log.info("STT boş sonuç uuid=%s", self.uuid)
            return
        # Aynı modeli aynı ayarlarla ikinci kez çalıştırmak yalnızca gecikmeyi
        # artırır. Doğrulama modeli gerçekten farklıysa düşük güveni doğrula.
        cfg = get_voice_settings()
        if (
            transcript.confidence < .25
            and len(pcm) >= 12800
            and cfg.voice_stt_accurate_model != cfg.voice_stt_fast_model
        ):
            accurate = await self.stt.transcribe(
                pcm, accurate=True, domain_prompt=domain_prompt
            )
            if accurate.text:
                transcript = accurate
        stt_done = time.monotonic()
        raw_transcript = transcript.text
        normalized_transcript = self.dialog.normalize_stt_text(raw_transcript)
        log.info(
            "STT tamam uuid=%s state=%s model=%s confidence=%.2f chars=%d ms=%d",
            self.uuid,
            expected_state,
            transcript.model,
            transcript.confidence,
            len(transcript.text),
            round((stt_done - started) * 1000),
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
        answer = await self.dialog.respond(normalized_transcript)
        if revision != self.turn_revision:
            latest_revision = self.turn_revision
            latest_pcm = bytes(self.turn_pcm)
            self._start_turn(latest_pcm, latest_revision)
            return
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
        self.playback = asyncio.create_task(self._speak(answer, started))

    async def _speak(self, text: str, turn_started: float) -> None:
        tts = TextToSpeechEngine()
        first = True
        try:
            async for chunk in tts.synthesize_stream(text):
                if first:
                    TURN_SECONDS.observe(time.monotonic() - turn_started)
                    log.info(
                        "İlk cevap sesi uuid=%s latency_ms=%d",
                        self.uuid,
                        round((time.monotonic() - turn_started) * 1000),
                    )
                    first = False
                await self._send_audio(chunk)
                await asyncio.sleep(.02)
        except asyncio.CancelledError:
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
        if self.dialog and self.dialog.closed:
            self.writer.write(encode_frame(0x00))
            await self.writer.drain()

    async def _send_audio(self, chunk: bytes) -> None:
        self.writer.write(encode_frame(0x10, chunk))
        await self.writer.drain()
        self.frames_out += 1
        if self.first_audio_at is None:
            self.first_audio_at = time.monotonic()

    async def close(self) -> None:
        await self._cancel_playback()
        if self.current_turn and not self.current_turn.done():
            self.current_turn.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.current_turn
        await registry.remove(self.uuid)
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
