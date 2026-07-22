from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.core.db import close_client, get_client, init_indexes
from app.core.session_cache import (
    close_voice_session_cache,
    get_voice_session_cache,
)
from app.voice.config import get_voice_settings
from app.voice.sip_server import start_sip_server
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
    redis_ok = await get_voice_session_cache().ping()
    if not redis_ok:
        log.warning("Redis kullanılamıyor; voice cache L1/MongoDB fallback ile çalışacak")
    await TextToSpeechEngine.startup()
    app.state.ready = False
    app.state.sip_transport, app.state.sip = await start_sip_server()
    await SpeechToTextEngine().warmup()
    app.state.ready = True
    log.info(
        "Voice service hazır DirectSIP=udp/%s RTP=%s-%s",
        cfg.voice_server_port,
        cfg.rtp_start_port,
        cfg.rtp_end_port,
    )
    yield
    app.state.ready = False
    await app.state.sip.close()
    await TextToSpeechEngine.shutdown()
    await close_voice_session_cache()
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
    redis = await get_voice_session_cache().ping()
    ready_value = bool(getattr(app.state, "ready", False))
    return {
        "ok": mongo,
        "ready": ready_value,
        "redis": redis,
        "degraded": bool(mongo and ready_value and not redis),
    }


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
