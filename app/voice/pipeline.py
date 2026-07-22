"""
FAZ 3 - Asenkron Kuyruk Mimarisi ile Doğal Konuşma (Full Duplex / Barge-In)
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import re
import struct
import time
from typing import Any, Callable, Coroutine

from app.voice.llm import VoiceLLMEngine
from app.voice.models import SessionState, VoiceSession
from app.voice.stt import (
    SpeechToTextEngine,
    choose_transcript,
    transcript_quality,
)
from app.voice.tts import TextToSpeechEngine

logger = logging.getLogger(__name__)


_HANGUP_SENTINEL = object()


class _QueuedText(str):
    """TTS metnini üretildiği konuşma turuyla birlikte taşır."""

    def __new__(cls, value: str, generation: int):
        item = super().__new__(cls, value)
        item.generation = generation
        return item


class _QueuedControl:
    def __init__(self, value: object, generation: int) -> None:
        self.value = value
        self.generation = generation


class VoicePipeline:
    """Ses oturumu için uçtan uca asenkron kuyruk mimarisine sahip yöneticidir."""

    def __init__(self, session: VoiceSession) -> None:
        self.session = session
        self.stt = SpeechToTextEngine()
        self.llm = VoiceLLMEngine(
            business_slug=session.business_slug,
            customer_phone=session.caller_number,
        )
        self.tts = TextToSpeechEngine()
        
        # Asenkron Kuyruklar
        self.audio_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.llm_queue: asyncio.Queue[str] = asyncio.Queue()
        self.stt_queue: asyncio.Queue[tuple[bytes, int]] = asyncio.Queue(maxsize=1)
        self.tts_queue: asyncio.Queue[str | object] = asyncio.Queue()
        
        # Kontrol Event'leri (Interrupt/Barge-in)
        self.interrupt_event = asyncio.Event()
        self._interrupt_generation = 0
        
        # Callback
        self.send_audio_cb: Callable[[bytes], Coroutine[Any, Any, None]] | None = None
        self.on_hangup: Callable[[], Coroutine[Any, Any, None]] | None = None
        self._hangup_started = False
        self._stt_domain_prompt: str | None = None
        self._stt_context_task: asyncio.Task | None = None
        self._last_transcript_key = ""
        self._last_transcript_generation = -1
        self._last_transcript_at = 0.0
        self._last_clarification_at = 0.0
        
        # Worker Task'lar
        self._workers: list[asyncio.Task] = []
        self._is_running = False

    def start(self, send_audio_cb: Callable[[bytes], Coroutine[Any, Any, None]]) -> None:
        """Kuyrukları okuyan asenkron işçileri (workers) başlatır."""
        if self._is_running:
            return
            
        self.send_audio_cb = send_audio_cb
        self._is_running = True
        
        self._workers.append(asyncio.create_task(self._audio_worker()))
        self._workers.append(asyncio.create_task(self._stt_worker()))
        self._workers.append(asyncio.create_task(self._llm_worker()))
        self._workers.append(asyncio.create_task(self._tts_worker()))
        self._workers.append(asyncio.create_task(self._play_opening()))
        self._stt_context_task = asyncio.create_task(self._prime_stt_context())
        
        logger.info("🟢 Pipeline başlatıldı. (session_id=%s)", self.session.session_id)

    async def _prime_stt_context(self) -> None:
        """Usta ve hizmet adlarını ilk müşteri cümlesinden önce STT'ye hazırla."""
        from app.voice.tools import VoiceToolExecutor

        try:
            services, staff = await asyncio.gather(
                VoiceToolExecutor.get_services(self.session.business_slug or ""),
                VoiceToolExecutor.get_staff(self.session.business_slug or ""),
            )
            service_names = [str(item) for item in services]
            staff_names = [str(item) for item in staff]
            # LLM aynı katalog bilgisini alan çıkarımında da kullanabilsin.
            self.llm._db_services = service_names
            self.llm._db_staff = staff_names
            terms = [
                *staff_names,
                *service_names,
                "bugün", "yarın", "pazartesi", "salı", "çarşamba",
                "perşembe", "cuma", "cumartesi", "pazar",
                "saat", "evet", "hayır", "yok", "onaylıyorum",
            ]
            self._stt_domain_prompt = "Beklenen kelimeler: " + ", ".join(terms)
            logger.info(
                "STT çağrı bağlamı hazır staff=%d services=%d session_id=%s",
                len(staff_names),
                len(service_names),
                self.session.session_id,
            )
        except Exception as exc:
            # Katalog ön yüklemesi görüşmeyi engellemez; STT bağlamsız devam eder.
            logger.warning("STT çağrı bağlamı hazırlanamadı: %s", exc)

    def stop(self) -> None:
        """Pipeline işçilerini durdurur."""
        self._is_running = False
        for task in self._workers:
            task.cancel()
        if self._stt_context_task:
            self._stt_context_task.cancel()
        logger.info("🛑 Pipeline durduruldu. (session_id=%s)", self.session.session_id)

    def feed_audio(self, pcm_audio: bytes) -> None:
        """RTP Server'dan gelen ham ses paketlerini kuyruğa ekler."""
        if self._is_running:
            self.audio_queue.put_nowait(pcm_audio)

    async def _play_opening(self) -> None:
        from app.voice.config import get_voice_settings
        import wave
        from pathlib import Path
        
        def read_pcm(path: Path) -> bytes:
            if path.suffix.lower() == ".wav":
                with wave.open(str(path), "rb") as f:
                    return f.readframes(f.getnframes())
            return path.read_bytes()
            
        settings = get_voice_settings()
        generation = self._interrupt_generation
        
        # 1. Sabit karşılama
        greeting_path = Path(settings.voice_greeting_pcm)
        if greeting_path.is_file():
            self.session.update_state(SessionState.SPEAKING)
            data = read_pcm(greeting_path)
            for offset in range(0, len(data), 320):
                if (
                    not self._is_running
                    or generation != self._interrupt_generation
                ):
                    return
                chunk = data[offset:offset + 320].ljust(320, b"\0")
                if self.send_audio_cb:
                    await self.send_audio_cb(chunk)
                await asyncio.sleep(.02)
                
        # 2. Kesilebilir (Barge-in) Personel Sorusu
        opening_path_value = getattr(settings, "voice_opening_pcm", "")
        opening_path = Path(opening_path_value) if opening_path_value else None
        
        if opening_path and opening_path.is_file():
            # Buradan itibaren kesilebilir
            self.session.update_state(SessionState.SPEAKING)
            
            data = read_pcm(opening_path)
            try:
                for offset in range(0, len(data), 320):
                    if (
                        not self._is_running
                        or generation != self._interrupt_generation
                    ):
                        return
                    chunk = data[offset:offset + 320].ljust(320, b"\0")
                    if self.send_audio_cb:
                        await self.send_audio_cb(chunk)
                    await asyncio.sleep(.02)
            except asyncio.CancelledError:
                pass
                
        if generation == self._interrupt_generation:
            self.session.update_state(SessionState.LISTENING)

    def trigger_interrupt(self) -> None:
        """Kullanıcı konuştuğunda STT/TTS ve LLM'i susturup sıfırlar."""
        # Kapanış kararı verildikten sonra son anons ve SIP BYE kesilmemeli.
        if self.llm.is_session_closed:
            return
        if not self.interrupt_event.is_set():
            logger.info("🚨 KULLANICI ARAYA GİRDİ (Barge-in). AI susturuluyor... (session_id=%s)", self.session.session_id)
            self._interrupt_generation += 1
            self.interrupt_event.set()
            
            # Eski üretilmiş TTS ve LLM isteklerini temizle
            while not self.tts_queue.empty():
                try: self.tts_queue.get_nowait()
                except asyncio.QueueEmpty: pass
                
            while not self.llm_queue.empty():
                try: self.llm_queue.get_nowait()
                except asyncio.QueueEmpty: pass
                
            self.session.update_state(SessionState.LISTENING)

    def _queue_stt(self, utterance: bytes) -> None:
        """STT'yi tek worker'da tut; bekleyen eski parçanın yerine yenisini koy."""
        if self.stt_queue.full():
            with contextlib.suppress(asyncio.QueueEmpty):
                self.stt_queue.get_nowait()
            logger.info("Bekleyen eski STT parçası yenisiyle değiştirildi")
        self.stt_queue.put_nowait((utterance, self._interrupt_generation))

    async def _stt_worker(self) -> None:
        """Aynı çağrıda birden fazla Whisper işinin paralel çalışmasını engelle."""
        while self._is_running:
            try:
                utterance, generation = await self.stt_queue.get()
                await self._process_stt(utterance, generation)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("STT worker hatası: %s", exc)

    async def _audio_worker(self) -> None:
        """Sesi biriktirir, VAD ile kesme yapar ve sessizlikte STT'ye yollar."""
        from app.voice.vad import UtteranceSegmenter
        segmenter = UtteranceSegmenter()
        
        while self._is_running:
            try:
                # Küçük zaman aşımlarıyla kuyruktan oku ki iptal durumlarında asılı kalmasın
                pcm_audio = await asyncio.wait_for(self.audio_queue.get(), timeout=0.1)
                
                state_before = self.session.state
                was_customer_speaking = segmenter.speaking
                assistant_speaking = (state_before == SessionState.SPEAKING)
                barge, completed = segmenter.feed(pcm_audio, assistant_speaking)
                
                if barge:
                    self.trigger_interrupt()
                elif (
                    not was_customer_speaking
                    and segmenter.speaking
                    and (
                        state_before == SessionState.PROCESSING
                        or not self.tts_queue.empty()
                        or not self.llm_queue.empty()
                    )
                ):
                    # Bot henüz cevap hazırlarken gelen yeni insan sesi de önceki
                    # turun sonradan konuşmaya başlamasını engellemelidir.
                    self.trigger_interrupt()
                    
                for utterance in completed:
                    if len(utterance) >= 8000: # En az 0.5 saniye ses varsa STT yap
                        self._queue_stt(utterance)
                        
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Audio Worker hatası: %s", e)

    async def _process_stt(self, pcm_audio: bytes, generation: int | None = None) -> None:
        if self.llm.is_session_closed:
            return
        if generation is None:
            generation = self._interrupt_generation
        elif generation != self._interrupt_generation:
            logger.info("Eski konuşma turuna ait STT parçası atlandı")
            return
        self.session.update_state(SessionState.PROCESSING)
        self.interrupt_event.clear() # Yeni işlem başlıyor, interrupt'ı sıfırla

        if self._stt_context_task and not self._stt_context_task.done():
            with contextlib.suppress(asyncio.TimeoutError, asyncio.CancelledError):
                await asyncio.wait_for(
                    asyncio.shield(self._stt_context_task), timeout=0.75
                )
        
        try:
            from app.voice.config import get_voice_settings

            transcript = await self.stt.transcribe(
                pcm_audio,
                domain_prompt=self._stt_domain_prompt,
            )
            cfg = get_voice_settings()
            if (
                generation == self._interrupt_generation
                and transcript.confidence < cfg.voice_stt_context_retry_confidence
            ):
                contextual = await self.stt.transcribe(
                    pcm_audio,
                    domain_prompt=self._stt_domain_prompt,
                    contextual=True,
                )
                selected = choose_transcript(
                    transcript, contextual, self._stt_domain_prompt
                )
                logger.info(
                    "STT bağlamsal doğrulama first=%s/%.2f contextual=%s/%.2f selected=%s",
                    " ".join(transcript.text.split())[:120],
                    transcript_quality(transcript, self._stt_domain_prompt),
                    " ".join(contextual.text.split())[:120],
                    transcript_quality(contextual, self._stt_domain_prompt),
                    "contextual" if selected is contextual else "first",
                )
                transcript = selected
            if (
                transcript
                and transcript.text
                and generation == self._interrupt_generation
            ):
                quality = transcript_quality(
                    transcript, self._stt_domain_prompt
                )
                if quality < cfg.voice_stt_absolute_min_confidence:
                    logger.info(
                        "STT düşük güven nedeniyle LLM'e gönderilmedi "
                        "confidence=%.2f quality=%.2f text=%s",
                        transcript.confidence,
                        quality,
                        " ".join(transcript.text.split())[:160],
                    )
                    now = time.monotonic()
                    if (
                        (
                            not hasattr(self, "stt_queue")
                            or self.stt_queue.empty()
                        )
                        and now - getattr(self, "_last_clarification_at", 0.0) >= 6.0
                    ):
                        await self.tts_queue.put(_QueuedText(
                            "Sizi net anlayamadım. Lütfen kısa ve net tekrar eder misiniz?",
                            generation,
                        ))
                        self._last_clarification_at = now
                    self.session.update_state(SessionState.LISTENING)
                    return
                transcript_key = re.sub(
                    r"[^a-zçğıöşü0-9]+",
                    " ",
                    transcript.text.replace("İ", "i").replace("I", "ı").lower(),
                ).strip()
                now = time.monotonic()
                if (
                    transcript_key
                    and transcript_key == getattr(self, "_last_transcript_key", "")
                    and generation == getattr(self, "_last_transcript_generation", -1)
                    and now - getattr(self, "_last_transcript_at", 0.0) < 10.0
                ):
                    logger.info(
                        "Tekrarlanan STT sonucu LLM'e gönderilmedi text=%s",
                        transcript.text[:160],
                    )
                    self.session.update_state(SessionState.LISTENING)
                    return
                logger.info(
                    "✅ STT tamamlandı confidence=%.2f quality=%.2f: '%s'",
                    transcript.confidence,
                    quality,
                    transcript.text,
                )
                self._last_transcript_key = transcript_key
                self._last_transcript_generation = generation
                self._last_transcript_at = now
                await self.llm_queue.put(transcript.text)
            elif generation == self._interrupt_generation:
                logger.info("STT boş sonuç LLM'e gönderilmedi")
                now = time.monotonic()
                if (
                    (
                        not hasattr(self, "stt_queue")
                        or self.stt_queue.empty()
                    )
                    and now - getattr(self, "_last_clarification_at", 0.0) >= 6.0
                ):
                    await self.tts_queue.put(_QueuedText(
                        "Sizi net anlayamadım. Lütfen kısa ve net tekrar eder misiniz?",
                        generation,
                    ))
                    self._last_clarification_at = now
                self.session.update_state(SessionState.LISTENING)
        except Exception as e:
            logger.error("STT hatası: %s", e)
            self.session.update_state(SessionState.LISTENING)

    async def _llm_worker(self) -> None:
        """STT'den gelen metni alıp LLM'e yollar, gelen cevabı TTS'e atar."""
        while self._is_running:
            try:
                text = await asyncio.wait_for(self.llm_queue.get(), timeout=0.5)
                
                if self.interrupt_event.is_set():
                    continue # İptal edildiyse işlemi atla
                generation = self._interrupt_generation
                    
                logger.info("⏳ LLM'e istek gönderiliyor...")
                try:
                    response_parts: list[str] = []
                    async for sentence in self.llm.generate_response(text):
                        if generation != self._interrupt_generation:
                            logger.info("🛑 LLM yayını araya girilerek İPTAL edildi.")
                            break
                            
                        if sentence:
                            logger.info("🧠 LLM cümlesi: '%s'", sentence)
                            response_parts.append(sentence.strip())

                    if (
                        response_parts
                        and generation == self._interrupt_generation
                    ):
                        # Tek LLM turunu tek TTS isteğinde oynat. Cümle başına
                        # ayrı TTS, botun art arda yeniden konuşması gibi duyuluyordu.
                        await self.tts_queue.put(_QueuedText(
                            " ".join(response_parts), generation
                        ))

                    # FIFO kapanış işareti, bu yanıta ait bütün TTS
                    # cümlelerinden sonra işlenir.
                    if (
                        self.llm.is_session_closed
                        and generation == self._interrupt_generation
                    ):
                        await self.tts_queue.put(
                            _QueuedControl(_HANGUP_SENTINEL, generation)
                        )
                            
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    logger.error("LLM hatası: %s", e)
                    
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def _tts_worker(self) -> None:
        """LLM'den gelen metni sese çevirir ve RTP Server'a gönderir."""
        while self._is_running:
            try:
                item = await asyncio.wait_for(self.tts_queue.get(), timeout=0.5)
                generation = getattr(item, "generation", self._interrupt_generation)
                text = getattr(item, "value", item)

                if generation != self._interrupt_generation:
                    continue

                if text is _HANGUP_SENTINEL:
                    await self._finish_assistant_hangup()
                    continue
                
                if self.interrupt_event.is_set():
                    continue
                generation = self._interrupt_generation
                    
                self.session.update_state(SessionState.SPEAKING)
                logger.info("🗣️ TTS üretiliyor ve gönderiliyor...")
                
                try:
                    async for chunk in self.tts.synthesize_stream(text):
                        if generation != self._interrupt_generation:
                            logger.info("🛑 TTS gönderimi kesildi (Barge-in).")
                            break # Ses gönderimini anında kes
                            
                        if self.send_audio_cb:
                            await self.send_audio_cb(chunk)
                            
                        await asyncio.sleep(len(chunk) / 16000.0)
                        self.session.total_audio_frames_sent += 1
                        
                    if generation == self._interrupt_generation:
                        self.session.update_state(SessionState.LISTENING)
                        
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error("TTS işlemi sırasında hata: %s", e)
                    self.session.update_state(SessionState.LISTENING)
                    
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def _finish_assistant_hangup(self) -> None:
        """Son TTS bittikten sonra doğrudan SIP kapanışını bir kez başlat."""
        if self._hangup_started:
            return
        self._hangup_started = True
        logger.info("Conversation completed")
        self.session.update_state(SessionState.CLOSED)
        logger.info("Waiting for final RTP packet")
        await asyncio.sleep(0.25)
        if self.on_hangup:
            logger.info("Preparing direct SIP call termination")
            await self.on_hangup()
        else:
            logger.error("Doğrudan SIP kapanış callback'i bağlı değil")

async def handle_voice_pipeline(
    reader: asyncio.StreamReader, writer
) -> None:
    """AudioSocket protokolünü kullanarak RTP üzerinden VoicePipeline'ı çalıştırır."""
    from app.voice.audio_socket import read_frame, encode_frame
    from app.voice.registry import registry
    from app.voice.audio_socket import resolve_business
    import uuid
    
    try:
        packet_type, payload = await asyncio.wait_for(read_frame(reader), timeout=5.0)
        if packet_type != 0x01:
            logger.error("İlk paket ID (0x01) değil tür: 0x%02x", packet_type)
            return
            
        call_uuid = str(uuid.UUID(bytes=payload))
        logger.info("VoicePipeline bağlantısı kabul edildi uuid=%s", call_uuid)
        
        context = await registry.wait(call_uuid)
        if not context:
            raise RuntimeError("FastAGI çağrı bağlamı bulunamadı")
            
        business = await resolve_business(context.did)
        if not business:
            raise RuntimeError("Aranan numara için etkin işletme bulunamadı")
            
        session = VoiceSession(
            session_id=call_uuid,
            caller_number=context.caller,
            business_slug=business["business_id"]
        )
        
        pipeline = VoicePipeline(session)
        
        async def send_audio_cb(pcm: bytes) -> None:
            if hasattr(writer, 'write') and not getattr(writer, '_closed', False):
                writer.write(encode_frame(0x10, pcm))
                if hasattr(writer, 'drain'):
                    await writer.drain()

        async def on_hangup() -> None:
            # DirectMediaWriter bu 0x00 karesini SIPServerProtocol.hangup()
            # çağrısına dönüştürür. Bu yol Asterisk kullanmaz.
            if hasattr(writer, 'write') and not getattr(writer, '_closed', False):
                writer.write(encode_frame(0x00))
                if hasattr(writer, 'drain'):
                    await writer.drain()

        pipeline.on_hangup = on_hangup
                    
        pipeline.start(send_audio_cb)
        
        try:
            while True:
                packet_type, payload = await read_frame(reader)
                if packet_type == 0x00:
                    break
                if packet_type == 0x10:
                    pipeline.feed_audio(payload)
        except asyncio.IncompleteReadError:
            pass
        finally:
            pipeline.stop()
            if hasattr(writer, 'close'):
                writer.close()
            
    except asyncio.TimeoutError:
        logger.error("VoicePipeline ilk paket (ID) okuma zaman aşımı")
    except Exception as e:
        logger.exception("VoicePipeline oturum hatası: %s", e)
