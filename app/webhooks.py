from __future__ import annotations

import json
import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Request, Response

from app.channels import instagram as ig
from app.channels import whatsapp as wa
from app.channels.whatsapp.flow import handle_endpoint_request
from app.core.config import get_settings
from app.core.orchestrator import handle_instagram_payload, handle_whatsapp_payload

log = logging.getLogger(__name__)
router = APIRouter()


def _verify_subscription(
    mode: str | None, token: str | None, challenge: str | None, expected: str
) -> Response:
    if mode == "subscribe" and token == expected and challenge is not None:
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="verify_failed")


@router.get("/webhooks/whatsapp")
async def whatsapp_verify(
    hub_mode: str | None = Query(None, alias="hub.mode"),
    hub_verify_token: str | None = Query(None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(None, alias="hub.challenge"),
):
    return _verify_subscription(
        hub_mode, hub_verify_token, hub_challenge, get_settings().wa_verify_token
    )


@router.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request, background: BackgroundTasks):
    body = await request.body()
    if not wa.verify_signature(body, request.headers.get("X-Hub-Signature-256")):
        raise HTTPException(status_code=401, detail="invalid_signature")
    payload = await request.json()
    background.add_task(handle_whatsapp_payload, payload)
    return {"ok": True}


@router.post("/webhooks/whatsapp/flow")
async def whatsapp_flow_endpoint(request: Request):
    # 200 → encrypted base64, 421 decrypt fail, 427 token fail, 432 imza
    raw = await request.body()
    if not wa.verify_signature(raw, request.headers.get("X-Hub-Signature-256")):
        # 432 — request signature validation failed
        return Response(status_code=432)

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid_json")

    status, content = await handle_endpoint_request(body)
    if status >= 400:
        # Meta istemcisi 4xx'te gövdeye bakmıyor; debug log için içeri yazılır.
        if content:
            log.info("Flow endpoint %s: %s", status, content)
        return Response(status_code=status)
    if isinstance(content, str):
        return Response(content=content, media_type="text/plain", status_code=status)
    return Response(content=json.dumps(content),
                    media_type="application/json", status_code=status)


@router.get("/webhooks/instagram")
async def instagram_verify(
    hub_mode: str | None = Query(None, alias="hub.mode"),
    hub_verify_token: str | None = Query(None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(None, alias="hub.challenge"),
):
    return _verify_subscription(
        hub_mode, hub_verify_token, hub_challenge, get_settings().ig_verify_token
    )


@router.post("/webhooks/instagram")
async def instagram_webhook(request: Request, background: BackgroundTasks):
    body = await request.body()
    if not ig.verify_signature(body, request.headers.get("X-Hub-Signature-256")):
        raise HTTPException(status_code=401, detail="invalid_signature")
    payload = await request.json()
    background.add_task(handle_instagram_payload, payload)
    return {"ok": True}
