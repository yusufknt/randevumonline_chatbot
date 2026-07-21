from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

import httpx
from rapidfuzz import fuzz, process

from app.core.booking import cancel_appointment, create_appointment, reschedule_appointment
from app.core.db import (
    append_conversation_message,
    get_db,
    upsert_conversation,
    upsert_customer_by_phone,
)
from app.voice.config import get_voice_settings
from app.voice.llm import parse_target_date_tr

log = logging.getLogger(__name__)

MONTHS_TR = (
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
)


def _date_spoken(value: date) -> str:
    return f"{value.day} {MONTHS_TR[value.month]}"


def _repair_time_stt(text: str) -> str:
    """Sistem saat beklerken oluşan dar kapsamlı saat→saç varyantlarını düzeltir."""
    text = re.sub(
        r"^\s*saç\b[\s,.:;-]*", "saat ", text, count=1, flags=re.IGNORECASE
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
    m = re.search(r"(?:saat\s+)([01]?\d|2[0-3])(?:\s*(buçuk))?", text.lower())
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


def _has_date(text: str) -> bool:
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

    for variant in ("yarım", "yarim", "yerin", "yerim", "yaren"):
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
        self.history: list[dict[str, str]] = []

    async def initialize(self) -> None:
        db = get_db()
        self.services = await db.services.find(
            {"business_id": self.business["_id"], "is_active": True}
        ).to_list(100)
        self.staff = await db.staff.find(
            {"business_id": self.business["_id"], "is_active": True}
        ).to_list(100)
        self.customer = await upsert_customer_by_phone(
            self.business["_id"], self.caller, "Telefon Müşterisi"
        )
        self.conversation = await upsert_conversation(
            self.business["_id"], "voice", self.call_id, self.customer["_id"]
        )

    def _match(self, text: str, docs: list[dict]) -> dict | None:
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
        result = process.extractOne(text, names, scorer=fuzz.WRatio, score_cutoff=72)
        return docs[result[2]] if result else None

    def _spoken_staff_names(self) -> str:
        first_names = [str(item.get("name", "")).split()[0] for item in self.staff[:4]]
        if len(first_names) < 2:
            return "".join(first_names)
        return ", ".join(first_names[:-1]) + " ve " + first_names[-1]

    def stt_context(self) -> tuple[str, str]:
        """Whisper'ı yalnızca bu turda beklenen kelimelere yönlendirir."""
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
        if state == "time":
            normalized = _repair_time_stt(normalized)
        return normalized

    async def _record(self, role: str, text: str) -> None:
        self.history.append({"role": role, "content": text})
        self.history = self.history[-10:]
        if self.conversation:
            await append_conversation_message(self.conversation["_id"], {
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
                "son cümlesini konuşma geçmişi ve verilen işletme durumuyla yorumla. "
                "Yalnızca geçerli JSON döndür. Alanlar: "
                "intent(create,list,cancel,reschedule,availability,close,other), "
                "service, staff, date, time, answer. date YYYY-MM-DD, time HH:MM "
                "olmalı; bilinmeyen alan null. answer kısa, doğal, en fazla iki "
                "cümlelik Türkçe cevaptır. Personel, hizmet, fiyat veya işletme "
                "sorusunu yalnızca verilen durumdan cevapla; bilgi yoksa uydurma. "
                "Randevu oluşturma/iptal/değiştirme işlemini kendin yapma."
            ),
        }
        messages: list[dict[str, str]] = [
            prompt,
            {"role": "system", "content": "GÜNCEL DURUM: " + self._llm_state()},
            *self.history[-6:],
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
                    "temperature": 0,
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
        service_text = interpreted.get("service") or text
        staff_text = interpreted.get("staff") or text
        matched_service = self._match(str(service_text), self.services)
        matched_staff = self._match(str(staff_text), self.staff)
        if matched_service:
            self.service = matched_service
        if matched_staff:
            self.staff_member = matched_staff

        date_text = _repair_date_stt(
            text,
            booking_context=bool(
                matched_staff
                or matched_service
                or self.staff_member
                or self.service
            ),
        )
        parsed_date = interpreted.get("date")
        if parsed_date:
            try:
                candidate = date.fromisoformat(str(parsed_date))
                if candidate >= date.today():
                    self.target_date = candidate
            except ValueError:
                pass
        elif _has_date(date_text):
            self.target_date, _ = parse_target_date_tr(date_text)

        expects_time = bool(
            self.staff_member
            and self.service
            and self.target_date
            and not self.target_time
        )
        parsed_time = interpreted.get("time") or _time_from_text(
            text, allow_bare=expects_time
        )
        if parsed_time and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", str(parsed_time)):
            self.target_time = str(parsed_time)

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
            self.service = matched_service

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
        if any(x in lower for x in ("randevularım", "randevum var", "listele")):
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
        await self._record("user", text)
        lower = text.lower()
        if any(x in lower for x in ("görüşürüz", "iyi günler", "kapat", "hoşça kal")):
            self.closed = True
            answer = "Bizi aradığınız için teşekkür ederiz. İyi günler."
            await self._record("assistant", answer)
            return answer

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
                    self.pending = Pending("create")
                    answer = self._confirmation_answer("create")
                else:
                    answer = "Elbette. Hangi bilgiyi değiştirmek istersiniz?"
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
                self.pending = None
                answer = "Randevunuz iptal edildi." if ok else "Randevu iptal edilemedi."
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
                self.pending = None
                answer = (
                    "Randevunuz değiştirildi."
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
        interpreted = (
            {"intent": local_intent}
            if local_intent
            else await self._interpret(text)
        )
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
            answer = interpreted.get("answer") or "Bizi aradığınız için teşekkür ederiz. İyi günler."
            await self._record("assistant", answer)
            return str(answer)

        if intent == "other":
            answer = interpreted.get("answer")
            if not answer:
                answer = (
                    "Sorunuzu anlayamadım. Randevu oluşturma, uygunluk, iptal veya "
                    "değişiklik konusunda yardımcı olabilirim."
                )
            await self._record("assistant", str(answer))
            return str(answer)

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

        self._apply_entities(text, interpreted)

        if not self.staff_member:
            names = self._spoken_staff_names()
            answer = (
                f"Uygun berberlerimiz: {names}. "
                "Hangi berberi tercih edersiniz?"
            )
        elif not self.service:
            allowed = [
                s["name"] for s in self.services
                if s["_id"] in (self.staff_member.get("service_ids") or [])
            ]
            answer = "Hangi hizmeti istersiniz? " + ", ".join(allowed[:6]) + "."
        elif not self.target_date:
            answer = "Hangi gün gelmek istersiniz?"
        elif not self.target_time:
            from app.voice.tools import VoiceToolExecutor
            slots = await VoiceToolExecutor.check_availability(
                self.business["business_id"], self.service["name"],
                self.target_date.isoformat(), self.staff_member["name"],
            )
            times = slots.get("available_slots", [])
            answer = (
                "Uygun saatler " + ", ".join(times[:5]) + ". Hangisini istersiniz?"
                if times else "Bu gün uygun saat bulunmuyor. Başka bir gün seçer misiniz?"
            )
        else:
            action = (
                "reschedule_confirm"
                if self.pending and self.pending.action == "reschedule_collect"
                else "create"
            )
            appointment = self.pending.appointment if self.pending else None
            self.pending = Pending(action, appointment)
            answer = self._confirmation_answer(action)
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
            self.target_time = None
            return "Bu saat az önce doldu. Başka bir saat seçer misiniz?"
        if result.get("error"):
            return "Randevu kaydedilemedi. Lütfen tekrar deneyin."
        self.service = self.staff_member = self.target_date = self.target_time = None
        return "Randevunuz oluşturuldu. Başka bir isteğiniz var mı?"
