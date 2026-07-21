from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.core.db import close_client, get_client, init_indexes
from app.voice.audio_socket import start_audiosocket
from app.voice.config import get_voice_settings
from app.voice.fastagi import start_fastagi
from app.voice.stt import SpeechToTextEngine
from app.voice.tts import TextToSpeechEngine

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = get_voice_settings()
    logging.basicConfig(
        level=cfg.voice_log_level,
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
    )
    missing = cfg.validate_critical_connections()
    if missing:
        raise RuntimeError("Eksik kritik ayarlar: " + ", ".join(missing))
    await get_client().admin.command("ping")
    await init_indexes()
    await TextToSpeechEngine.startup()
    app.state.ready = False
    app.state.agi = await start_fastagi()
    app.state.audio = await start_audiosocket()
    await SpeechToTextEngine().warmup()
    app.state.ready = True
    log.info(
        "Voice service hazır FastAGI=%s AudioSocket=%s",
        cfg.voice_agi_port,
        cfg.voice_audiosocket_port,
    )
    yield
    app.state.ready = False
    app.state.agi.close()
    app.state.audio.close()
    await asyncio.gather(
        app.state.agi.wait_closed(), app.state.audio.wait_closed()
    )
    await TextToSpeechEngine.shutdown()
    await close_client()


app = FastAPI(title="RandevumOnline Voice Engine", lifespan=lifespan)


@app.get("/health")
async def health() -> dict:
    mongo = False
    try:
        await get_client().admin.command("ping")
        mongo = True
    except Exception:
        pass
    return {"ok": mongo, "ready": bool(getattr(app.state, "ready", False))}


@app.get("/ready")
async def ready() -> Response:
    value = bool(getattr(app.state, "ready", False))
    return Response(
        content='{"ready":true}' if value else '{"ready":false}',
        status_code=200 if value else 503,
        media_type="application/json",
    )


@app.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
