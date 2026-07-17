"""
Sunum/format yardımcıları — kanal mesajları ve tool sonuçları için ortak
metin biçimlendirme. Saf fonksiyonlar; domain veya DB bağımlılığı yok.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from zoneinfo import ZoneInfo

from bson.decimal128 import Decimal128

# availability.WEEKDAY_NAMES (İngilizce gün anahtarları) → Türkçe görünen ad.
WEEKDAY_TR = {
    "monday": "Pazartesi",
    "tuesday": "Salı",
    "wednesday": "Çarşamba",
    "thursday": "Perşembe",
    "friday": "Cuma",
    "saturday": "Cumartesi",
    "sunday": "Pazar",
}


def truncate(s: str, n: int) -> str:
    """n karakteri aşan metni '…' ile kısaltır (kanal başlık/limitleri için)."""
    if not s:
        return ""
    return s if len(s) <= n else s[: n - 1] + "…"


def money_str(v: Any) -> str:
    """Decimal128/Decimal/diğer para değerini sade string'e çevirir."""
    if v is None:
        return ""
    if isinstance(v, Decimal128):
        return str(v.to_decimal())
    if isinstance(v, Decimal):
        return str(v)
    try:
        return str(v.to_decimal()) if hasattr(v, "to_decimal") else str(v)
    except Exception:
        return str(v)


def format_price(value: Any, value_max: Any = None) -> str:
    """Müşteriye gösterilecek fiyat metni: '120₺' veya aralık '120₺ – 180₺'."""
    raw = money_str(value)
    if not raw:
        return "?"
    if "." in raw:
        raw = raw.rstrip("0").rstrip(".")
    if value_max is not None:
        raw_max = money_str(value_max)
        if raw_max:
            if "." in raw_max:
                raw_max = raw_max.rstrip("0").rstrip(".")
            if raw_max != raw:
                return f"{raw}₺ – {raw_max}₺"
    return f"{raw}₺"


def local_iso(dt: datetime, tz_name: str) -> str:
    """UTC/aware datetime → 'YYYY-MM-DD HH:MM' lokal saat string'i."""
    return dt.astimezone(ZoneInfo(tz_name)).strftime("%Y-%m-%d %H:%M")
