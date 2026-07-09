from __future__ import annotations

import base64
import json
import logging
from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

log = logging.getLogger(__name__)


@dataclass
class DecryptedRequest:
    payload: dict
    aes_key: bytes
    iv: bytes


def _load_private_key(pem: str, passphrase: str | None):
    pwd = passphrase.encode("utf-8") if passphrase else None
    return serialization.load_pem_private_key(pem.encode("utf-8"), password=pwd)


def decrypt_request(
    body: dict,
    private_key_pem: str,
    private_key_passphrase: str | None = None,
) -> DecryptedRequest:
    enc_flow = base64.b64decode(body["encrypted_flow_data"])
    enc_aes = base64.b64decode(body["encrypted_aes_key"])
    iv = base64.b64decode(body["initial_vector"])

    private_key = _load_private_key(private_key_pem, private_key_passphrase)
    aes_key = private_key.decrypt(
        enc_aes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    if len(aes_key) != 16:
        raise ValueError(f"AES key boyu beklenmedik: {len(aes_key)}")

    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(iv, enc_flow, None)
    payload = json.loads(plaintext.decode("utf-8"))
    return DecryptedRequest(payload=payload, aes_key=aes_key, iv=iv)


def encrypt_response(response: dict, aes_key: bytes, iv: bytes) -> str:
    flipped_iv = bytes(b ^ 0xFF for b in iv)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(
        flipped_iv,
        json.dumps(response, ensure_ascii=False).encode("utf-8"),
        None,
    )
    return base64.b64encode(ciphertext).decode("utf-8")
