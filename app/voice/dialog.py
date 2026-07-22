from __future__ import annotations

import json
import logging
import re
import asyncio
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

import httpx
from rapidfuzz import fuzz, process

from app.core.availability import (
    WEEKDAY_NAMES,
    compute_available_slots,
    is_special_closure,
    windows_for_day,
)
from app.core.booking import cancel_appointment, create_appointment, reschedule_appointment
from app.core.db import (
    get_db,
    upsert_conversation,
    upsert_customer_by_phone,
)
from app.core.session_cache import get_voice_session_cache
from app.voice.config import get_voice_settings
from app.voice.llm import parse_target_date_tr
from app.voice.message_buffer import ConversationMessageBuffer

log = logging.getLogger(__name__)

MONTHS_TR = (
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
)


def _date_spoken(value: date) -> str:
    return f"{value.day} {MONTHS_TR[value.month]}"


def _slot_ranges(
    slots: list[datetime], tz: ZoneInfo, duration_minutes: int, step_minutes: int = 15
) -> list[tuple[datetime, datetime]]:
    """Bitişik randevu başlangıçlarını konuşulabilir boş zaman aralıklarına çevirir."""
    local_slots = sorted({slot.astimezone(tz) for slot in slots})
    if not local_slots:
        return []
    ranges: list[tuple[datetime, datetime]] = []
    start = previous = local_slots[0]
    step = timedelta(minutes=step_minutes)
    duration = timedelta(minutes=duration_minutes)
    for current in local_slots[1:]:
        if current - previous != step:
            ranges.append((start, previous + duration))
            start = current
        previous = current
    ranges.append((start, previous + duration))
    return ranges


def _clock_spoken(value: datetime) -> str:
    return str(value.hour) if value.minute == 0 else f"{value.hour}:{value.minute:02d}"


def _format_slot_ranges(ranges: list[tuple[datetime, datetime]]) -> str:
    parts = [
        f"{_clock_spoken(start)} ile {_clock_spoken(end)} arası"
        for start, end in ranges
    ]
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " ve " + parts[-1]


def _repair_time_stt(text: str) -> str:
    """Sistem saat beklerken oluşan dar kapsamlı saat→saç varyantlarını düzeltir."""
    text = re.sub(
        r"^\s*saç\b[\s,.:;-]*", "saat ", text, count=1, flags=re.IGNORECASE
    )
    # 8 kHz telefon sesinde /b/ patlaması kaybolduğunda "beşe" sıkça
    # "deşe/leşe" olarak çözülür. Yalnızca saat beklenen bağlamda çağrılır.
    text = re.sub(
        r"\b(?:deşe|leşe|veşe|peşe)\b", "beşe", text, count=1,
        flags=re.IGNORECASE,
    )
    return re.sub(
        r"\bsaat\s+on(?:\s+)?işin\b",
        "saat on için",
        text,
        count=1,
        flags=re.IGNORECASE,
    )


def _time_from_text(text: str, *, allow_bare: bool = False) -> str | None:
    if allow_bare:
        text = _repair_time_stt(text)
    m = re.search(r"\b([01]?\d|2[0-3])[:.]([0-5]\d)\b", text)
    if m:
        return f"{int(m.group(1)):02d}:{m.group(2)}"
    m = re.search(
        r"(?:saat\s+)([01]?\d|2[0-3])(?![\d:.])(?:\s*(buçuk))?",
        text.lower(),
    )
    if m:
        hour = int(m.group(1))
        if 1 <= hour <= 7:
            hour += 12
        return f"{hour:02d}:{'30' if m.group(2) else '00'}"
    m = re.search(r"\b([01]?\d|2[0-3])['’]?(?:e|a|ye|ya)\b", text.lower())
    if m:
        hour = int(m.group(1))
        if 1 <= hour <= 7:
            hour += 12
        return f"{hour:02d}:00"
    hour_words = {
        "bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5, "altı": 6,
        "yedi": 7, "sekiz": 8, "dokuz": 9, "on": 10, "on bir": 11,
        "on iki": 12, "on üç": 13, "on dört": 14, "on beş": 15,
        "on altı": 16, "on yedi": 17, "on sekiz": 18, "on dokuz": 19,
        "yirmi": 20, "yirmi bir": 21, "yirmi iki": 22, "yirmi üç": 23,
    }
    m = re.search(
        r"\bsaat\s+((?:yirmi|on)(?:\s+(?:bir|iki|üç|dört|beş|altı|yedi|"
        r"sekiz|dokuz))?|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz)"
        r"(?:\s*['’]?(?:ye|ya|e|a|te|ta|de|da))?\b",
        text.lower(),
    )
    if not m and allow_bare:
        # Sistem saat beklerken "bir" veya "bir olsun" cevabı da saattir.
        m = re.fullmatch(
            r"\s*((?:yirmi|on)(?:\s+(?:bir|iki|üç|dört|beş|altı|yedi|"
            r"sekiz|dokuz))?|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz)"
            r"(?:\s+(?:olsun|uygun))?\s*[.!]?\s*",
            text.lower(),
        )
    if m and m.group(1) in hour_words:
        hour = hour_words[m.group(1)]
        if 1 <= hour <= 7:
            hour += 12
        return f"{hour:02d}:00"
    return None


def _invalid_explicit_date(text: str) -> bool:
    """32 Temmuz gibi takvimde bulunmayan açık tarihleri yakala."""
    months = {
        "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4, "mayıs": 5,
        "haziran": 6, "temmuz": 7, "ağustos": 8, "eylül": 9,
        "ekim": 10, "kasım": 11, "aralık": 12,
    }
    month_pattern = "|".join(months)
    match = re.search(
        rf"\b(\d{{1,2}})\s*({month_pattern})(?:\s+(\d{{4}}))?\b",
        text.casefold(),
    )
    if not match:
        return False
    day = int(match.group(1))
    month = months[match.group(2)]
    year = int(match.group(3)) if match.group(3) else date.today().year
    try:
        date(year, month, day)
    except ValueError:
        return True
    return False


def _invalid_explicit_time(text: str) -> bool:
    """Saat 28 ve 12:75 gibi saat aralığı dışındaki ifadeleri yakala."""
    lower = text.casefold()
    numeric = re.search(r"\bsaat\s+(\d{1,2})(?:[:.](\d{1,2}))?\b", lower)
    if not numeric:
        numeric = re.search(r"\b(\d{1,2})[:.](\d{2})\b", lower)
    if numeric:
        hour = int(numeric.group(1))
        minute = int(numeric.group(2) or 0)
        return hour > 23 or minute > 59

    units = {
        "sıfır": 0, "bir": 1, "iki": 2, "üç": 3, "dört": 4,
        "beş": 5, "altı": 6, "yedi": 7, "sekiz": 8, "dokuz": 9,
    }
    tens = {
        "on": 10, "yirmi": 20, "otuz": 30, "kırk": 40, "elli": 50,
        "altmış": 60, "yetmiş": 70, "seksen": 80, "doksan": 90,
    }
    word = re.search(
        r"\bsaat\s+(sıfır|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|"
        r"on|yirmi|otuz|kırk|elli|altmış|yetmiş|seksen|doksan)"
        r"(?:\s+(bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz))?\b",
        lower,
    )
    if not word:
        return False
    first, second = word.group(1), word.group(2)
    hour = (tens.get(first) if first in tens else units[first]) + (
        units.get(second, 0) if first in tens else 0
    )
    return hour > 23


def _has_date(text: str) -> bool:
    if _invalid_explicit_date(text):
        return False
    words = (
        "bugün", "yarın", "öbür gün", "pazartesi", "salı", "çarşamba",
        "perşembe", "cuma", "cumartesi", "pazar", "ocak", "şubat", "mart",
        "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim",
        "kasım", "aralık", "hafta",
    )
    return any(word in text.lower() for word in words)


def _repair_date_stt(text: str, *, booking_context: bool = False) -> str:
    """Telefon STT'sindeki yaygın yarın→yarım son-ses karışmasını bağlamda düzeltir."""
    lower = text.lower()
    has_booking_cue = any(
        cue in lower
        for cue in ("randevu", "alacağım", "almak", "berber", "usta", "beyden")
    )
    if not (booking_context or has_booking_cue):
        return text

    # "Yarım saat sonra" gerçek bir süre ifadesidir. Buna karşılık
    # "yarım saat beşe" dilbilgisel olarak yarın+saat STT karışmasıdır.
    hour_starts = (
        r"bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|\d"
    )
    text = re.sub(
        rf"\byarım\s+saat\s+(?=(?:{hour_starts}))",
        "yarın saat ",
        text,
        count=1,
        flags=re.IGNORECASE,
    )
    if "yarım saat" in text.lower():
        return text

    for variant in (
        "yarım", "yarim", "yerin", "yerim", "yaren", "yard", "yar",
    ):
        text = re.sub(
            rf"\b{variant}\b", "yarın", text, count=1, flags=re.IGNORECASE
        )
    return text


def _yes(text: str) -> bool:
    t = text.lower().strip()
    if any(x in t for x in ("evet", "olur", "tamam", "onaylıyorum", "uygun")):
        return True
    # Telefon STT'sinde "evet" sıklıkla "evert" olarak gelebiliyor.
    return any(fuzz.ratio(word, "evet") >= 78 for word in re.findall(r"\w+", t))


def _no(text: str) -> bool:
    t = text.lower().strip()
    return any(x in t for x in ("hayır", "olmaz", "vazgeç", "değiştir"))


def _no_more_requests(text: str) -> bool:
    """Takip sorusuna verilen kesin olumsuz cevabı ayırt eder.

    Telefon STT'si kısa cevapları bazen ``hayır, yok, yok`` gibi tekrarlı
    döndürebilir. Tekrarları kabul et; ancak ``yok ama ...`` biçiminde yeni bir
    talebe bağlanan cümleyi kapanış sayma.
    """
    # Python'da büyük Türkçe İ casefold sonrası ``i`` + birleşen nokta olur;
    # telefon STT'sinden gelen "İstemiyorum" ifadesini iki kelimeye bölme.
    folded = text.casefold().replace("i\u0307", "i")
    normalized = re.sub(r"[^\wçğıöşü]+", " ", folded).strip()
    if not normalized or re.search(r"\bama\b", normalized):
        return False
    # Teşekkür/veda sözcüğünün yanında açık bir işlem talebi varsa görüşmeyi
    # kapatma; kullanıcı takip sorusuna doğrudan yeni talebiyle cevap verebilir.
    if re.search(
        r"\b(?:randevu|istiyorum|isterim|oluştur|almak|iptal|değiştir|"
        r"ertele|yarın|bugün|saat)\b",
        normalized,
    ):
        return False

    explicit_phrases = (
        "başka bir isteğim yok",
        "başka isteğim yok",
        "başka bir şey yok",
        "başka şey yok",
        "başka yok",
        "başka bir talebim yok",
        "başka talebim yok",
        "gerek yok",
        "hepsi bu",
        "bu kadardı",
        "çok teşekkür",
        "sağ olun",
        "sağolun",
        "konuşmayı sonlandır",
        "konuşmaya sonlandır",
        "kapatabilirsin",
        "bu kadar",
    )
    if any(phrase in normalized for phrase in explicit_phrases):
        return True

    tokens = normalized.split()
    allowed_tokens = {
        "hayır", "hayir", "yok", "yoktur", "yo", "yoh", "istemiyorum",
        "istemem", "teşekkür", "teşekkürler", "ederim", "sağ", "ol",
        "olun", "sağol", "sağolun", "peki", "iyi", "günler", "başka",
        "bir", "şey", "istek", "talep", "gerek", "hepsi", "bu", "kadar",
        "kadardı",
    }
    closing_tokens = {
        "hayır", "hayir", "yok", "yoktur", "yo", "yoh", "istemiyorum",
        "istemem", "teşekkür", "teşekkürler",
    }
    return set(tokens) <= allowed_tokens and any(
        token in closing_tokens for token in tokens
    )


def _yes_more_requests(text: str) -> bool:
    normalized = re.sub(r"[^\wçğıöşü]+", " ", text.casefold()).strip()
    return bool(re.fullmatch(r"(?:evet(?:\s+var)?|var|olur)", normalized))


@dataclass
class Pending:
    action: str
    appointment: dict | None = None


class DialogManager:
    """LLM'in veritabanı yazamadığı, açık onaylı ve tipli görüşme akışı."""

    _http: httpx.AsyncClient | None = None

    def __init__(self, business: dict, caller: str, call_id: str) -> None:
        self.business = business
        self.caller = caller
        self.call_id = call_id
        self._cache = get_voice_session_cache()
        self._cache_session_id = f"voice:{call_id}"
        self.services: list[dict] = []
        self.staff: list[dict] = []
        self.customer: dict | None = None
        self.conversation: dict | None = None
        self.service: dict | None = None
        self.staff_member: dict | None = None
        self.target_date: date | None = None
        self.target_time: str | None = None
        self.pending: Pending | None = None
        self.closed = False
        self.completion_kind: str | None = None
        self.history: list[dict[str, str]] = []
        self._message_buffer: ConversationMessageBuffer | None = None

    def clear_cache(self) -> None:
        self._cache.clear_session(self._cache_session_id)

    async def shutdown(self) -> None:
        if self._message_buffer is not None:
            await self._message_buffer.close(timeout_s=2.0)
        await self._cache.clear_session_wait(self._cache_session_id)

    async def initialize(self) -> None:
        db = get_db()

        async def load_catalog() -> dict[str, list[dict]]:
            services, staff = await asyncio.gather(
                db.services.find({
                    "business_id": self.business["_id"], "is_active": True,
                }).to_list(100),
                db.staff.find({
                    "business_id": self.business["_id"], "is_active": True,
                }).to_list(100),
            )
            return {"services": services, "staff": staff}

        catalog_task = self._cache.get_or_load(
            f"voice-catalog:{self.business['_id']}",
            ("active_staff_services", str(self.business["_id"])),
            load_catalog,
            kind="catalog",
        )
        customer_task = upsert_customer_by_phone(
            self.business["_id"], self.caller, "Telefon Müşterisi"
        )
        catalog, self.customer = await asyncio.gather(
            catalog_task, customer_task
        )
        self.services = list(catalog.get("services") or [])
        self.staff = list(catalog.get("staff") or [])
        self.conversation = await upsert_conversation(
            self.business["_id"], "voice", self.call_id, self.customer["_id"]
        )
        self._message_buffer = ConversationMessageBuffer(
            self.conversation["_id"]
        )

    def _match(
        self, text: str, docs: list[dict], *, fuzzy: bool = True
    ) -> dict | None:
        names = [str(doc.get("name", "")) for doc in docs]
        searchable = re.sub(r"[^\w]+", " ", text.casefold(), flags=re.UNICODE)
        tokens = searchable.split()
        direct = next(
            (
                doc
                for doc in docs
                if re.sub(
                    r"[^\w]+", " ", str(doc.get("name", "")).casefold(),
                    flags=re.UNICODE,
                ).strip() in searchable
            ),
            None,
        )
        if direct:
            return direct
        # "Mehmet", "Emre'den" ve "Yusuf usta" gibi yalnızca ilk adla
        # yapılan seçimleri LLM çağrısı olmadan kesin olarak eşleştir.
        first_name_matches = []
        for doc in docs:
            first_name = str(doc.get("name", "")).casefold().split()[0]
            if first_name in tokens:
                first_name_matches.append(doc)
        if len(first_name_matches) == 1:
            return first_name_matches[0]
        if not fuzzy:
            return None

        # Uzun bir randevu cümlesini hizmet adının tamamıyla karşılaştırmak,
        # telefon STT'sindeki tek ek/harf hatasında skoru gereksiz düşürür.
        # Yalnız hizmet/personel adı uzunluğundaki ardışık kelime pencerelerini
        # değerlendir ve birbirinden açıkça ayrılan tek katalog sonucunu kabul et.
        window_scores: list[tuple[float, int]] = []
        for index, doc in enumerate(docs):
            normalized_name = re.sub(
                r"[^\w]+", " ", str(doc.get("name", "")).casefold(),
                flags=re.UNICODE,
            ).strip()
            word_count = len(normalized_name.split())
            if not normalized_name or not word_count or len(tokens) < word_count:
                continue
            score = max(
                fuzz.ratio(" ".join(tokens[offset:offset + word_count]), normalized_name)
                for offset in range(len(tokens) - word_count + 1)
            )
            window_scores.append((score, index))
        window_scores.sort(reverse=True)
        if window_scores and window_scores[0][0] >= 84:
            runner_up = window_scores[1][0] if len(window_scores) > 1 else 0
            if window_scores[0][0] - runner_up >= 5:
                return docs[window_scores[0][1]]

        result = process.extractOne(text, names, scorer=fuzz.WRatio, score_cutoff=72)
        return docs[result[2]] if result else None

    def is_probable_playback_echo(self, text: str) -> bool:
        """Okunan listeyi geri döndüren hat yankısını kullanıcı seçimi sayma."""
        searchable = re.sub(r"[^\w]+", " ", text.casefold(), flags=re.UNICODE)
        tokens = set(searchable.split())
        staff_hits = sum(
            str(item.get("name", "")).casefold().split()[0] in tokens
            for item in self.staff
        )
        if not self.staff_member and staff_hits >= 2:
            return True
        service_hits = sum(
            re.sub(
                r"[^\w]+",
                " ",
                str(item.get("name", "")).casefold(),
                flags=re.UNICODE,
            ).strip() in searchable
            for item in self._available_services_for_selected_staff()
        )
        return bool(self.staff_member and not self.service and service_hits >= 2)

    def _spoken_staff_names(self) -> str:
        first_names = [str(item.get("name", "")).split()[0] for item in self.staff[:4]]
        if len(first_names) < 2:
            return "".join(first_names)
        return ", ".join(first_names[:-1]) + " ve " + first_names[-1]

    def _available_services_for_selected_staff(self) -> list[dict]:
        """Seçilen personelin verebildiği aktif hizmetleri konuşma sırasıyla döndürür."""
        if not self.staff_member:
            return self.services
        service_ids = set(self.staff_member.get("service_ids") or [])
        return [item for item in self.services if item.get("_id") in service_ids]

    @staticmethod
    def _staff_allows_service(staff: dict, service: dict) -> bool:
        return service.get("_id") in set(staff.get("service_ids") or [])

    @staticmethod
    def _spoken_names(items: list[dict]) -> str:
        names = [str(item.get("name", "")).strip() for item in items if item.get("name")]
        if not names:
            return ""
        if len(names) == 1:
            return names[0]
        return ", ".join(names[:-1]) + " ve " + names[-1]

    def _staff_selection_prompt(self) -> str:
        names = self._spoken_staff_names()
        return (
            f"Berberlerimiz: {names}. Hangisini tercih edersiniz?"
            if names
            else "Hangi berberimizi tercih edersiniz?"
        )

    def opening_prompt(self) -> str:
        """Hazır karşılama bittikten sonra kesilebilir ilk diyalog sorusu."""
        return self._staff_selection_prompt()

    def _service_selection_prompt(self) -> str:
        names = self._spoken_names(self._available_services_for_selected_staff())
        return (
            f"Hizmetlerimiz: {names}. Hangisini istersiniz?"
            if names
            else "Hangi işlemi yaptırmak istersiniz?"
        )

    def stt_context(self) -> tuple[str, str]:
        """Whisper'ı yalnızca bu turda beklenen kelimelere yönlendirir."""
        if self.pending and self.pending.action == "post_booking":
            return (
                "post_booking",
                "Beklenen cevap: başka bir isteğim var, evet, hayır, yok veya yeni randevu talebi.",
            )
        if self.pending and self.pending.action in {
            "create", "cancel", "reschedule_confirm"
        }:
            return "confirmation", "Beklenen kısa cevap: evet, hayır, olur veya değiştir."
        if not self.staff_member:
            names = ", ".join(str(item.get("name", "")) for item in self.staff)
            return "staff", f"Beklenen berber adı: {names}."
        if not self.service:
            allowed = [
                str(item.get("name", ""))
                for item in self.services
                if item["_id"] in (self.staff_member.get("service_ids") or [])
            ]
            return "service", "Beklenen hizmet adı: " + ", ".join(allowed) + "."
        if not self.target_date:
            return (
                "date",
                "Beklenen tarih: bugün, yarın, haftaya, pazartesi, salı, "
                "çarşamba, perşembe, cuma, cumartesi veya pazar.",
            )
        if not self.target_time:
            return (
                "time",
                "Beklenen saat: saat dokuz, saat on, saat on bir, saat on iki, "
                "saat bir, saat iki, saat üç, saat dört, saat beş.",
            )
        return (
            "general",
            "Türkçe berber randevusu; berber, hizmet, tarih ve saat.",
        )

    def normalize_stt_text(self, text: str) -> str:
        """Diyalog aşamasına göre güvenli STT düzeltmelerini cevap öncesi uygular."""
        state, _ = self.stt_context()
        normalized = _repair_date_stt(
            text,
            booking_context=state in {"date", "time", "general"}
            or bool(self.staff_member or self.service),
        )
        # Telefon hattında "saç tıraşı" özellikle "saç trafiği" veya
        # "saç daş" olarak çözülebiliyor. İşletmede Saç Kesimi gerçekten varsa
        # yalnız bu dar ve gözlenmiş varyantları katalogdaki kesin ada çevir.
        hair_service = next(
            (
                str(item.get("name"))
                for item in self.services
                if str(item.get("name", "")).casefold() == "saç kesimi"
            ),
            None,
        )
        if hair_service:
            normalized = re.sub(
                r"\bsaç\s+(?:tıraşı|traşı|tırışı|trafiği|trafigi|daş(?:ı)?)\b",
                hair_service,
                normalized,
                flags=re.IGNORECASE,
            )
        if state == "time":
            normalized = _repair_time_stt(normalized)
        return normalized

    @staticmethod
    def is_close_request(text: str) -> bool:
        """Türkçe büyük İ ve noktalama farklarından bağımsız kesin vedayı yakala."""
        folded = text.casefold().replace("i\u0307", "i")
        normalized = re.sub(r"[^\wçğıöşü]+", " ", folded).strip()
        if any(
            phrase in normalized
            for phrase in (
                "iyi günler", "görüşürüz", "hoşça kal", "telefonu kapat",
                "kapat", "konuşmayı sonlandır", "konuşmaya sonlandır",
                "görüşmeyi sonlandır", "sonlandırabilirsin",
            )
        ):
            return True
        if "kolay gelsin" not in normalized:
            return False
        # "Kolay gelsin, yarın için randevu istiyorum" bir selamlamadır;
        # yalnız yanında gerçek bir talep yoksa görüşme vedası kabul edilir.
        request_words = (
            "randevu", "almak", "istiyorum", "isterim", "müsait", "boş",
            "iptal", "değiştir", "ertele", "usta", "berber", "hizmet",
            "işlem", "yarın", "bugün", "saat",
        )
        return not any(word in normalized for word in request_words)

    def accepts_low_confidence_transcript(self, text: str) -> bool:
        """Yalnız mevcut adımda açıkça tanınan düşük güvenli cevabı kabul eder."""
        if self.is_close_request(text):
            return True
        state, _ = self.stt_context()
        if state == "staff":
            return self._match(text, self.staff, fuzzy=False) is not None
        if state == "service":
            return self._match(
                text,
                self._available_services_for_selected_staff(),
                fuzzy=False,
            ) is not None
        if state == "date":
            return _has_date(_repair_date_stt(text, booking_context=True))
        if state == "time":
            # Hotword/yankı bazen "saat iki, saat on iki" gibi birden fazla
            # aday üretir. Düşük güvende yalnız tek saat adayı kabul edilir.
            if text.casefold().count("saat") > 1:
                return False
            return _time_from_text(text, allow_bare=True) is not None
        if state == "confirmation":
            return _yes(text) or _no(text)
        if state == "post_booking":
            return _no_more_requests(text) or _yes_more_requests(text)
        return False

    def low_confidence_retry_prompt(self) -> str:
        state, _ = self.stt_context()
        prompts = {
            "staff": self._staff_selection_prompt(),
            "service": self._service_selection_prompt(),
            "date": "Hangi gün gelmek istersiniz?",
            "time": "Saat kaçta gelmek istersiniz?",
            "confirmation": "Onaylıyorsanız evet, değiştirmek istiyorsanız hayır deyin.",
            "post_booking": "Başka bir isteğiniz varsa söyleyin, yoksa hayır deyin.",
        }
        return prompts.get(state, "Lütfen isteğinizi tekrar söyler misiniz?")

    def sanitize_low_confidence_transcript(self, text: str) -> str:
        """Düşük güvenli metinden yalnız kesin tanınan mevcut-adım değerini alır."""
        if self.is_close_request(text):
            return "kapat"
        state, _ = self.stt_context()
        if state == "staff":
            matched = self._match(text, self.staff, fuzzy=False)
            return str(matched.get("name")) if matched else ""
        if state == "service":
            matched = self._match(
                text,
                self._available_services_for_selected_staff(),
                fuzzy=False,
            )
            return str(matched.get("name")) if matched else ""
        if state == "date":
            repaired = _repair_date_stt(text, booking_context=True)
            if _has_date(repaired):
                value, _ = parse_target_date_tr(repaired)
                return _date_spoken(value)
            return ""
        if state == "time":
            value = _time_from_text(text, allow_bare=True)
            return f"saat {value}" if value else ""
        if state == "confirmation":
            if _yes(text):
                return "evet"
            if _no(text):
                return "hayır"
        if state == "post_booking":
            if _no_more_requests(text):
                return "yok"
            if _yes_more_requests(text):
                return "evet"
        return ""

    async def _record(self, role: str, text: str) -> None:
        self.history.append({"role": role, "content": text})
        # Kalıcı iş durumu staff/service/date/time alanlarında tutulur. Serbest
        # metin geçmişini kısa tutmak uzun görüşmede eski ve düzeltilmiş
        # bilgilerin yeniden LLM bağlamına sızmasını engeller.
        self.history = self.history[-6:]
        if self._message_buffer is not None:
            self._message_buffer.enqueue({
                "role": role,
                "content": text,
                "timestamp": datetime.now(timezone.utc),
            })

    async def _appointments(self) -> list[dict]:
        if not self.customer:
            return []
        return await get_db().appointments.find({
            "business_id": self.business["_id"],
            "customer_id": self.customer["_id"],
            "status": {"$in": ["pending", "confirmed"]},
            "start_time": {"$gt": datetime.now(timezone.utc)},
        }).sort("start_time", 1).to_list(10)

    def _describe_appointment(self, apt: dict) -> str:
        tz = ZoneInfo(self.business.get("timezone", "Europe/Istanbul"))
        local = apt["start_time"].astimezone(tz)
        service = (apt.get("services") or [{}])[0].get("name", "işlem")
        staff = next((s.get("name") for s in self.staff if s["_id"] == apt["staff_id"]), "personel")
        return f"{_date_spoken(local.date())} saat {local:%H:%M}, {staff}, {service}"

    def _llm_state(self) -> str:
        return json.dumps(
            {
                "business": self.business.get("name", "Randevum Online"),
                "staff": [item.get("name") for item in self.staff],
                "services": [item.get("name") for item in self.services],
                "selected": {
                    "staff": self.staff_member.get("name") if self.staff_member else None,
                    "service": self.service.get("name") if self.service else None,
                    "date": self.target_date.isoformat() if self.target_date else None,
                    "time": self.target_time,
                },
                "pending_action": self.pending.action if self.pending else None,
                "today": date.today().isoformat(),
            },
            ensure_ascii=False,
        )

    def _llm_recent_history(self) -> list[dict[str, str]]:
        """Yalnızca son asistan mesajı ve güncel kullanıcı sözünü döndürür."""
        return self.history[-2:]

    async def _interpret(self, text: str) -> dict[str, Any]:
        cfg = get_voice_settings()
        if not cfg.deepseek_api_key:
            return {}
        if self.__class__._http is None:
            self.__class__._http = httpx.AsyncClient(
                timeout=min(cfg.ai_request_timeout_s, 8.0),
                limits=httpx.Limits(max_connections=6, max_keepalive_connections=3),
            )
        prompt = {
            "role": "system",
            "content": (
                "Sen Randevum Online'ın Türkçe telefon asistanısın. Kullanıcının "
                "son cümlesini verilen işletme durumuyla yorumla. GÜNCEL DURUM "
                "tek güvenilir hafızadır; kısa konuşma geçmişindeki eski veya "
                "çelişkili değerleri yok say. Yalnızca son kullanıcı cümlesi dolu "
                "bir alanı değiştirebilir. "
                "Yalnızca geçerli JSON döndür. Alanlar: "
                "intent(create,list,cancel,reschedule,availability,close,other), "
                "service, staff, date, time, answer. date YYYY-MM-DD, time HH:MM "
                "olmalı; bilinmeyen alan null. answer kısa, doğal, en fazla iki "
                "cümlelik, sıcak ve gündelik Türkçe cevaptır. Kullanıcı bir bilgiyi "
                "düzeltiyorsa yeni değeri esas al; 'söyledim ya' gibi bir tepki "
                "veriyorsa kısa bir özür veya anlayış göster. Daha önce verilen "
                "bilgiyi tekrar sorma ve menü gibi işlem seçenekleri sayma. "
                "Personel, hizmet, fiyat veya işletme "
                "sorusunu yalnızca verilen durumdan cevapla; bilgi yoksa uydurma. "
                "Randevu oluşturma/iptal/değiştirme işlemini kendin yapma."
            ),
        }
        messages: list[dict[str, str]] = [
            prompt,
            {"role": "system", "content": "GÜNCEL DURUM: " + self._llm_state()},
            *self._llm_recent_history(),
        ]
        if not messages or messages[-1].get("content") != text:
            messages.append({"role": "user", "content": text})
        try:
            response = await self._http.post(
                f"{cfg.deepseek_base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {cfg.deepseek_api_key}"},
                json={
                    "model": cfg.deepseek_model,
                    "messages": messages,
                    "temperature": 0.2,
                    "max_tokens": 220,
                    "response_format": {"type": "json_object"},
                },
            )
            response.raise_for_status()
            data = response.json()["choices"][0]["message"]["content"]
            return json.loads(data)
        except Exception as exc:
            log.warning("DeepSeek yorumlama başarısız type=%s", type(exc).__name__)
            return {}

    def _apply_entities(self, text: str, interpreted: dict[str, Any]) -> None:
        # LLM yalnız niyet sınıflandırır. Kullanıcının gerçek transkriptinde açık
        # kanıtı olmayan hiçbir usta, hizmet, tarih veya saat oturuma yazılamaz.
        matched_service = self._match(text, self.services)
        matched_staff = self._match(text, self.staff)
        if matched_staff:
            self.staff_member = matched_staff
        if matched_service:
            if not self.staff_member or self._staff_allows_service(
                self.staff_member, matched_service
            ):
                self.service = matched_service
            else:
                self.service = None
        # Önce hizmet, sonra personel söylenmiş olabilir. Yeni personel mevcut
        # hizmeti vermiyorsa yanlış kombinasyonla onaya ilerleme.
        if (
            self.staff_member
            and self.service
            and not self._staff_allows_service(self.staff_member, self.service)
        ):
            self.service = None

        date_text = _repair_date_stt(
            text,
            booking_context=bool(
                matched_staff
                or matched_service
                or self.staff_member
                or self.service
            ),
        )
        if _has_date(date_text):
            self.target_date, _ = parse_target_date_tr(date_text)

        expects_time = bool(
            self.staff_member
            and self.service
            and self.target_date
            and not self.target_time
        )
        parsed_time = _time_from_text(text, allow_bare=expects_time)
        if parsed_time and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", str(parsed_time)):
            self.target_time = str(parsed_time)

    def _complete_booking_is_explicit_in_text(self, text: str) -> bool:
        """Dört rezervasyon alanının da aynı müşteri cümlesinde bulunduğunu doğrula."""
        staff = self._match(text, self.staff)
        service = self._match(text, self.services)
        if not staff or not service or not self._staff_allows_service(staff, service):
            return False
        date_text = _repair_date_stt(text, booking_context=True)
        if not _has_date(date_text):
            return False
        # Tek cümlede otomatik kayıt için çıplak sayı kabul edilmez; saat ifadesi
        # transkriptte açıkça bulunmalıdır.
        parsed_time = _time_from_text(text, allow_bare=False)
        return bool(
            parsed_time
            and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", parsed_time)
        )

    def _is_explicit_new_request(self, text: str) -> bool:
        """Takip sorusundan sonra yalnız kesin yeni talepte rezervasyon durumunu aç."""
        if self._local_intent(text) is not None:
            return True
        repaired = _repair_date_stt(text, booking_context=True)
        return bool(
            self._match(text, self.staff, fuzzy=False)
            or self._match(text, self.services, fuzzy=False)
            or _has_date(repaired)
            or _time_from_text(text, allow_bare=False)
        )

    def _apply_confirmation_correction(self, text: str) -> bool:
        """Onay reddiyle aynı cümlede verilen yeni alanı kaybetmeden uygular."""
        before = (
            self.staff_member,
            self.service,
            self.target_date,
            self.target_time,
        )
        matched_staff = self._match(text, self.staff)
        matched_service = self._match(text, self.services)
        if matched_staff:
            self.staff_member = matched_staff
        if matched_service:
            if not self.staff_member or self._staff_allows_service(
                self.staff_member, matched_service
            ):
                self.service = matched_service
            else:
                self.service = None
        if (
            self.staff_member
            and self.service
            and not self._staff_allows_service(self.staff_member, self.service)
        ):
            self.service = None

        parsed_time = _time_from_text(text, allow_bare=True)
        if parsed_time:
            self.target_time = parsed_time

        lower = text.lower()
        # "Bu hafta değil" yalnızca ret bilgisidir; yeni tarih değildir.
        negative_date_only = any(
            phrase in lower
            for phrase in ("bu hafta değil", "o gün değil", "bugün değil", "yarın değil")
        )
        if _has_date(text) and not negative_date_only:
            self.target_date, _ = parse_target_date_tr(text)

        after = (
            self.staff_member,
            self.service,
            self.target_date,
            self.target_time,
        )
        return after != before

    def _confirmation_answer(self, action: str) -> str:
        assert self.target_date and self.target_time
        assert self.staff_member and self.service
        return (
            f"{_date_spoken(self.target_date)} saat "
            f"{self.target_time}, {self.staff_member['name']}, "
            f"{self.service['name']} için "
            f"{'değişikliği' if action == 'reschedule_confirm' else 'randevuyu'} "
            "onaylıyor musunuz?"
        )

    async def _requested_slot_status(self) -> str:
        """Seçili personelin istenen saatte uygunluk durumunu döndürür."""
        assert self.target_date and self.target_time
        assert self.staff_member and self.service
        try:
            slots = await self._available_slots()
        except Exception as exc:
            log.warning("Onay öncesi müsaitlik kontrolü başarısız type=%s", type(exc).__name__)
            return "error"

        tz = ZoneInfo(self.business.get("timezone", "Europe/Istanbul"))
        requested = self.target_time
        if any(slot.astimezone(tz).strftime("%H:%M") == requested for slot in slots):
            return "available"
        return "time_full" if slots else "date_full"

    def _effective_working_windows(self) -> list[tuple[time, time]]:
        """Tam gün müsait ifadesi için işletme/personel ortak çalışma pencereleri."""
        assert self.target_date and self.staff_member
        # Özel gün saatleri normal programdan farklı olabilir; bu durumda yanlış
        # "tamamen müsait" dememek için aralık cevabını tercih ederiz.
        if is_special_closure(self.business, self.target_date):
            return []
        day_name = WEEKDAY_NAMES[self.target_date.weekday()]
        business_hours = self.business.get("working_hours") or []
        staff_hours = self.staff_member.get("working_hours") or business_hours
        business_windows = windows_for_day(business_hours, day_name)
        staff_windows = windows_for_day(staff_hours, day_name)
        return [
            (max(b_start, s_start), min(b_end, s_end))
            for b_start, b_end in business_windows
            for s_start, s_end in staff_windows
            if max(b_start, s_start) < min(b_end, s_end)
        ]

    async def _availability_answer(self) -> str:
        """Tek tek saat okumadan, birleşik boş zaman aralıklarını söyler."""
        assert self.target_date and self.staff_member and self.service
        slots = await self._available_slots()
        if not slots:
            return "Bu gün uygun saat bulunmuyor. Başka bir gün seçmek ister misiniz?"

        tz = ZoneInfo(self.business.get("timezone", "Europe/Istanbul"))
        ranges = _slot_ranges(
            slots, tz, int(self.service["duration_minutes"]), step_minutes=15
        )
        working_windows = self._effective_working_windows()
        fully_available = bool(working_windows) and len(ranges) == len(working_windows)
        if fully_available:
            fully_available = all(
                start.time().replace(tzinfo=None) == window_start
                and end.time().replace(tzinfo=None) == window_end
                for (start, end), (window_start, window_end)
                in zip(ranges, working_windows)
            )
        if fully_available:
            return (
                f"{_date_spoken(self.target_date)} günü tamamen müsait. "
                "Saat kaçta gelmek istersiniz?"
            )
        return (
            f"{_date_spoken(self.target_date)} günü saat "
            f"{_format_slot_ranges(ranges)} müsait. Hangi saati istersiniz?"
        )

    async def _available_slots(self) -> list[datetime]:
        """Seçili günün slotlarını çağrı oturumu boyunca kısa süreli saklar."""
        assert self.target_date and self.staff_member and self.service
        key = (
            "available_slots",
            str(self.business["_id"]),
            str(self.service["_id"]),
            str(self.staff_member["_id"]),
            self.target_date.isoformat(),
            15,
        )

        async def load() -> list[datetime]:
            return await compute_available_slots(
                get_db(),
                self.business,
                self.service,
                self.staff_member,
                self.target_date,
                step_minutes=15,
            )

        return await self._cache.get_or_load(
            self._cache_session_id, key, load, kind="availability"
        )

    async def _prepare_confirmation(
        self, action: str, appointment: dict | None = None
    ) -> str:
        """Müsaitlik doğrulanmadan kullanıcıdan kayıt onayı istemez."""
        assert self.target_date and self.target_time
        assert self.staff_member and self.service
        status = await self._requested_slot_status()
        selected_date = self.target_date
        selected_time = self.target_time
        staff_name = str(self.staff_member.get("name", "personel"))

        if status == "time_full":
            self.target_time = None
            self.pending = (
                Pending("reschedule_collect", appointment)
                if action == "reschedule_confirm"
                else None
            )
            return (
                f"{_date_spoken(selected_date)} saat {selected_time}, "
                f"{staff_name} için dolu. Başka bir saat ister misiniz?"
            )
        if status == "date_full":
            self.target_date = None
            self.target_time = None
            self.pending = (
                Pending("reschedule_collect", appointment)
                if action == "reschedule_confirm"
                else None
            )
            return (
                f"{_date_spoken(selected_date)} günü {staff_name} için uygun saat "
                "kalmamış. Başka bir tarih ister misiniz?"
            )
        if status == "error":
            self.pending = (
                Pending("reschedule_collect", appointment)
                if action == "reschedule_confirm"
                else None
            )
            return (
                "Müsaitliği şu anda doğrulayamıyorum. Başka bir saat söylemek "
                "veya biraz sonra tekrar denemek ister misiniz?"
            )

        self.pending = Pending(action, appointment)
        return self._confirmation_answer(action)

    def _fast_information_answer(self, text: str) -> str | None:
        lower = text.lower()
        if any(
            word in lower
            for word in ("randevu al", "iptal", "değiştir", "ertele", "müsait")
        ):
            return None
        if (
            any(word in lower for word in ("berber", "usta", "personel"))
            and any(word in lower for word in ("kaç", "kim", "hangi", "isim"))
        ):
            names = ", ".join(str(item.get("name")) for item in self.staff)
            return f"{len(self.staff)} berberimiz var: {names}."
        if (
            any(word in lower for word in ("hizmet", "işlem"))
            and any(word in lower for word in ("neler", "hangi", "say", "öğren"))
        ):
            services = ", ".join(str(item.get("name")) for item in self.services)
            return f"Hizmetlerimiz: {services}."
        return None

    def _local_intent(self, text: str) -> str | None:
        lower = text.lower()
        date_text = _repair_date_stt(
            text, booking_context=bool(self.staff_member or self.service)
        )
        if any(
            x in lower
            for x in (
                "randevularım", "randevum var", "listele", "randevu bilg",
                "randevunun bilg", "randevumu söyle", "randevumu oku",
                "randevumu öğren", "oluşturduğum randevu", "aldığım randevu",
            )
        ):
            return "list"
        if "iptal" in lower:
            return "cancel"
        if any(x in lower for x in ("değiştir", "ertele", "revize")):
            return "reschedule"
        if any(x in lower for x in ("müsait", "boş saat")):
            return "availability"
        if "randevu" in lower:
            return "create"
        if (
            self._match(text, self.staff)
            or self._match(text, self.services)
            or _has_date(date_text)
            or _time_from_text(text)
        ):
            return (
                "reschedule"
                if self.pending and self.pending.action == "reschedule_collect"
                else "create"
            )
        return None

    async def respond(self, text: str) -> str:
        # AudioSocket bu düzeltmeyi STT sonrasında uygular; diğer çağrı yolları
        # ve doğrudan testler de aynı tek-cümle davranışını kullansın.
        text = self.normalize_stt_text(text)
        await self._record("user", text)
        lower = text.casefold().replace("i\u0307", "i")
        if self.is_close_request(text):
            self.closed = True
            answer = "Bizi aradığınız için teşekkür ederiz. İyi günler."
            await self._record("assistant", answer)
            return answer

        if _invalid_explicit_date(text):
            if self.pending and self.pending.action in {
                "create", "reschedule_collect", "reschedule_confirm",
            }:
                self.pending = None
            self.target_date = None
            self.target_time = None
            answer = (
                "Bu tarih takvimde bulunmuyor. Lütfen geçerli bir tarih "
                "söyler misiniz?"
            )
            await self._record("assistant", answer)
            return answer

        if _invalid_explicit_time(text):
            if self.pending and self.pending.action in {
                "create", "reschedule_collect", "reschedule_confirm",
            }:
                self.pending = None
            self.target_time = None
            answer = (
                "Bu saat geçerli değil. Lütfen sıfır ile yirmi üç arasında "
                "geçerli bir saat söyler misiniz?"
            )
            await self._record("assistant", answer)
            return answer

        if self.pending and self.pending.action == "post_booking":
            if _no_more_requests(text):
                self.pending = None
                self.closed = True
                answer = "Peki, bizi aradığınız için teşekkür ederiz. İyi günler."
                await self._record("assistant", answer)
                return answer
            if _yes_more_requests(text):
                self.pending = None
                self.staff_member = None
                self.service = None
                self.target_date = None
                self.target_time = None
                self.completion_kind = None
                answer = "Tabii, başka nasıl yardımcı olabilirim?"
                await self._record("assistant", answer)
                return answer
            # Önceki onay cümlesinin yankısı veya FIFO'da kalan ikinci parçası
            # yeni bir talep değildir. Durumu bozma ve LLM'e yorumlatma.
            if "onay" in lower or _yes(text):
                self.pending = Pending("post_booking")
                answer = "Randevunuz hazır. Başka bir isteğiniz var mı?"
                await self._record("assistant", answer)
                return answer
            if not self._is_explicit_new_request(text):
                # Belirsiz STT sonucu yeni randevu sayılıp berber listesine
                # düşmemeli; takip durumu korunur.
                answer = "Randevunuz hazır. Başka bir isteğiniz var mı?"
                await self._record("assistant", answer)
                return answer
            # Kullanıcı "evet" demeden doğrudan yeni isteğini söylemiş olabilir.
            self.pending = None
            self.staff_member = None
            self.service = None
            self.target_date = None
            self.target_time = None
            self.completion_kind = None

        if self.pending and self.pending.action == "create":
            if _yes(text):
                answer = await self._commit_create()
                await self._record("assistant", answer)
                return answer
            if _no(text):
                self.pending = None
                corrected = self._apply_confirmation_correction(text)
                if corrected and all((
                    self.staff_member,
                    self.service,
                    self.target_date,
                    self.target_time,
                )):
                    answer = await self._prepare_confirmation("create")
                else:
                    answer = "Elbette. Hangi bilgiyi değiştirmek istersiniz?"
                await self._record("assistant", answer)
                return answer
            # Kullanıcı onay sırasında bir alanı tekrar söylüyor veya düzeltiyor
            # olabilir. Katı biçimde "evet/hayır" dayatmak yerine onu uygula ve
            # güncel özeti yeniden sor.
            mentioned_entity = bool(
                self._match(text, self.staff)
                or self._match(text, self.services)
                or _has_date(_repair_date_stt(text, booking_context=True))
                or _time_from_text(text, allow_bare=True)
            )
            if mentioned_entity:
                self.pending = None
                self._apply_confirmation_correction(text)
                answer = await self._prepare_confirmation("create")
                if any(x in lower for x in ("söyledim", "dedim", "diyorum")):
                    answer = "Haklısınız, söylediğiniz bilgiyi aldım. " + answer
                await self._record("assistant", answer)
                return answer
            if any(x in lower for x in ("tekrar oku", "bilgileri söyle", "bilgiyi söyle")):
                answer = "Tabii. " + self._confirmation_answer("create")
                await self._record("assistant", answer)
                return answer
            answer = "Onay için lütfen evet veya hayır deyin."
            await self._record("assistant", answer)
            return answer
        if self.pending and self.pending.action == "cancel":
            if _yes(text):
                ok = await cancel_appointment(
                    get_db(), str(self.pending.appointment["_id"]), "voice_customer"
                )
                if ok:
                    self.clear_cache()
                    self.pending = Pending("post_booking")
                else:
                    self.pending = None
                answer = (
                    "Randevunuz iptal edildi. Başka bir isteğiniz var mı?"
                    if ok
                    else "Randevu iptal edilemedi."
                )
            elif _no(text):
                self.pending = None
                answer = "İptal işlemini durdurdum. Başka bir isteğiniz var mı?"
            else:
                answer = "İptal işlemi için lütfen evet veya hayır deyin."
            await self._record("assistant", answer)
            return answer
        if self.pending and self.pending.action == "reschedule_confirm":
            if _yes(text):
                assert self.target_date and self.target_time
                result = await reschedule_appointment(
                    get_db(),
                    str(self.pending.appointment["_id"]),
                    f"{self.target_date.isoformat()} {self.target_time}",
                    self.business,
                    self.service,
                    self.staff_member,
                )
                if not result.get("error"):
                    self.clear_cache()
                    self.pending = Pending("post_booking")
                else:
                    self.pending = None
                answer = (
                    "Randevunuz değiştirildi. Başka bir isteğiniz var mı?"
                    if not result.get("error")
                    else "Randevu değiştirilemedi. Başka bir saat seçer misiniz?"
                )
                await self._record("assistant", answer)
                return answer
            if _no(text):
                self.pending = None
                self.target_date = None
                self.target_time = None
                answer = "Değişikliği durdurdum."
                await self._record("assistant", answer)
                return answer
        fast_answer = self._fast_information_answer(text)
        if fast_answer:
            await self._record("assistant", fast_answer)
            return fast_answer

        local_intent = self._local_intent(text)
        # Eksik alan adımlarında o alana veya başka bir randevu bilgisine ait
        # hiçbir veri yoksa serbest LLM cevabı üretme. Böylece "merhaba" gibi
        # FIFO/yankı parçaları işletme ve kişi adı uyduramaz.
        matched_staff = self._match(text, self.staff)
        matched_service = self._match(text, self.services)
        has_date = _has_date(_repair_date_stt(text, booking_context=True))
        has_time = _time_from_text(text, allow_bare=True) is not None
        if not local_intent:
            if not self.staff_member and not any((matched_staff, matched_service, has_date, has_time)):
                answer = self._staff_selection_prompt()
                await self._record("assistant", answer)
                return answer
            if self.staff_member and not self.service and not any((matched_service, has_date, has_time)):
                answer = self._service_selection_prompt()
                await self._record("assistant", answer)
                return answer
            if self.staff_member and self.service and not self.target_date and not any((has_date, has_time)):
                answer = "Hangi gün gelmek istersiniz?"
                await self._record("assistant", answer)
                return answer
        # Rezervasyon işlemleri deterministiktir: usta, hizmet, tarih ve saat
        # yalnız gerçek STT metninden çıkarılır. Bu turlarda LLM çağrısı hem
        # gecikme hem de söylenmeyen alan üretme riski oluşturur.
        if local_intent:
            interpreted: dict[str, Any] = {"intent": local_intent}
        else:
            interpreted = await self._interpret(text)
        intent = str(interpreted.get("intent") or "").lower()
        if intent not in {
            "create", "list", "cancel", "reschedule", "availability", "close", "other"
        }:
            if any(x in lower for x in ("randevularım", "randevum var", "listele")):
                intent = "list"
            elif "iptal" in lower:
                intent = "cancel"
            elif any(x in lower for x in ("değiştir", "ertele", "revize")):
                intent = "reschedule"
            elif any(x in lower for x in ("müsait", "boş saat")):
                intent = "availability"
            elif "randevu" in lower:
                intent = "create"
            else:
                intent = "other"

        if intent == "close":
            self.closed = True
            answer = "Bizi aradığınız için teşekkür ederiz. İyi günler."
            await self._record("assistant", answer)
            return answer

        if intent == "other":
            # LLM serbest sohbet metni üretemez; yalnız niyet ve alan çıkarır.
            # Böylece işletme/kişi adı veya kullanıcının söylemediği ayrıntılar
            # telefonda kendiliğinden uydurulmaz.
            answer = (
                "Sorunuzu anlayamadım. Randevu oluşturma, uygunluk, iptal veya "
                "değişiklik konusunda yardımcı olabilirim."
            )
            await self._record("assistant", answer)
            return answer

        if intent in {"list", "cancel", "reschedule"}:
            appointments = await self._appointments()
            if not appointments:
                answer = "Aktif bir randevunuz bulunmuyor."
                await self._record("assistant", answer)
                return answer
            if intent == "list":
                answer = "Aktif randevunuz: " + self._describe_appointment(appointments[0]) + "."
                await self._record("assistant", answer)
                return answer
            apt = appointments[0]
            if intent == "cancel":
                self.pending = Pending("cancel", apt)
                answer = self._describe_appointment(apt) + " randevunuzu iptal etmemi onaylıyor musunuz?"
                await self._record("assistant", answer)
                return answer
            self.pending = Pending("reschedule_collect", apt)
            self.service = next(
                (s for s in self.services if s["_id"] == apt["services"][0]["service_id"]),
                None,
            )
            self.staff_member = next(
                (s for s in self.staff if s["_id"] == apt["staff_id"]), None
            )

        complete_single_utterance = (
            intent == "create"
            and not (
                self.pending and self.pending.action == "reschedule_collect"
            )
            and self._complete_booking_is_explicit_in_text(text)
        )
        self._apply_entities(text, interpreted)

        if not self.staff_member:
            answer = self._staff_selection_prompt()
        elif not self.service:
            answer = self._service_selection_prompt()
        elif not self.target_date:
            answer = "Hangi gün gelmek istersiniz?"
        elif not self.target_time:
            answer = await self._availability_answer()
        else:
            action = (
                "reschedule_confirm"
                if self.pending and self.pending.action == "reschedule_collect"
                else "create"
            )
            appointment = self.pending.appointment if self.pending else None
            answer = await self._prepare_confirmation(action, appointment)
            if (
                complete_single_utterance
                and self.pending
                and self.pending.action == "create"
            ):
                # _prepare_confirmation canlı müsaitliği doğruladı. Son kayıt
                # yine create_appointment içindeki atomik çakışma kontrolünden geçer.
                answer = await self._commit_create()
        await self._record("assistant", answer)
        return answer

    async def _commit_create(self) -> str:
        assert all((
            self.customer, self.conversation, self.service, self.staff_member,
            self.target_date, self.target_time,
        ))
        result = await create_appointment(
            db=get_db(),
            business=self.business,
            customer=self.customer,
            conversation=self.conversation,
            service=self.service,
            staff=self.staff_member,
            start_local=f"{self.target_date.isoformat()} {self.target_time}",
            source="voice",
            created_by="voice_assistant",
        )
        self.pending = None
        if result.get("error") == "slot_taken":
            self.clear_cache()
            self.target_time = None
            return "Bu saat az önce doldu. Başka bir saat seçer misiniz?"
        if result.get("error"):
            return "Randevu kaydedilemedi. Lütfen tekrar deneyin."
        self.clear_cache()
        summary = (
            f"{_date_spoken(self.target_date)} saat {self.target_time}, "
            f"{self.staff_member['name']} ile {self.service['name']}"
        )
        self.service = self.staff_member = self.target_date = self.target_time = None
        self.pending = Pending("post_booking")
        self.closed = False
        self.completion_kind = None
        log.info("Randevu başarıyla oluşturuldu call_id=%s summary=%s", self.call_id, summary)
        return "Randevunuz oluşturuldu. Başka bir isteğiniz var mı?"
