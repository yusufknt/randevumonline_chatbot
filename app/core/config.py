from __future__ import annotations

from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# os.getenv() ile vault ref çözümleyen get_secret() için de env yüklü olmalı.
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "randevum_chatbot"

    wa_graph_base_url: str = "https://graph.facebook.com/v25.0"
    wa_app_secret: str | None = None
    wa_verify_token: str = "dev-wa-verify-token"
    # Flow endpoint RSA key — PEM içeriği (WA_FLOW_PRIVATE_KEY) veya dosya yolu (WA_FLOW_PRIVATE_KEY_PATH)
    wa_flow_private_key: str | None = None
    wa_flow_private_key_path: str | None = None
    wa_flow_private_key_passphrase: str | None = None
    wa_flow_json_version: str = "7.3"
    # "draft" → test sırasında PUBLISHED olmayan Flow'u gönderebilir; prod'da boş bırak
    wa_flow_mode: str | None = None
    wa_flow_preview_business_slug: str | None = None

    ig_graph_base_url: str = "https://graph.instagram.com/v25.0"
    # Instagram App Secret — Facebook App Secret'tan FARKLI; IG product → API setup sayfasında bulunur
    ig_app_secret: str | None = None
    ig_verify_token: str = "dev-ig-verify-token"

    # ── AI (Groq / OpenAI-uyumlu) ──────────────────────────────────────────────
    # Instagram "Müşteri Temsilcisi" modunu çalıştıran LLM. ai_enabled=False iken
    # buton eski davranışına (telefon) düşer. Groq ücretsiz key:
    # console.groq.com/keys — base_url OpenAI-uyumlu olduğu için Ollama da kullanılabilir.
    ai_enabled: bool = False
    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.3-70b-versatile"
    ai_request_timeout_s: float = 30.0
    ai_max_tool_iterations: int = 5
    conversation_history_turns: int = 8

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
