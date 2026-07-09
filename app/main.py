from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.db import close_client, get_client, init_indexes
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
    yield
    await close_client()


app = FastAPI(title="RandevumOnline Chatbot", lifespan=lifespan)
app.include_router(webhooks_router)


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}
