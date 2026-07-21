"""
FAZ 3 - Asenkron Kuyruk Mimarisi ile Doğal Konuşma (Full Duplex / Barge-In)
"""

from __future__ import annotations

import asyncio
import logging
import struct
from typing import Any, Callable, Coroutine

from app.voice.llm import VoiceLLMEngine
from app.voice.models import SessionState, VoiceSession
from app.voice.stt import SpeechToTextEngine
from app.voice.tts import TextToSpeechEngine

logger = logging.getLogger(__name__)


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
        self.tts_queue: asyncio.Queue[str] = asyncio.Queue()
        
        # Kontrol Event'leri (Interrupt/Barge-in)
        self.interrupt_event = asyncio.Event()
        
        # Callback
        self.send_audio_cb: Callable[[bytes], Coroutine[Any, Any, None]] | None = None
        
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
        self._workers.append(asyncio.create_task(self._llm_worker()))
        self._workers.append(asyncio.create_task(self._tts_worker()))
        
        logger.info("🟢 Pipeline başlatıldı. (session_id=%s)", self.session.session_id)

    def stop(self) -> None:
        """Pipeline işçilerini durdurur."""
        self._is_running = False
        for task in self._workers:
            task.cancel()
        logger.info("🛑 Pipeline durduruldu. (session_id=%s)", self.session.session_id)

    def feed_audio(self, pcm_audio: bytes) -> None:
        """RTP Server'dan gelen ham ses paketlerini kuyruğa ekler."""
        if self._is_running:
            self.audio_queue.put_nowait(pcm_audio)

    def trigger_interrupt(self) -> None:
        """Kullanıcı konuştuğunda STT/TTS ve LLM'i susturup sıfırlar."""
        if not self.interrupt_event.is_set():
            logger.info("🚨 KULLANICI ARAYA GİRDİ (Barge-in). AI susturuluyor... (session_id=%s)", self.session.session_id)
            self.interrupt_event.set()
            
            # Eski üretilmiş TTS ve LLM isteklerini temizle
            while not self.tts_queue.empty():
                try: self.tts_queue.get_nowait()
                except asyncio.QueueEmpty: pass
                
            while not self.llm_queue.empty():
                try: self.llm_queue.get_nowait()
                except asyncio.QueueEmpty: pass
                
            self.session.update_state(SessionState.LISTENING)

    async def _audio_worker(self) -> None:
        """Sesi biriktirir, VAD ile kesme yapar ve sessizlikte STT'ye yollar."""
        audio_buffer = bytearray()
        silence_frames = 0
        is_speaking = False
        
        while self._is_running:
            try:
                # Küçük zaman aşımlarıyla kuyruktan oku ki iptal durumlarında asılı kalmasın
                pcm_audio = await asyncio.wait_for(self.audio_queue.get(), timeout=0.1)
                
                # Enerji hesabı (VAD)
                samples = struct.unpack(f"<{len(pcm_audio)//2}h", pcm_audio)
                energy = sum(abs(s) for s in samples) / len(samples)
                
                if energy > 2000: # Kullanıcı konuşuyor (daha hassas)
                    self.trigger_interrupt()
                    
                    is_speaking = True
                    silence_frames = 0
                    audio_buffer.extend(pcm_audio)
                elif is_speaking:
                    silence_frames += 1
                    audio_buffer.extend(pcm_audio)
                    
                    # 75 frame (~1.5 sn sessizlik) ise cümleyi bitir (Erken kesilmeyi önler)
                    if silence_frames > 75:
                        is_speaking = False
                        
                        if len(audio_buffer) >= 8000: # En az 0.5 saniye ses varsa STT yap
                            audio_to_process = bytes(audio_buffer)
                            # Hızlıca STT task'ına at, bloklamasın
                            asyncio.create_task(self._process_stt(audio_to_process))
                            
                        audio_buffer.clear()
                        
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Audio Worker hatası: %s", e)

    async def _process_stt(self, pcm_audio: bytes) -> None:
        self.session.update_state(SessionState.PROCESSING)
        self.interrupt_event.clear() # Yeni işlem başlıyor, interrupt'ı sıfırla
        
        try:
            transcript = await self.stt.transcribe(pcm_audio)
            if transcript and transcript.text and not self.interrupt_event.is_set():
                logger.info("✅ STT tamamlandı: '%s'", transcript.text)
                await self.llm_queue.put(transcript.text)
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
                    
                logger.info("⏳ LLM'e istek gönderiliyor...")
                try:
                    async for sentence in self.llm.generate_response(text):
                        if self.interrupt_event.is_set():
                            logger.info("🛑 LLM yayını araya girilerek İPTAL edildi.")
                            break
                            
                        if sentence:
                            logger.info("🧠 LLM cümlesi: '%s'", sentence)
                            await self.tts_queue.put(sentence)
                            
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
                text = await asyncio.wait_for(self.tts_queue.get(), timeout=0.5)
                
                if self.interrupt_event.is_set():
                    continue
                    
                self.session.update_state(SessionState.SPEAKING)
                logger.info("🗣️ TTS üretiliyor ve gönderiliyor...")
                
                try:
                    async for chunk in self.tts.synthesize_stream(text):
                        if self.interrupt_event.is_set():
                            logger.info("🛑 TTS gönderimi kesildi (Barge-in).")
                            break # Ses gönderimini anında kes
                            
                        if self.send_audio_cb:
                            await self.send_audio_cb(chunk)
                            
                        await asyncio.sleep(len(chunk) / 8000.0)
                        self.session.total_audio_frames_sent += 1
                        
                    if not self.interrupt_event.is_set():
                        self.session.update_state(SessionState.LISTENING)
                        
                        # Kapanış etiketi kontrolü (llm.py'den)
                        if hasattr(self.llm, "is_session_closed") and self.llm.is_session_closed:
                            logger.info("Conversation completed")
                            self.session.update_state(SessionState.CLOSED)
                            
                            logger.info("Preparing call termination")
                            logger.info("Waiting for final RTP packet")
                            await asyncio.sleep(1.0)
                            
                            if hasattr(self, 'on_hangup') and self.on_hangup:
                                asyncio.create_task(self.on_hangup())
                                
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error("TTS işlemi sırasında hata: %s", e)
                    self.session.update_state(SessionState.LISTENING)
                    
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
