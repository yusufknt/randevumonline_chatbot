from __future__ import annotations

import re


def normalize_phone(value: str | None) -> str:
    """SIP URI/CallerID içinden numarayı E.164-benzeri güvenli biçime getirir."""
    if not value:
        return ""
    match = re.search(r"(?:sip:)?(\+?\d{7,15})", value)
    if not match:
        return ""
    raw = match.group(1)
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("00"):
        return "+" + digits[2:]
    if digits.startswith("0") and len(digits) == 11:
        return "+90" + digits[1:]
    if digits.startswith("90") and len(digits) == 12:
        return "+" + digits
    return ("+" if raw.startswith("+") else "") + digits


def redact_phone(value: str | None) -> str:
    number = normalize_phone(value)
    if len(number) < 7:
        return "[redacted]"
    return f"{number[:3]}***{number[-2:]}"
