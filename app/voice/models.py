"""
Ses Modülü (Voice Agent) veri modelleri ve durum tanımları.
"""

from __future__ import annotations

from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class SessionState(str, Enum):
    """Ses oturumunun anlık durumu."""

    CONNECTED = "connected"     # TCP bağlantısı kuruldu, UUID bekleniyor
    LISTENING = "listening"     # Müşteri konuşuyor, STT & VAD dinlemede
    PROCESSING = "processing"   # LLM ve araçlar randevu kontrolü yapıyor
    SPEAKING = "speaking"       # TTS ile müşteriye ses dinletiliyor
    CLOSED = "closed"           # Çağrı sonlandırıldı


class AudioSocketPacketType(int, Enum):
    """Asterisk AudioSocket protokol çerçeve (frame) tipleri."""

    TERMINATE = 0x00
    ID = 0x01
    AUDIO = 0x10
    ERROR = 0xFF


class AudioSocketPacket(BaseModel):
    """AudioSocket protokolünden ayrıştırılan bir veri paketi."""

    packet_type: AudioSocketPacketType
    payload: bytes


class VoiceSession(BaseModel):
    """Tek bir telefon aramasının oturum (session) bilgileri."""

    session_id: str
    caller_number: str | None = None
    business_slug: str | None = None
    state: SessionState = SessionState.CONNECTED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_audio_frames_received: int = 0
    total_audio_frames_sent: int = 0

    def update_state(self, new_state: SessionState) -> None:
        """Oturum durumunu güvenli şekilde günceller."""
        self.state = new_state
