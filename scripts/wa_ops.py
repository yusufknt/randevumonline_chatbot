"""WhatsApp Flow kurulum işlemleri: RSA anahtarları, Meta API çağrıları, MongoDB güncellemeleri."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pymongo import MongoClient

from app.channels.whatsapp.flow_manifest import build_flow_json
from app.core.config import get_settings

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SECRETS_DIR = ROOT / "secrets"
DEFAULT_PUB_PATH = DEFAULT_SECRETS_DIR / "flow_public.pem"


# ── RSA anahtarları ────────────────────────────────────────────────────────────

def generate_keypair(
    secrets_dir: Path = DEFAULT_SECRETS_DIR,
    *,
    overwrite: bool = False,
) -> tuple[Path, Path]:
    secrets_dir.mkdir(exist_ok=True)
    priv_path = secrets_dir / "flow_private.pem"
    pub_path = secrets_dir / "flow_public.pem"

    if (priv_path.exists() or pub_path.exists()) and not overwrite:
        raise FileExistsError(
            f"Var olan anahtar üzerine yazmıyorum. Önce {priv_path.name} ve "
            f"{pub_path.name} dosyalarını silin veya overwrite=True kullanın."
        )

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    priv_path.write_bytes(priv_pem)
    pub_path.write_bytes(pub_pem)
    os.chmod(priv_path, 0o600)
    return priv_path, pub_path


# ── Meta API ───────────────────────────────────────────────────────────────────

@dataclass
class UploadResult:
    status_code: int
    body: str
    ok: bool


def read_public_pem(path: Path = DEFAULT_PUB_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Public key bulunamadı: {path}")
    return path.read_text(encoding="utf-8")


def upload_public_key(
    phone_number_id: str,
    access_token: str,
    pub_pem: str,
    *,
    api_version: str = "v25.0",
    timeout_s: float = 60.0,
) -> UploadResult:
    url = (
        f"https://graph.facebook.com/{api_version}/"
        f"{phone_number_id}/whatsapp_business_encryption"
    )
    with httpx.Client(timeout=timeout_s) as client:
        resp = client.post(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            data={"business_public_key": pub_pem},
        )
    return UploadResult(status_code=resp.status_code, body=resp.text, ok=resp.status_code < 400)


def subscribe_app_to_waba(
    waba_id: str,
    access_token: str,
    *,
    api_version: str = "v25.0",
    timeout_s: float = 60.0,
) -> UploadResult:
    # test number'lar Meta'nın default app'ine bağlıdır; bu çağrı mevcut app'i ekler — idempotent
    url = f"https://graph.facebook.com/{api_version}/{waba_id}/subscribed_apps"
    with httpx.Client(timeout=timeout_s) as client:
        resp = client.post(url, headers={"Authorization": f"Bearer {access_token}"})
    return UploadResult(status_code=resp.status_code, body=resp.text, ok=resp.status_code < 400)


@dataclass
class CreateFlowResult:
    flow_id: str | None
    create_response: dict
    publish_status: int | None
    publish_body: str | None
    validation_errors: list | None


def create_flow(
    waba_id: str,
    access_token: str,
    public_base_url: str,
    *,
    flow_name: str = "randevu_form_v1",
    api_version: str = "v25.0",
    timeout_s: float = 60.0,
) -> CreateFlowResult:
    public_base = public_base_url.rstrip("/")
    endpoint_uri = f"{public_base}/webhooks/whatsapp/flow"
    flow_json_str = build_flow_json()

    create_url = f"https://graph.facebook.com/{api_version}/{waba_id}/flows"
    create_body = {
        "name": flow_name,
        "categories": ["APPOINTMENT_BOOKING"],
        "flow_json": flow_json_str,
        "endpoint_uri": endpoint_uri,
    }

    with httpx.Client(timeout=timeout_s) as client:
        resp = client.post(
            create_url,
            headers={"Authorization": f"Bearer {access_token}"},
            json=create_body,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"Flow create HTTP {resp.status_code}: {resp.text}")
        out = resp.json()
        flow_id = out.get("id")
        validation_errors = out.get("validation_errors")

        if validation_errors:
            return CreateFlowResult(
                flow_id=None, create_response=out,
                publish_status=None, publish_body=None,
                validation_errors=validation_errors,
            )
        if not flow_id:
            raise RuntimeError("Flow create yanıtında id yok")

        publish_url = f"https://graph.facebook.com/{api_version}/{flow_id}/publish"
        resp2 = client.post(publish_url, headers={"Authorization": f"Bearer {access_token}"})
        return CreateFlowResult(
            flow_id=flow_id, create_response=out,
            publish_status=resp2.status_code, publish_body=resp2.text,
            validation_errors=None,
        )


# ── MongoDB ────────────────────────────────────────────────────────────────────

@dataclass
class UpdateResult:
    matched: int
    modified: int
    business: dict | None


def update_business_wa_channel(
    slug: str,
    *,
    flow_id: str | None = None,
    phone_number_id: str | None = None,
    business_account_id: str | None = None,
) -> UpdateResult:
    update: dict[str, str] = {}
    if flow_id is not None:
        update["channels.whatsapp.flow_id"] = flow_id
    if phone_number_id is not None:
        update["channels.whatsapp.phone_number_id"] = phone_number_id
    if business_account_id is not None:
        update["channels.whatsapp.business_account_id"] = business_account_id

    s = get_settings()
    client = MongoClient(s.mongodb_url)
    try:
        db = client[s.mongodb_db]

        if update:
            res = db.businesses.update_one({"business_id": slug}, {"$set": update})
            matched, modified = res.matched_count, res.modified_count
        else:
            matched = db.businesses.count_documents({"business_id": slug})
            modified = 0

        biz = db.businesses.find_one(
            {"business_id": slug},
            {"name": 1, "channels.whatsapp": 1},
        )
    finally:
        client.close()
    return UpdateResult(matched=matched, modified=modified, business=biz)
