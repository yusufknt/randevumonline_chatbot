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

    # SIP Sunucu Ayarları
    voice_server_host: str = "0.0.0.0"
    voice_server_port: int = 8010
    voice_external_ip: str | None = None
    
    # RTP Sunucu Ayarları
    rtp_start_port: int = 10000
    rtp_end_port: int = 10100
    
    voice_sample_rate: int = 8000  # 8kHz
    voice_frame_size: int = 320    # 20ms @ 8kHz, 16-bit PCM = 320 bayt

    # Oturum Zaman Aşımı ve Gecikme Sınırları
    voice_session_timeout_s: float = 300.0
    voice_log_level: str = "INFO"

    # DeepSeek LLM Ayarları
    deepseek_api_key: str | None = None
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    ai_request_timeout_s: float = 15.0

    # Görüşme Süresi ve Limit Koruması (Graceful Exit / Fallback)
    voice_max_call_duration_s: float = 180.0
    voice_max_turns: int = 15
    voice_timeout_message: str = (
        "Görüşme süremizin sonuna geldik, randevu talebinizle ilgili detayları "
        "SMS olarak ileteceğiz. İyi günler dileriz."
    )

    # Yeni Voice API (TTS) Ayarları
    tts_api_key: str | None = None
    tts_api_gender: str = "erkek"
    tts_api_emotion: str = "motivasyon"
    tts_api_base_url: str = "https://voiceapi.createupload.com"



@lru_cache
def get_voice_settings() -> VoiceSettings:
    """VoiceSettings tekil (singleton) örneğini döndürür."""
    return VoiceSettings()
