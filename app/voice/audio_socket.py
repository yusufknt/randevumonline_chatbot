"""
Asterisk AudioSocket Protokolü Asenkron TCP Sunucusu.

AudioSocket Çerçeve Formatı:
  - 1 Bayt : Paket Tipi (0x00 Terminate, 0x01 ID, 0x10 Audio, 0xFF Error)
  - 2 Bayt : Yük Uzunluğu (Big-Endian unsigned short)
  - N Bayt : Veri Yükü (Payload)
"""

from __future__ import annotations

import asyncio
import logging
import struct
from typing import Any

from app.voice.config import get_voice_settings
from app.voice.models import (
    AudioSocketPacket,
    AudioSocketPacketType,
    SessionState,
    VoiceSession,
)

logger = logging.getLogger(__name__)


class AudioSocketServer:
    """Asterisk VoIP santraliyle haberleşen asenkron TCP sunucusu."""

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        settings = get_voice_settings()
        self.host = host or settings.voice_server_host
        self.port = port or settings.voice_server_port
        self._server: asyncio.Server | None = None
        self._active_sessions: dict[str, VoiceSession] = {}
        # Pipeline artık her oturum (ID paketi) için ayrı ayrı başlatılacaktır.

    async def start(self) -> None:
        """TCP sunucusunu başlatır."""
        self._server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port,
        )
        logger.info("🟢 AudioSocket Sunucusu başladı -> tcp://%s:%s (Asterisk/SIP aramaları için dinleniyor)", self.host, self.port)

    async def stop(self) -> None:
        """TCP sunucusunu kapatır ve aktif bağlantıları sonlandırır."""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
            logger.info("AudioSocket Sunucusu kapatıldı")

    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """Asterisk'ten gelen her bir TCP bağlantısını yöneten işleyici."""
        client_addr = writer.get_extra_info("peername")
        remote_ip = client_addr[0] if client_addr else "Unknown"
        remote_port = client_addr[1] if client_addr else "Unknown"
        
        logger.info("📞 [Yeni Çağrı] AudioSocket bağlantısı alındı. Remote IP: %s, Remote Port: %s", remote_ip, remote_port)

        session: VoiceSession | None = None
        pipeline = None

        try:
            while True:
                packet = await self._read_packet(reader)
                if packet is None:
                    break

                if packet.packet_type == AudioSocketPacketType.TERMINATE:
                    logger.info("Çağrı sonlandırma sinyali alındı: %s", client_addr)
                    break

                elif packet.packet_type == AudioSocketPacketType.ID:
                    session_id = packet.payload.decode("utf-8", errors="replace")
                    session = VoiceSession(session_id=session_id)
                    self._active_sessions[session_id] = session
                    
                    # Her oturum için yeni bir pipeline oluştur (Böylece session'a özel durum yönetimi sağlanır)
                    from app.voice.pipeline import VoicePipeline
                    pipeline = VoicePipeline(session=session)
                    
                    logger.info("✅ Oturum kimliği doğrulandı: session_id=%s", session_id)

                elif packet.packet_type == AudioSocketPacketType.AUDIO:
                    if session:
                        if session.total_audio_frames_received == 0:
                            logger.info("▶️ Ses paketi alınmaya başlandı. (Session: %s)", session.session_id)
                            
                        session.total_audio_frames_received += 1
                        # İlk birkaç pakette log yazdıralım (spam olmaması için modulo kullanabiliriz)
                        if session.total_audio_frames_received % 150 == 1:
                            logger.debug("🔊 RTP/AudioSocket ses alınıyor... (Paket: %s)", session.total_audio_frames_received)

                        # Eğer STT/LLM/TTS akışı aktifse pipeline çalıştır, değilse echo ile devam et
                        if pipeline:
                            await pipeline.handle_incoming_audio(
                                packet.payload,
                                lambda chunk: self.send_audio(writer, chunk),
                            )
                        else:
                            await self.send_audio(writer, packet.payload)
                            session.total_audio_frames_sent += 1

                elif packet.packet_type == AudioSocketPacketType.ERROR:
                    logger.warning("Asterisk hata paketi gönderdi: %s", client_addr)
                    break

        except asyncio.CancelledError:
            logger.info("⚠️ Bağlantı iptal edildi (Remote: %s:%s)", remote_ip, remote_port)
        except ConnectionResetError:
            logger.warning("🔌 İstemci bağlantıyı zorla kapattı (TCP Reset). (Remote: %s:%s)", remote_ip, remote_port)
        except Exception as e:
            logger.exception("❌ İstemci işlenirken beklenmeyen hata oluştu (Sunucu çökmeyecek): %s:%s - Hata: %s", remote_ip, remote_port, str(e))
        finally:
            if session and session.session_id in self._active_sessions:
                session.update_state(SessionState.CLOSED)
                del self._active_sessions[session.session_id]
            writer.close()
            await writer.wait_closed()
            logger.info("🛑 Bağlantı tamamen kapatıldı (Çağrı sonlandı): %s:%s", remote_ip, remote_port)

    @staticmethod
    async def _read_packet(reader: asyncio.StreamReader) -> AudioSocketPacket | None:
        """Ağ akışından 3 baytlık başlığı okur ve paketi ayrıştırır."""
        try:
            header = await reader.readexactly(3)
        except asyncio.IncompleteReadError:
            return None

        try:
            packet_type_raw, length = struct.unpack("!BH", header)
        except struct.error as e:
            logger.error("Bozuk paket başlığı ayrıştırılamadı (struct.error): %s", str(e))
            return None

        try:
            packet_type = AudioSocketPacketType(packet_type_raw)
        except ValueError:
            logger.error("Bilinmeyen paket tipi alındı: 0x%02X", packet_type_raw)
            return None

        try:
            payload = await reader.readexactly(length)
        except asyncio.IncompleteReadError:
            logger.error("Eksik veri yükü (payload) okundu. Beklenen: %s bytes", length)
            return None

        return AudioSocketPacket(packet_type=packet_type, payload=payload)

    @staticmethod
    async def send_audio(writer: asyncio.StreamWriter, pcm_data: bytes) -> None:
        """Belirtilen PCM ses yükünü AudioSocket formatında paketleyip gönderir."""
        header = struct.pack(
            "!BH",
            AudioSocketPacketType.AUDIO.value,
            len(pcm_data),
        )
        writer.write(header + pcm_data)
        await writer.drain()
