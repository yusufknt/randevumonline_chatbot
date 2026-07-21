"""
Ses Modülü (Voice Agent) yapılandırma ayarları.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

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
    voice_agi_host: str = "127.0.0.1"
    voice_agi_port: int = 4573
    voice_audiosocket_host: str = "127.0.0.1"
    voice_audiosocket_port: int = 9019
    voice_health_host: str = "127.0.0.1"
    voice_health_port: int = 9020
    voice_default_business_slug: str | None = None
    voice_max_concurrent_calls: int = 3

    # Oturum Zaman Aşımı ve Gecikme Sınırları
    voice_session_timeout_s: float = 300.0
    voice_log_level: str = "INFO"
    voice_metrics_retention_days: int = 30
    voice_greeting_pcm: str = "app/voice/assets/greeting.slin"

    # Yerel ve ücretsiz ses işleme
    voice_vad_model: str = "app/voice/assets/models/silero_vad.onnx"
    voice_vad_start_probability: float = 0.50
    voice_vad_barge_probability: float = 0.72
    voice_vad_start_ms: int = 64
    voice_vad_barge_ms: int = 96
    voice_vad_end_silence_ms: int = 384
    voice_vad_preroll_ms: int = 256
    voice_vad_energy_floor: float = 350.0
    voice_vad_barge_energy_floor: float = 900.0
    voice_vad_energy_multiplier: float = 3.0
    voice_vad_min_voiced_ms: int = 192
    voice_max_utterance_s: float = 12.0
    # 8 kHz telefon sesinde base model özellikle tarih eklerini karıştırabiliyor.
    # Small model hâlâ yerel/ücretsizdir ve kısa ifadelerde kabul edilebilir hızdadır.
    voice_stt_fast_model: str = "small"
    # Small model hızlı ilk geçişi yapar; düşük güvenli telefon sesi daha güçlü
    # modelle doğrulanır. Turbo, large-v3 doğruluğunu daha düşük gecikmeyle verir.
    voice_stt_accurate_model: str = "large-v3-turbo"
    voice_stt_accurate_confidence_threshold: float = 0.60
    voice_stt_fast_workers: int = 2
    voice_stt_accurate_workers: int = 1

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
    tts_cookie_file: str | None = "cookies.txt"
    tts_api_gender: str = "erkek"
    tts_api_emotion: str = "motivasyon"
    tts_api_base_url: str = "https://voiceapi.createupload.com"

    def validate_critical_connections(self) -> list[str]:
        """Canlı geçiş için eksik kritik ayar adlarını, değerleri açmadan döndürür."""
        missing: list[str] = []
        if not self.deepseek_api_key:
            missing.append("DEEPSEEK_API_KEY")
        if not self.deepseek_base_url:
            missing.append("DEEPSEEK_BASE_URL")
        if not self.tts_api_base_url:
            missing.append("TTS_API_BASE_URL")
        cookie = Path(self.tts_cookie_file).expanduser() if self.tts_cookie_file else None
        if not self.tts_api_key and not (cookie and cookie.is_file()):
            missing.append("TTS_API_KEY veya TTS_COOKIE_FILE")
        return missing



@lru_cache
def get_voice_settings() -> VoiceSettings:
    """VoiceSettings tekil (singleton) örneğini döndürür."""
    return VoiceSettings()
