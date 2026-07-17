"""
Flow endpoint'i Meta olmadan local'de uçtan uca test eder.

Meta'nın Flow client'ını taklit eder:
  - RSA-OAEP-SHA256 ile AES-128 anahtarı public key'le sarar
  - AES-128-GCM ile data_exchange payload'unu şifreler
  - X-Hub-Signature-256 ile imzalar
  - POST /webhooks/whatsapp/flow
  - Yanıtı çözer, sıradaki ekran payload'unu alır

6 ekranı otomatik geçer (her seçimde ilk seçeneği alır):
  AD_SOYAD → SERVICE → STAFF → DAY → TIME → CONFIRM → SUCCESS

CLI:
    .venv/bin/uvicorn app.main:app --port 8000   # arka planda
    python -m scripts test-flow <flow_token>
    # flow_token yoksa: python -m scripts gen-test-token <slug>
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import sys
from pathlib import Path

import httpx
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import get_settings
from scripts.setup_env import C, banner

ROOT = Path(__file__).resolve().parent.parent


# ---------- Crypto ----------

def load_public_key() -> RSAPublicKey:
    pub_path = ROOT / "secrets" / "flow_public.pem"
    if not pub_path.exists():
        sys.exit(f"Public key yok: {pub_path}. `python -m scripts gen-keys` çalıştırın.")
    return serialization.load_pem_public_key(pub_path.read_bytes())


def encrypt_request(plaintext_obj: dict, public_key: RSAPublicKey):
    """Meta client'ın yaptığı şifrelemeyi taklit eder.
    Dönüş: (encrypted_body_dict, aes_key, iv)."""
    aes_key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    plaintext = json.dumps(plaintext_obj, ensure_ascii=False).encode("utf-8")
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    enc_aes = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return {
        "encrypted_flow_data": base64.b64encode(ciphertext).decode(),
        "encrypted_aes_key": base64.b64encode(enc_aes).decode(),
        "initial_vector": base64.b64encode(iv).decode(),
    }, aes_key, iv


def decrypt_response(b64_response: str, aes_key: bytes, iv: bytes) -> dict:
    flipped_iv = bytes(b ^ 0xFF for b in iv)
    aesgcm = AESGCM(aes_key)
    pt = aesgcm.decrypt(flipped_iv, base64.b64decode(b64_response), None)
    return json.loads(pt.decode("utf-8"))


def sign_body(body: bytes, app_secret: str) -> str:
    return "sha256=" + hmac.new(
        app_secret.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()


# ---------- Tek istek ----------

def do_exchange(
    endpoint: str,
    public_key: RSAPublicKey,
    app_secret: str,
    *,
    action: str,
    screen: str | None,
    data: dict | None,
    flow_token: str,
) -> dict:
    """Bir data_exchange POST'u atar, çözülmüş yanıtı döner."""
    request_payload = {
        "version": "3.0",
        "action": action,
        "flow_token": flow_token,
    }
    if screen is not None:
        request_payload["screen"] = screen
    if data is not None:
        request_payload["data"] = data

    enc_body, aes_key, iv = encrypt_request(request_payload, public_key)
    body = json.dumps(enc_body).encode("utf-8")
    sig = sign_body(body, app_secret)

    resp = httpx.post(
        endpoint,
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": sig,
        },
        timeout=30.0,
    )

    if resp.status_code != 200:
        print(f"{C.RED}HTTP {resp.status_code}{C.R}: {resp.text}")
        sys.exit(1)

    return decrypt_response(resp.text, aes_key, iv)


# ---------- Senaryo ----------

def run(flow_token: str, endpoint: str | None = None) -> int:
    s = get_settings()
    if not s.wa_app_secret:
        sys.exit("WA_APP_SECRET .env'de set edilmemiş; endpoint imzayı 432 ile reddeder.")

    public_key = load_public_key()
    if not endpoint:
        host = "localhost"
        port = 8000
        endpoint = f"http://{host}:{port}/webhooks/whatsapp/flow"
    app_secret = s.wa_app_secret

    print(f"{C.B}{C.CYAN}╭─────────────────────────────────────────╮{C.R}")
    print(f"{C.B}{C.CYAN}│  Flow endpoint local simulator          │{C.R}")
    print(f"{C.B}{C.CYAN}╰─────────────────────────────────────────╯{C.R}")
    print(f"  endpoint:   {endpoint}")
    print(f"  flow_token: {flow_token[:40]}…")

    # ---- Ping (health check) ----
    banner("0/7 — Health check (action=ping)")
    enc, aes_key, iv = encrypt_request(
        {"version": "3.0", "action": "ping"}, public_key
    )
    body = json.dumps(enc).encode()
    sig = sign_body(body, app_secret)
    resp = httpx.post(endpoint, content=body,
                      headers={"Content-Type": "application/json",
                               "X-Hub-Signature-256": sig},
                      timeout=10.0)
    if resp.status_code != 200:
        sys.exit(f"Ping fail: HTTP {resp.status_code}: {resp.text}")
    pong = decrypt_response(resp.text, aes_key, iv)
    if pong.get("data", {}).get("status") == "active":
        print(f"  {C.GREEN}✓ ping → active{C.R}")
    else:
        print(f"  {C.YELLOW}? ping yanıtı: {pong}{C.R}")

    # ---- 1. AD_SOYAD submit → SERVICE ----
    banner("1/7 — AD_SOYAD submit → SERVICE listesi")
    out = do_exchange(
        endpoint, public_key, app_secret,
        action="data_exchange", screen="AD_SOYAD",
        flow_token=flow_token,
        data={"first_name": "Test", "last_name": "Kullanıcı"},
    )
    print(f"  next screen: {C.GREEN}{out.get('screen')}{C.R}")
    services = out["data"]["services"]
    print(f"  {len(services)} hizmet dönmüş:")
    for sv in services[:5]:
        print(f"    - {sv['id']}  {sv['title']:30}  {sv.get('description','')}")
    chosen_service = services[0]
    print(f"  {C.MAG}→ seçim: {chosen_service['title']}{C.R}")

    # ---- 2. SERVICE submit → STAFF (veya tek personel → DAY) ----
    banner("2/7 — SERVICE submit → STAFF/DAY")
    out = do_exchange(
        endpoint, public_key, app_secret,
        action="data_exchange", screen="SERVICE",
        flow_token=flow_token,
        data={
            "first_name": "Test", "last_name": "Kullanıcı",
            "service_id": chosen_service["id"],
        },
    )
    print(f"  next screen: {C.GREEN}{out.get('screen')}{C.R}")
    next_screen = out["screen"]
    out_data = out["data"]

    if next_screen == "STAFF":
        staff_options = out_data["staff_options"]
        print(f"  {len(staff_options)} personel:")
        for st in staff_options[:5]:
            print(f"    - {st['id']}  {st['title']}")
        chosen_staff = staff_options[0]
        print(f"  {C.MAG}→ seçim: {chosen_staff['title']}{C.R}")

        # ---- 3. STAFF submit → DAY ----
        banner("3/7 — STAFF submit → DAY listesi")
        out = do_exchange(
            endpoint, public_key, app_secret,
            action="data_exchange", screen="STAFF",
            flow_token=flow_token,
            data={
                "first_name": "Test", "last_name": "Kullanıcı",
                "service_id": chosen_service["id"],
                "staff_id":   chosen_staff["id"],
            },
        )
        if out.get("screen") != "DAY":
            sys.exit(f"Beklenen DAY ekranı, gelen: {out}")
        out_data = out["data"]
        staff_id_for_next = chosen_staff["id"]
    else:
        # SERVICE → DAY (tek personel shortcut)
        print(f"  {C.DIM}(tek personel — STAFF ekranı atlandı){C.R}")
        staff_id_for_next = out_data.get("staff_id", "any")

    # ---- DAY ----
    banner(f"4/7 — DAY listesi  ({len(out_data['days'])} gün)")
    days = out_data["days"]
    for d in days[:5]:
        print(f"    - {d['id']}  {d['title']}")
    chosen_day = days[0]
    print(f"  {C.MAG}→ seçim: {chosen_day['title']}{C.R}")

    out = do_exchange(
        endpoint, public_key, app_secret,
        action="data_exchange", screen="DAY",
        flow_token=flow_token,
        data={
            "first_name": "Test", "last_name": "Kullanıcı",
            "service_id": chosen_service["id"],
            "staff_id":   staff_id_for_next,
            "day":        chosen_day["id"],
        },
    )
    if out.get("screen") != "TIME":
        sys.exit(f"Beklenen TIME ekranı, gelen: {out}")
    times = out["data"]["times"]

    # ---- TIME ----
    banner(f"5/7 — TIME listesi  ({len(times)} slot)")
    for t in times[:5]:
        print(f"    - {t['id']}  {t['title']}")
    chosen_time = times[0]
    print(f"  {C.MAG}→ seçim: {chosen_time['title']}{C.R}")

    out = do_exchange(
        endpoint, public_key, app_secret,
        action="data_exchange", screen="TIME",
        flow_token=flow_token,
        data={
            "first_name": "Test", "last_name": "Kullanıcı",
            "service_id": chosen_service["id"],
            "staff_id":   staff_id_for_next,
            "day":        chosen_day["id"],
            "time":       chosen_time["id"],
        },
    )
    if out.get("screen") != "CONFIRM":
        sys.exit(f"Beklenen CONFIRM ekranı, gelen: {out}")
    confirm_data = out["data"]

    # ---- CONFIRM ekranını göster ----
    banner("6/7 — CONFIRM özeti")
    print(f"  Ad Soyad : {confirm_data.get('full_name')}")
    print(f"  Hizmet   : {confirm_data.get('service_name')}")
    print(f"  Personel : {confirm_data.get('staff_name')}")
    print(f"  Tarih    : {confirm_data.get('day_label')}")
    print(f"  Saat     : {confirm_data.get('time_range')}")
    print(f"  Süre     : {confirm_data.get('duration_minutes')} dk")

    # ---- CONFIRM submit → SUCCESS ----
    banner("7/7 — CONFIRM submit → SUCCESS (randevu yarat)")
    out = do_exchange(
        endpoint, public_key, app_secret,
        action="data_exchange", screen="CONFIRM",
        flow_token=flow_token,
        data={
            "first_name": confirm_data.get("first_name", "Test"),
            "last_name":  confirm_data.get("last_name", "Kullanıcı"),
            "service_id": confirm_data["service_id"],
            "service_name": confirm_data["service_name"],
            "staff_id":   confirm_data["staff_id"],
            "staff_name": confirm_data.get("staff_name", ""),
            "day":        confirm_data["day"],
            "time":       confirm_data["time"],
            "notes":      "Local test notu",
        },
    )

    if out.get("screen") == "SUCCESS":
        params = out["data"]["extension_message_response"]["params"]
        print(f"  {C.GREEN}{C.B}✓ Randevu oluşturuldu!{C.R}")
        print(f"  appointment_id   : {params.get('appointment_id')}")
        print(f"  service_name     : {params.get('service_name')}")
        print(f"  staff_name       : {params.get('staff_name')}")
        print(f"  start_time_local : {params.get('start_time_local')}")
        print(f"  duration_minutes : {params.get('duration_minutes')}")
        print(f"\n{C.DIM}Doğrulamak için:{C.R}")
        print(f"  echo 'db.appointments.findOne({{_id:ObjectId(\"{params['appointment_id']}\")}})' | mongosh randevum_chatbot")
        return 0
    elif out.get("screen") == "CONFIRM" and out["data"].get("error_message"):
        print(f"  {C.YELLOW}CONFIRM → error_message:{C.R} {out['data']['error_message']}")
        return 1
    else:
        print(f"  {C.RED}Beklenmedik yanıt:{C.R}")
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 1


