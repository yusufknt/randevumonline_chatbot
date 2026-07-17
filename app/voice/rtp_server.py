"""
RTP ve SIP Sunucu Uygulaması (Asterisk olmadan)
"""

import asyncio
import logging
import struct
import time
from typing import Callable, Coroutine, Any
from app.voice.pipeline import VoicePipeline
from app.voice.models import VoiceSession, SessionState

logger = logging.getLogger(__name__)

# G.711 A-Law ve U-Law için lookup tabloları ve decode/encode fonksiyonları
# Python 3.13'te audioop kaldırıldığı için manuel olarak uygulandı.

# A-Law Decoder Table (PCMA)
ALAW_DECODE_TABLE = [0] * 256
for i in range(256):
    alaw = i ^ 0x55
    sign = (alaw & 0x80)
    exponent = (alaw & 0x70) >> 4
    mantissa = alaw & 0x0f
    
    sample = (mantissa << 4) + 8
    if exponent != 0:
        sample += 0x100
        sample <<= (exponent - 1)
        
    if sign == 0:
        ALAW_DECODE_TABLE[i] = sample
    else:
        ALAW_DECODE_TABLE[i] = -sample

def alaw2lin(data: bytes) -> bytes:
    """PCMA (A-Law) verisini 16-bit PCM verisine dönüştürür."""
    pcm_data = bytearray(len(data) * 2)
    for i in range(len(data)):
        val = ALAW_DECODE_TABLE[data[i]]
        struct.pack_into("<h", pcm_data, i * 2, val)
    return bytes(pcm_data)

def lin2alaw(data: bytes) -> bytes:
    """16-bit PCM (wav) verisini PCMA (A-Law) verisine dönüştürür."""
    alaw_data = bytearray(len(data) // 2)
    for i in range(len(alaw_data)):
        val = struct.unpack_from("<h", data, i * 2)[0]
        
        sign = 0x80 if val < 0 else 0x00
        if val < 0:
            val = -val
            
        if val > 32767:
            val = 32767
            
        exponent = 7
        mask = 0x4000
        
        if val < 256:
            exponent = 0
            mantissa = (val >> 4) & 0x0F
        else:
            while (val & mask) == 0 and exponent > 0:
                exponent -= 1
                mask >>= 1
            mantissa = (val >> (exponent + 3)) & 0x0F
            
        alaw = sign | (exponent << 4) | mantissa
        alaw ^= 0x55
        alaw_data[i] = alaw
    return bytes(alaw_data)


class RTPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, remote_ip: str, remote_port: int, pipeline: VoicePipeline):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.pipeline = pipeline
        self.transport = None
        self.sequence_number = 0
        self.timestamp = 0
        import random
        self.ssrc = random.randint(10000, 999999)
        self._greeting_sent = False
        
        self.audio_buffer = bytearray()
        self._silence_timer: asyncio.TimerHandle | None = None
        self._is_speaking = False
        self._silence_frames = 0

    def connection_made(self, transport):
        self.transport = transport
        logger.info("RTP Sunucusu başlatıldı ve bağlandı. Hedef: %s:%s", self.remote_ip, self.remote_port)
        
        self._greeting_sent = False
        # Çağrı bağlandıktan 1 saniye sonra karşılama mesajını otomatik gönder
        asyncio.create_task(self._delayed_greeting())
        
        # PBX'in çağrıyı düşürmesini engellemek için keepalive başlat
        self._keepalive_task = asyncio.create_task(self._rtp_keepalive())
        
    async def _rtp_keepalive(self):
        """Eğer uzun süre sessizlik olursa veya işlem sürüyorsa PBX'in çağrıyı kesmemesi için boş RTP yollar."""
        while self.transport and not self.transport.is_closing():
            await asyncio.sleep(2.0)
            if self.pipeline.session.state == SessionState.PROCESSING:
                # 40ms sessizlik paketi (ALAW'da 0xD5)
                silence = b'\xd5' * 320
                await self.send_audio(silence)
        
    async def _delayed_greeting(self):
        # Bekleme süresi tamamen kaldırıldı, anında başlat.
        await self._send_greeting()
        
    async def _send_greeting(self):
        if self._greeting_sent:
            return
        self._greeting_sent = True
        try:
            self.pipeline.session.update_state(SessionState.SPEAKING)
            
            import os
            greeting_file = os.path.join(os.path.dirname(__file__), "assets", "greeting.alaw")
            
            # Eğer dosya bulunamazsa (veya silinirse), loga uyarı yaz ve eski dinamik (on-the-fly) metoda dön
            if not os.path.exists(greeting_file):
                logger.warning("⚠️ Hazır açılış sesi (%s) bulunamadı! Eski davranışa dönülüyor (Dinamik TTS)...", greeting_file)
                greeting_text = "Merhaba. RandevumOnline yapay zeka asistanına hoş geldiniz. Size yardımcı olabilmem için lütfen randevu talebinizi söyleyebilirsiniz."
                async for chunk in self.pipeline.tts.synthesize_stream(greeting_text):
                    await self.send_audio(chunk)
                    await asyncio.sleep(len(chunk) / 8000.0)
                logger.info("✅ Dinamik açılış sesi müşteriye iletildi.")
                self.pipeline.session.update_state(SessionState.LISTENING)
                return
                    
            logger.info("🎵 Hazır açılış sesi (%s) ağa gönderiliyor...", greeting_file)
            with open(greeting_file, "rb") as f:
                alaw_data = f.read()
                
            chunk_size = 320
            for i in range(0, len(alaw_data), chunk_size):
                chunk = alaw_data[i:i+chunk_size]
                if not chunk:
                    break
                await self.send_audio(chunk)
                await asyncio.sleep(len(chunk) / 8000.0)
                
            logger.info("✅ Hazır açılış sesi müşteriye başarıyla iletildi. Normal STT dinleme moduna geçiliyor.")
            
            if self.pipeline.session.state == SessionState.SPEAKING:
                self.pipeline.session.update_state(SessionState.LISTENING)
        except Exception as e:
            logger.error("Greeting hatası: %s", e)
            self.pipeline.session.update_state(SessionState.LISTENING)

    def _process_buffered_audio(self):
        if not self.audio_buffer:
            return
        
        # Buffer kopyasını al ve temizle
        audio_data = bytes(self.audio_buffer)
        self.audio_buffer.clear()
        
        if len(audio_data) >= 8000: # En az 0.5 saniye ses
            logger.info("🎙️ Müşteri konuşması bitti, STT'ye gönderiliyor. (%d bytes)", len(audio_data))
            asyncio.create_task(
                self.pipeline.handle_incoming_audio(
                    audio_data,
                    self.send_audio
                )
            )

    def datagram_received(self, data, addr):
        # Update remote IP and port for symmetric RTP
        if self.remote_ip != addr[0] or self.remote_port != addr[1]:
            self.remote_ip = addr[0]
            self.remote_port = addr[1]
            logger.info("RTP Hedef adresi güncellendi (Symmetric RTP): %s:%s", self.remote_ip, self.remote_port)

        # RTP Header 12 byte'dır
        if len(data) < 12:
            return
        
        # RTP paketi
        payload_type = data[1] & 0x7F
        # Sadece PCMA (A-Law) = 8
        if payload_type == 8:
            # Asistan konuşurken müşteri sesini YÖKSAY (Half-Duplex mod - Barge-in kapalı)
            if self.pipeline.session.state == SessionState.SPEAKING:
                return
                
            payload = data[12:]
            pcm_audio = alaw2lin(payload)
            
            # Enerji hesabı (Ses Şiddeti)
            samples = struct.unpack(f"<{len(pcm_audio)//2}h", pcm_audio)
            energy = sum(abs(s) for s in samples) / len(samples)
            
            # Ses aktivitesi (VAD) mantığı
            if energy > 3000:
                self._is_speaking = True
                self._silence_frames = 0
                self.audio_buffer.extend(pcm_audio)
            elif self._is_speaking:
                # Konuşma devam ederken aradaki kısa sessizlikler (kelime araları)
                self.audio_buffer.extend(pcm_audio)
                self._silence_frames += 1
                
                # 100 frame (2 saniye) kesintisiz sessizlik olursa konuşma bitti say (müşteri yavaş konuşabilir)
                if self._silence_frames > 100:
                    self._is_speaking = False
                    self._process_buffered_audio()

    async def send_audio(self, pcm_data: bytes) -> None:
        """Pipeline tarafından üretilen ALAW verisini doğrudan yollar."""
        if not self.transport or self.transport.is_closing():
            return
            
        alaw_data = pcm_data
        
        # PCMA (A-Law) verisi her byte için 1 sample demektir.
        samples = len(alaw_data)
        
        # RTP header (12 bytes)
        # Version(2) Padding(0) Extension(0) CSRC_count(0) = 0x80
        # Marker(0) PayloadType(8 = PCMA) = 0x08
        header = struct.pack("!BBHII", 
                             0x80, 
                             0x08, 
                             self.sequence_number, 
                             self.timestamp, 
                             self.ssrc)
                             
        rtp_packet = header + alaw_data
        
        try:
            self.transport.sendto(rtp_packet, (self.remote_ip, self.remote_port))
            self.sequence_number = (self.sequence_number + 1) & 0xFFFF
            self.timestamp = (self.timestamp + samples) & 0xFFFFFFFF
        except Exception as e:
            logger.error("RTP Gönderme hatası: %s", e)
