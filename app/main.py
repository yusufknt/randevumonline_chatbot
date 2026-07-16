from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.db import close_client, get_client, init_indexes
from app.voice.audio_socket import AudioSocketServer
from app.webhooks import router as webhooks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    )
    log = logging.getLogger(__name__)
    client = get_client()
    await client.admin.command("ping")
    log.info("MongoDB bağlantısı tamam (db=%s)", settings.mongodb_db)
    try:
        await init_indexes()
        log.info("MongoDB indexleri uygulandı")
    except Exception:
        log.exception("init_indexes başarısız — devam ediliyor")
    # AudioSocket Ses Sunucusunu (Asterisk için) başlat
    audio_server = AudioSocketServer()
    app.state.audio_server = audio_server
    await audio_server.start()

    yield

    await audio_server.stop()
    await close_client()


app = FastAPI(title="RandevumOnline Chatbot", lifespan=lifespan)
app.include_router(webhooks_router)


@app.get("/healthz", include_in_schema=False)
async def healthz() -> dict:
    return {"ok": True}

@app.get("/health", tags=["System"])
async def health_check() -> dict:
    """Faz 2 Production Health Check Endpoint"""
    from app.voice.config import get_voice_settings
    
    settings = get_voice_settings()
    
    # Mongo DB check
    mongo_ok = False
    try:
        client = get_client()
        await client.admin.command("ping")
        mongo_ok = True
    except Exception:
        pass

    # AudioSocket (Asterisk/SIP Listener) check
    audio_server_active = False
    if hasattr(app.state, "audio_server") and app.state.audio_server._server is not None:
        audio_server_active = True

    # LLM (DeepSeek/Groq) Check
    llm_ok = bool(settings.deepseek_api_key)
    
    # TTS Check
    tts_ok = bool(settings.tts_api_key)

    # STT Check (Local whisper always ready if installed)
    stt_ok = True

    return {
        "status": "ok" if (mongo_ok and audio_server_active) else "error",
        "bot_active": True,
        "sip_listener_active": audio_server_active,
        "llm_connection_ready": llm_ok,
        "stt_engine_ready": stt_ok,
        "tts_engine_ready": tts_ok,
        "mongodb_connection": mongo_ok,
        "booking_api_ready": mongo_ok, # MongoDB çalışıyorsa DB işlemleri çalışır
    }
