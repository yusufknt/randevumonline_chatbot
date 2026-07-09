"""
Ses Modülü (Voice Agent) yapılandırma ayarları.
"""

from __future__ import annotations

from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class VoiceSettings(BaseSettings):
    """Ses modülünün ortam değişkenlerinden beslenen ayarları."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # AudioSocket Sunucu Ayarları
    voice_server_host: str = "0.0.0.0"
    voice_server_port: int = 8010
    voice_sample_rate: int = 8000  # Asterisk varsayılan olarak 8kHz PCM akıtır
    voice_frame_size: int = 320    # 20ms @ 8kHz, 16-bit PCM = 320 bayt

    # Oturum Zaman Aşımı ve Gecikme Sınırları
    voice_session_timeout_s: float = 300.0
    voice_log_level: str = "INFO"


@lru_cache
def get_voice_settings() -> VoiceSettings:
    """VoiceSettings tekil (singleton) örneğini döndürür."""
    return VoiceSettings()
