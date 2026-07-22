"""
FAZ 3 - Sesli Asistan (Voice Agent) LLM ve Diyalog Yöneticisi.

Bu modül, STT'den gelen metni alıp randevu iş kurallarına göre uygun yanıtı
üretmek üzere DeepSeek entegrasyonu sağlar.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
import typing
from datetime import date, datetime
from typing import Any


import httpx

from app.core.config import get_settings
from app.voice.config import get_voice_settings
from app.voice.tools import VoiceToolExecutor

logger = logging.getLogger(__name__)

VOICE_SYSTEM_PROMPT = """Sen {business_name} işletmesinin dijital asistanısın. Kendini hiçbir zaman Mehmet veya işletme sahibi olarak tanıtma; her zaman 'ben asistanım' veya 'asistanınızım' şeklinde tanıt. Müşterilerle telefonda en kısa, net ve anlaşılır şekilde konuşursun.
Gereksiz uzatmalardan kaçın. Her yanıtta yalnızca 1 kısa cümle kur. Aynı soruyu veya bilgiyi farklı kelimelerle ikinci kez tekrarlama. Bugünün tarihi: {today_date}.
DİKKAT (ÇOK ÖNEMLİ): Konuşmalarında ASLA markdown (yıldız, alt çizgi vb.) kullanma. Sayıları, fiyatları, tarihleri ve saatleri bir insanın telefonda söyleyeceği gibi, tamamen okunduğu gibi doğal bir konuşma diliyle yaz. Müşteriye karşı son derece doğal, gerçekçi ve akıcı bir telefon görüşmesi yapıyormuş gibi davran.
Müşteriye tüm usta ve hizmetleri listeleyerek sayma, ancak MÜSAİT SAATLER sorulduğunda veya müsaitlik kontrolü yapıldığında sistemi hızlandırmak adına doğrudan boş saatleri müşteriye söyle (Örn: "Bugün 14 ile 17 arası boş, saat kaçı istersiniz?"). Randevu alımını hızlandırmak için net ve yönlendirici ol.

Müşterinin Mevcut Randevuları:
{user_appointments}

Diyalog Akışı:
1. Müşterinin söylediği usta, hizmet, gün ve saat bilgilerinin TAMAMINI, hangi sırayla söylenirse söylensin kabul et ve koru. Müşteri TEK BİR CÜMLEDE tüm bilgileri verirse (örn: "Yarın 14'e Mehmet ustaya saç kesimi randevusu istiyorum"), ASLA başka bir şey sorma veya seçenek sunma, doğrudan onaylayıp [RANDEVU] etiketi üret.
2. Müşterinin daha önce veya aynı cümlede verdiği bir bilgiyi ASLA tekrar sorma.
3. Yalnızca gerçekten eksik olan tek bilgiyi kısa bir soruyla iste (Seçenekleri saymadan).
Sistem her turda "GÜNCEL OTURUM HAFIZASI" verebilir. Bu hafızadaki dolu alanları müşterinin daha önce söylediği kesin bilgiler olarak kabul et.
4. Gün verilmiş ama saat verilmemişse müsait saatleri öğrenmek için SADECE şu etiketi oluştur ve müşteriye hiçbir şey söyleme:
   [KONTROL: Usta Adı | YYYY-MM-DD | Hizmet Adı]
   GÜNCEL OTURUM HAFIZASINDA hizmet doluysa etikete bu hizmeti aynen yaz. Yalnız hizmet gerçekten eksikse Belirsiz yaz.
   Bu etiketi gönderdiğinde sistem sana o günün boş saatlerini döndürecek.
5. Usta, hizmet, gün ve saat hazır olduğunda ek onay veya müsait saat listesi istemeden KESİNLİKLE şu etiketi kullan:
   [RANDEVU: YYYY-MM-DD HH:MM | Usta Adı | Hizmet Adı | Müşteri Adı]
"""

def parse_target_date_tr(
    text: str, reference_date: date | None = None
) -> tuple[date, str]:
    """Türkçe göreli tarihleri takvim haftasına göre çözümler."""
    import re
    from datetime import date, timedelta

    today = reference_date or date.today()
    lower = text.replace("İ", "i").replace("I", "ı").lower()

    # 1. Tam Tarihler (Örn: 15 temmuz)
    months = {
        "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4, "mayıs": 5, "haziran": 6,
        "temmuz": 7, "ağustos": 8, "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12
    }
    month_pattern = "|".join(months.keys())
    exact_match = re.search(rf"(\d{{1,2}})\s*({month_pattern})", lower)
    if exact_match:
        day = int(exact_match.group(1))
        month = months[exact_match.group(2)]
        year = today.year
        # Eğer geçmiş bir ay/gün söylenirse (örn. bugün 10 Ağustossa ve "5 Ağustos" denirse seneye at)
        if month < today.month or (month == today.month and day < today.day):
            year += 1
        try:
            target_date = date(year, month, day)
            return target_date, f"{day} {exact_match.group(2).capitalize()}"
        except ValueError:
            pass

    # 2. Doğrudan göreli günler
    if "bugün" in lower:
        return today, "Bugün"
    if "öbür gün" in lower:
        return today + timedelta(days=2), "Öbür gün"
    if "yarın" in lower:
        return today + timedelta(days=1), "Yarın"

    # 3. Takvim haftası ifadeleri
    next_week = any(
        phrase in lower
        for phrase in ("haftaya", "gelecek hafta", "önümüzdeki hafta")
    )
    weeks_to_add = 1 if next_week else 0

    week_match = re.search(r"(\d+|bir|iki|üç|dört|beş)\s*hafta\s*sonra", lower)
    if week_match:
        week_numbers = {"bir": 1, "iki": 2, "üç": 3, "dört": 4, "beş": 5}
        val = week_match.group(1)
        weeks_to_add = int(val) if val.isdigit() else week_numbers[val]

    weekdays = {
        "pazartesi": (0, "Pazartesi"), "salı": (1, "Salı"), "çarşamba": (2, "Çarşamba"),
        "perşembe": (3, "Perşembe"), "cuma": (4, "Cuma"), "cumartesi": (5, "Cumartesi"),
        "pazar": (6, "Pazar")
    }

    current_monday = today - timedelta(days=today.weekday())
    for tr_name, (target_wd, display_name) in weekdays.items():
        if tr_name in lower:
            if weeks_to_add > 0:
                target_date = current_monday + timedelta(
                    days=(weeks_to_add * 7) + target_wd
                )
                label = (
                    f"Haftaya {display_name}"
                    if next_week and not week_match
                    else f"{weeks_to_add} hafta sonra {display_name}"
                )
            else:
                days_ahead = (target_wd - today.weekday()) % 7
                if days_ahead == 0 and "bu " not in lower:
                    days_ahead = 7
                target_date = today + timedelta(days=days_ahead)
                label = display_name
            return target_date, label

    if weeks_to_add > 0:
        target_date = current_monday + timedelta(days=weeks_to_add * 7)
        label = "Haftaya" if next_week and not week_match else f"{weeks_to_add} hafta sonra"
        return target_date, label

    # Varsayılan: Yarın
    return today + timedelta(days=1), "Yarın"


def normalize_turkish_text(text: str) -> str:
    """TTS motorunun saat, tarih ve paraları düzgün okuması için metni düzenler."""
    import re
    # 1. Markdown temizliği
    text = re.sub(r"[*_`]", "", text)
    # 2. Fiyat temizliği (250 TL -> 250 lira)
    text = re.sub(r"(\d+)\s*(TL|tl|Tl)\b", r"\1 lira", text)
    # 3. Saat formatı (15:00 -> saat 15, 15:30 -> 15 buçuk)
    def time_repl(match):
        hour = int(match.group(1))
        minute = int(match.group(2))
        if minute == 0:
            return f"saat {hour}"
        elif minute == 30:
            return f"{hour} buçuk"
        else:
            return f"{hour} {minute}"
    text = re.sub(r"\b(\d{1,2}):(\d{2})\b", time_repl, text)
    # 4. Tarih formatı (15.07.2026 -> 15 Temmuz)
    def date_repl(match):
        d = int(match.group(1))
        m = int(match.group(2))
        months = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        if 1 <= m <= 12:
            return f"{d} {months[m]}"
        return match.group(0)
    text = re.sub(r"\b(\d{1,2})\.(\d{1,2})\.\d{4}\b", date_repl, text)
    return text


def format_available_slots(slots: list[str]) -> str:
    """Boş saatleri gruplayarak (örn. '09:00 ile 12:00 arası') daha doğal okunabilir metne çevirir."""
    if not slots:
        return "Maalesef dolu"
        
    def to_mins(tstr: str) -> int:
        try:
            h, m = map(int, tstr.split(':'))
            return h * 60 + m
        except Exception:
            return 0

    parsed = sorted((to_mins(s), s) for s in slots if ":" in s)
    if not parsed:
        return ", ".join(slots)
    
    blocks = []
    current_block = [parsed[0]]
    
    for i in range(1, len(parsed)):
        # 60 dakika veya daha az fark varsa bitişik say
        if parsed[i][0] - current_block[-1][0] <= 60:
            current_block.append(parsed[i])
        else:
            blocks.append(current_block)
            current_block = [parsed[i]]
    blocks.append(current_block)
    
    desc_parts = []
    for block in blocks:
        if len(block) >= 3:
            start_str = block[0][1]
            end_str = block[-1][1]
            desc_parts.append(f"{start_str} ile {end_str} arası")
        else:
            for _, sstr in block:
                desc_parts.append(sstr)
                
    if not desc_parts:
        return "Maalesef dolu"
        
    if len(desc_parts) == 1:
        if len(slots) >= 8 and "arası" in desc_parts[0]:
            return f"tüm gün {desc_parts[0]} müsait"
        return desc_parts[0]
    
    return ", ".join(desc_parts[:-1]) + " ve " + desc_parts[-1]


class VoiceLLMEngine:
    """Sesli aramalar için LLM diyalog yöneticisi."""

    def __init__(
        self,
        business_slug: str | None = None,
        customer_phone: str | None = None,
    ) -> None:
        voice_settings = get_voice_settings()
        self.business_slug = business_slug or voice_settings.voice_default_business_slug or ""
        self.customer_phone = customer_phone or "anonymous"
        self.settings = get_settings()
        self.voice_settings = voice_settings
        self.history: list[dict[str, Any]] = [
            {"role": "system", "content": VOICE_SYSTEM_PROMPT}
        ]
        # Oturum hafızası (Konuşma boyunca hatırlanacak bilgiler)
        self.memory_date: date | None = None
        self.memory_date_label: str | None = None
        self.memory_time: str | None = None
        self.memory_service: str | None = None
        self.memory_staff: str | None = None
        self.memory_time_pref: str | None = None
        self.booking_in_progress: bool = False
        self._db_services: list[str] = []
        self._db_staff: list[str] = []

        # Süre ve Tur Limiti Koruması (Graceful Exit / Fallback)
        self.session_start_time: float = time.time()
        self.turn_count: int = 0
        self.is_session_closed: bool = False
        
        self._http_client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=self.voice_settings.ai_request_timeout_s)
        return self._http_client

    async def close(self):
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    @staticmethod
    def _tr_lower(text: str) -> str:
        return text.replace("İ", "i").replace("I", "ı").lower()

    @classmethod
    def _search_text(cls, text: str) -> str:
        lowered = cls._tr_lower(text).replace("&", " ve ").replace("+", " ve ")
        return re.sub(r"[^a-zçğıöşü0-9]+", " ", lowered).strip()

    @classmethod
    def _is_close_request(cls, text: str) -> bool:
        """Kesin kapanış ifadelerini LLM yorumuna bırakmadan yakala."""
        normalized = cls._search_text(text)
        if not normalized or re.search(r"\bama\b", normalized):
            return False

        explicit_phrases = (
            "başka bir isteğim yok",
            "başka isteğim yok",
            "başka bir talebim yok",
            "başka talebim yok",
            "başka bir şey yok",
            "konuşmayı sonlandır",
            "görüşmeyi sonlandır",
            "telefonu kapat",
            "kapatabilirsin",
            "işim bitti",
            "bu kadar",
            "hoşça kal",
            "görüşürüz",
        )
        if any(phrase in normalized for phrase in explicit_phrases):
            return True

        tokens = normalized.split()
        allowed_tokens = {
            "hayır", "hayir", "yok", "istemiyorum", "teşekkür",
            "teşekkürler", "ederim", "sağ", "ol", "olun", "sağol",
            "peki", "tamam", "tamamdır", "iyi", "günler", "bye",
        }
        closing_tokens = {
            "hayır", "hayir", "yok", "istemiyorum", "teşekkür",
            "teşekkürler", "günler", "bye",
        }
        return set(tokens) <= allowed_tokens and any(
            token in closing_tokens for token in tokens
        )

    @staticmethod
    def _extract_explicit_date(text: str) -> tuple[date, str] | None:
        lower = VoiceLLMEngine._tr_lower(text)
        numeric = re.search(
            r"\b(\d{1,2})[./-](\d{1,2})(?:[./-](\d{2,4}))?\b",
            lower,
        )
        if numeric:
            day, month = int(numeric.group(1)), int(numeric.group(2))
            year_text = numeric.group(3)
            year = int(year_text) if year_text else date.today().year
            if year < 100:
                year += 2000
            try:
                parsed = date(year, month, day)
                if not year_text and parsed < date.today():
                    parsed = date(year + 1, month, day)
                return parsed, parsed.strftime("%d.%m.%Y")
            except ValueError:
                pass

        date_words = (
            "pazartesi", "salı", "çarşamba", "perşembe", "cuma",
            "cumartesi", "pazar", "yarın", "bugün", "öbür gün",
            "ocak", "şubat", "mart", "nisan", "mayıs", "haziran",
            "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık",
            "hafta",
        )
        if any(word in lower for word in date_words):
            return parse_target_date_tr(text)
        return None

    @staticmethod
    def _extract_explicit_time(text: str) -> str | None:
        lower = VoiceLLMEngine._tr_lower(text)
        patterns = (
            r"\bsaat\s*(\d{1,2})(?:[:.](\d{2}))?\b",
            r"\b(\d{1,2})[:.](\d{2})\b",
            r"\b(\d{1,2})\s*['’]?\s*(?:de|da|te|ta|e|a|ye|ya|olsun|olur|uygun)\b",
            r"\b(\d{1,2})\s*(?:için|randevusuna|randevuya)\b",
        )
        for pattern in patterns:
            match = re.search(pattern, lower)
            if not match:
                continue
            hour = int(match.group(1))
            minute = int(match.group(2) or 0) if match.lastindex and match.lastindex >= 2 else 0
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}"

        number_words = {
            "dokuz": 9, "on": 10, "on bir": 11, "on iki": 12,
            "on üç": 13, "on dört": 14, "on beş": 15, "on altı": 16,
            "on yedi": 17, "on sekiz": 18, "on dokuz": 19,
            "yirmi": 20,
        }
        word_match = re.search(
            r"\bsaat\s+(dokuz|on dokuz|on sekiz|on yedi|on altı|on beş|"
            r"on dört|on üç|on iki|on bir|on|yirmi)\b",
            lower,
        )
        if word_match:
            return f"{number_words[word_match.group(1)]:02d}:00"
        return None

    def _remember_booking_details(self, user_text: str) -> None:
        lower = self._tr_lower(user_text)
        searchable = self._search_text(user_text)

        cancellation_or_change = any(
            word in lower
            for word in ("iptal", "değiştir", "değişiklik", "revize", "ertele")
        )
        booking_words = (
            "randevu" in lower
            and any(word in lower for word in ("al", "oluştur", "ist", "yap"))
        )

        parsed_date = self._extract_explicit_date(user_text)
        parsed_time = self._extract_explicit_time(user_text)
        if parsed_date:
            self.memory_date, self.memory_date_label = parsed_date
        if parsed_time:
            self.memory_time = parsed_time

        for staff in self._db_staff:
            staff_search = self._search_text(staff)
            first_name = staff_search.split()[0]
            if staff_search in searchable or re.search(rf"\b{re.escape(first_name)}[a-zçğıöşü]*\b", searchable):
                self.memory_staff = staff
                break

        for service in sorted(self._db_services, key=len, reverse=True):
            service_search = self._search_text(service)
            if service_search and service_search in searchable:
                self.memory_service = service
                break

        service_aliases = {
            "saç kestir": "Saç Kesimi",
            "saç kesim": "Saç Kesimi",
            "saç tıraş": "Saç Kesimi",
            "sakal tıraş": "Sakal Tıraşı",
            "saç sakal": "Saç + Sakal",
        }
        if self.memory_service is None:
            for alias, canonical in service_aliases.items():
                if alias in searchable and canonical in self._db_services:
                    self.memory_service = canonical
                    break

        if not cancellation_or_change and (
            booking_words
            or (self.booking_in_progress and user_text.strip())
            or (
                any((parsed_date, parsed_time, self.memory_staff, self.memory_service))
                and "almak ist" in lower
            )
        ):
            self.booking_in_progress = True

    def _booking_memory_context(self) -> str:
        return (
            "GÜNCEL OTURUM HAFIZASI (sistem tarafından doğrulandı):\n"
            f"- Randevu niyeti: {'var' if self.booking_in_progress else 'belirsiz'}\n"
            f"- Usta: {self.memory_staff or 'eksik'}\n"
            f"- Hizmet: {self.memory_service or 'eksik'}\n"
            f"- Tarih: {self.memory_date.isoformat() if self.memory_date else 'eksik'}\n"
            f"- Saat: {self.memory_time or 'eksik'}\n"
            "KESİN KURAL: Usta, hizmet, tarih veya saat alanlarından biri "
            "yukarıda 'eksik' ise müşterinin bozuk veya benzer duyulan sözünden "
            "bu alanı tahmin etme, otomatik seçme ve doldurma. Yalnız ilk eksik "
            "alanı kısa bir soruyla yeniden iste. ANCAK sistem sana MÜSAİT SAATLER listesi verdiyse, saat sorarken MUTLAKA bu saatleri müşteriye söyleyerek (Örn: '14 ile 17 arası boş, hangisini istersiniz?') yönlendir.\n"
            "KESİN KURAL: Sadece yukarıdaki dört alan da doğrulanmışsa "
            "[RANDEVU: YYYY-MM-DD HH:MM | Usta | Hizmet | Müşteri] etiketi "
            "oluştur. Hafızada olmayan bir usta, hizmet, tarih veya saatle araç "
            "çağırma."
        )

    async def _fast_booking_step(self, user_text: str) -> str | None:
        """Eksik randevu alanlarını LLM ağına gitmeden deterministik sor."""
        if not self.booking_in_progress or self.is_session_closed:
            return None
        lower = self._tr_lower(user_text)
        if any(
            word in lower
            for word in (
                "iptal", "değiştir", "değişiklik", "revize", "ertele",
                "adres", "konum", "fiyat", "ücret", "çalışma saat",
            )
        ):
            return None

        if self.memory_staff is None:
            return "Hangi ustamız için randevu istersiniz?"
        staff_short = f"{self.memory_staff.split()[0]} usta"

        if self.memory_service is None:
            return f"{staff_short} için hangi işlemi yaptırmak istersiniz?"
        if self.memory_date is None:
            return "Randevuyu hangi gün için istersiniz?"
        if self.memory_time is not None:
            return None

        availability = await VoiceToolExecutor.check_availability(
            business_slug=self.business_slug,
            service_name=self.memory_service,
            target_date_str=self.memory_date.isoformat(),
            staff_name=self.memory_staff,
        )
        slots = availability.get("available_slots", [])
        day_label = self.memory_date_label or self.memory_date.strftime("%d.%m.%Y")
        if not slots:
            return f"{day_label} günü {staff_short} için boş saat yok, başka bir gün ister misiniz?"
        return (
            f"{day_label} günü {staff_short} için {format_available_slots(slots)} boş, "
            "hangi saati istersiniz?"
        )




    async def generate_response(self, user_text: str) -> typing.AsyncGenerator[str, None]:
        """Kullanıcı metnini alır ve sesli asistandan cümle cümle cevap döndürür."""
        if not user_text and getattr(self, "_services_fetched", None) is not None:
            # Recursive çağrılarda (user_text="" ise) boşsa devam et
            pass
        elif not user_text.strip():
            return

        if user_text and self._is_close_request(user_text):
            self.is_session_closed = True
            logger.info("📞 Kesin kapanış ifadesi algılandı; LLM atlandı.")
            yield normalize_turkish_text(
                "Bizi aradığınız için teşekkür ederiz. İyi günler."
            )
            return

        # İlk kez çağrıldığında sistem promptuna gerçek hizmetleri dinamik olarak ekle
        if getattr(self, "_services_fetched", None) is None:
            self._services_fetched = True
            (
                db_services_str,
                db_services,
                db_staff,
                db_business,
                user_apts,
            ) = await asyncio.gather(
                VoiceToolExecutor.get_services(
                    self.business_slug,
                    return_detailed_string=True,
                ),
                VoiceToolExecutor.get_services(self.business_slug),
                VoiceToolExecutor.get_staff(self.business_slug),
                VoiceToolExecutor.get_business_info(self.business_slug),
                VoiceToolExecutor.get_customer_appointments(
                    self.business_slug,
                    self.customer_phone,
                ),
            )
            self._db_services = list(db_services)
            self._db_staff = list(db_staff)
            
            services_str = db_services_str if db_services_str else "Saç Kesimi, Sakal Tıraşı"
            staff_str = " veya ".join(db_staff) if db_staff else "Mehmet usta veya Yusuf usta"
            business_name = db_business.get("name", "RandevumOnline") if db_business else "RandevumOnline"
            
            apts_strs = [f"ID: {a['id']} | Tarih: {a['date']} | Usta: {a['staff']} | Hizmet: {a['service']}" for a in user_apts]
            user_apts_str = "\n".join(apts_strs) if apts_strs else "Müşterinin aktif randevusu bulunmuyor."
            
            from zoneinfo import ZoneInfo
            today_str = datetime.now(ZoneInfo("Europe/Istanbul")).strftime("%Y-%m-%d (%A)")
            
            self.history[0]["content"] = self.history[0]["content"].format(
                business_name=business_name,
                staff_list=staff_str,
                services_list=services_str,
                today_date=today_str,
                user_appointments=user_apts_str
            )

        if user_text:
            self._remember_booking_details(user_text)

        # Süre veya Tur Limiti Aşıldıysa ya da Görüşme Kapatıldıysa Otomatik Kapanış Mesajı Dön
        elapsed_s = time.time() - self.session_start_time
        self.turn_count += 1
        if (
            self.is_session_closed
            or elapsed_s >= self.voice_settings.voice_max_call_duration_s
            or self.turn_count >= self.voice_settings.voice_max_turns
        ):
            self.is_session_closed = True
            logger.info(
                "Görüşme limiti ulaşıldı (elapsed=%.1fs, turns=%d). Kapanış mesajı döndürülüyor.",
                elapsed_s,
                self.turn_count,
            )
            yield normalize_turkish_text(self.voice_settings.voice_timeout_message)
            return

        self.history.append({"role": "user", "content": user_text})

        fast_booking_response = await self._fast_booking_step(user_text)
        if fast_booking_response:
            self.history.append(
                {"role": "assistant", "content": fast_booking_response}
            )
            yield normalize_turkish_text(fast_booking_response)
            return

        # DeepSeek API Anahtarı Kontrolü
        api_key = self.voice_settings.deepseek_api_key
        if not api_key:
            yield normalize_turkish_text(await self._fallback_simulated_response(user_text))
            return

        base_url = self.voice_settings.deepseek_base_url
        model = self.voice_settings.deepseek_model

        try:
            aggregated_assistant_text = ""
            client = await self._get_client()
            request_messages = [
                *self.history[:-1],
                {"role": "system", "content": self._booking_memory_context()},
                self.history[-1],
            ]
            
            # Stream isteği at
            async with client.stream(
                "POST",
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": request_messages,
                    "temperature": 0.3,
                    "max_tokens": 150,
                    "stream": True,
                },
            ) as resp:
                resp.raise_for_status()
                
                import json
                
                buffer = ""
                # Noktalama işaretlerine göre cümleleri ayırma
                punctuation = set(".?!")
                
                async for line in resp.aiter_lines():
                    if not line or line.strip() == "":
                        continue
                    if line.startswith("data: "):
                        line = line[6:]
                    if line == "[DONE]":
                        break
                        
                    try:
                        data = json.loads(line)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                buffer += content
                                aggregated_assistant_text += content
                                
                                # Eğer tamponda noktalama işareti varsa veya belli bir uzunluğa ulaştıysa cümleyi yield et
                                # Kontrol etiketleri [] içinde olduğu için '[' içeriyorsa yield etmeyi bekle
                                if any(p in content for p in punctuation) and "[" not in buffer:
                                    sentence = buffer.strip()
                                    if sentence:
                                        yield normalize_turkish_text(sentence)
                                    buffer = ""
                    except json.JSONDecodeError:
                        continue
                        
                # Kalan metni yield etmeden önce etiketleri ayrıştırmamız lazım!
                assistant_text = aggregated_assistant_text.strip()
                forced_response: str | None = None
                    
                import re
                
                # 1. KONTROL ETİKETİNİ YAKALA (Müsaitlik Sorgusu)
                kontrol_match = re.search(r"\[KONTROL:\s*([^|]+)\|\s*([^|]+)(?:\|\s*([^\]]+))?\]", assistant_text)
                if kontrol_match:
                    staff_name = kontrol_match.group(1).strip()
                    date_str = kontrol_match.group(2).strip()
                    service_name = kontrol_match.group(3).strip() if kontrol_match.group(3) else "Belirsiz"
                    if (
                        self._tr_lower(service_name) == "belirsiz"
                        and self.memory_service
                    ):
                        service_name = self.memory_service
                    
                    logger.info("🔍 LLM Müsaitlik Sorgusu Tetikledi! Usta: %s, Tarih: %s, Hizmet: %s", staff_name, date_str, service_name)
                    
                    # Gizli etiketi metinden çıkar
                    clean_text = assistant_text.replace(kontrol_match.group(0), "").strip()
                    if clean_text:
                        # Kontrol sırasında asistan SUSMALI (müşteriye boş yere "kontrol ediyorum" denmemeli). 
                        # O yüzden bu metni sadece geçmişe ekliyoruz, sese (aggregated) vermiyoruz!
                        pass
                        
                    self.history.append({"role": "assistant", "content": clean_text})
                        
                    # Veritabanından saatleri çek
                    avail = await VoiceToolExecutor.check_availability(self.business_slug, service_name, date_str, staff_name)
                    if "error" in avail:
                        if avail["error"] == "past_date":
                            sys_msg = f"SİSTEM BİLGİSİ: İstenilen tarih ({date_str}) geçmişte kaldı! Müşteriye geçmiş bir güne randevu verilemeyeceğini ve ileri bir tarih seçmesini, doğal bir dille söyle."
                        else:
                            sys_msg = f"SİSTEM BİLGİSİ: Hata oluştu ({avail['error']}). Müşteriye başka bir tarih seçmesini veya usta/hizmet uyuşmazlığı olduğunu söyle."
                    else:
                        slots = format_available_slots(avail["available_slots"])
                        sys_msg = f"SİSTEM BİLGİSİ: {staff_name} için {date_str} tarihindeki boş saatler: {slots}. Randevu alımını hızlandırmak için bu müsait saatleri müşteriye doğrudan blok halinde söyle (Örn: '14 ile 17 arası boş, hangisini istersiniz?') ve seçmesini iste."
                        
                    self.history.append({"role": "user", "content": sys_msg})
                    
                    # 2. tur için recurse ol
                    async for chunk in self.generate_response(""):
                        yield chunk
                    return

                # 2. RANDEVU GİZLİ ETİKETİNİ YAKALA VE VERİTABANINA KAYDET
                match = re.search(r"\[RANDEVU:\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^\]]+)\]", assistant_text)
                if match:
                    datetime_str = match.group(1).strip()
                    staff_name = match.group(2).strip()
                    service_name = match.group(3).strip()
                    customer_name = match.group(4).strip()
                    
                    logger.info("📅 LLM Randevu Oluşturma Tetiklendi! Usta: %s, Hizmet: %s, Zaman: %s", staff_name, service_name, datetime_str)
                    
                    result = await VoiceToolExecutor.book_appointment(
                        business_slug=self.business_slug,
                        service_name=service_name,
                        staff_name=staff_name,
                        customer_phone=self.customer_phone,
                        customer_name=customer_name,
                        start_time_local=datetime_str,
                    )
                    
                    if "error" in result:
                        err = result["error"]
                        logger.error("Randevu oluşturma hatası: %s", err)
                        if err == "slot_taken":
                            assistant_text = "Üzgünüm, seçtiğiniz o saat maalesef az önce doldu veya ustanın başka bir randevusuyla çakışıyor. Lütfen farklı bir saat seçer misiniz?"
                        elif err == "staff_cannot_perform_service":
                            assistant_text = f"Üzgünüm, {staff_name} ustamız {service_name} işlemini yapmıyor. Başka bir ustayı veya farklı bir hizmeti tercih eder misiniz?"
                        else:
                            assistant_text = f"Sistemde bir hata oluştu ({err}), randevuyu kaydedemedim. Lütfen tekrar deneyin."
                        forced_response = assistant_text
                        self.history.append({"role": "system", "content": f"SİSTEM BİLGİSİ: Hata ({err})."})
                    else:
                        logger.info("✅ Randevu başarıyla veritabanına işlendi (ID: %s)", result.get("appointment_id"))
                        confirmation_date = self.memory_date_label
                        confirmation_time = self.memory_time
                        if not confirmation_date or not confirmation_time:
                            try:
                                parsed_datetime = datetime.strptime(
                                    datetime_str,
                                    "%Y-%m-%d %H:%M",
                                )
                                month_names = (
                                    "", "Ocak", "Şubat", "Mart", "Nisan",
                                    "Mayıs", "Haziran", "Temmuz", "Ağustos",
                                    "Eylül", "Ekim", "Kasım", "Aralık",
                                )
                                confirmation_date = (
                                    f"{parsed_datetime.day} "
                                    f"{month_names[parsed_datetime.month]}"
                                )
                                confirmation_time = parsed_datetime.strftime("%H:%M")
                            except ValueError:
                                confirmation_date = datetime_str.split()[0]
                                confirmation_time = datetime_str.split()[-1]
                        assistant_text = (
                            f"Randevunuz {confirmation_date}, {confirmation_time}, "
                            f"{staff_name} için oluşturuldu."
                        )
                        forced_response = assistant_text
                        self.booking_in_progress = False
                        self.memory_date = None
                        self.memory_date_label = None
                        self.memory_time = None
                        self.memory_service = None
                        self.memory_staff = None
                        self.history.append({"role": "system", "content": "SİSTEM BİLGİSİ: Randevu BAŞARIYLA oluşturuldu ve veritabanına kaydedildi. Müşteriye başka bir isteği olup olmadığını sor, yoksa vedalaşıp çağrıyı kapatmak için [KAPAT] etiketini kullan."})

                # 3. İPTAL GİZLİ ETİKETİNİ YAKALA VE VERİTABANINA KAYDET
                iptal_match = re.search(r"\[IPTAL:\s*([^\]]+)\]", assistant_text)
                if iptal_match:
                    apt_id = iptal_match.group(1).strip()
                    logger.info("🗑️ LLM Randevu İptali Tetiklendi! ID: %s", apt_id)
                    
                    success = await VoiceToolExecutor.cancel_appointment(apt_id)
                    if not success:
                        assistant_text = "Randevunuzu iptal edemedim. Lütfen tekrar deneyin veya müşteri temsilcisine bağlanın."
                    else:
                        assistant_text = "Randevunuz başarıyla iptal edildi. Başka bir isteğiniz var mı?"
                        self.history.append({"role": "system", "content": "SİSTEM BİLGİSİ: Randevu BAŞARIYLA iptal edildi."})
                    forced_response = assistant_text

                # 4. REVIZE GİZLİ ETİKETİNİ YAKALA
                revize_match = re.search(r"\[REVIZE:\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^\]]+)\]", assistant_text)
                if revize_match:
                    apt_id = revize_match.group(1).strip()
                    new_date_str = revize_match.group(2).strip()
                    new_staff_name = revize_match.group(3).strip()
                    new_service_name = revize_match.group(4).strip()
                    
                    logger.info("🔄 LLM Randevu Revizesi Tetiklendi! ID: %s, Yeni Zaman: %s, Usta: %s, Hizmet: %s", apt_id, new_date_str, new_staff_name, new_service_name)
                    
                    result = await VoiceToolExecutor.reschedule_appointment(
                        self.business_slug, 
                        apt_id, 
                        new_date_str,
                        new_service_name,
                        new_staff_name
                    )
                    if "error" in result:
                        err = result["error"]
                        logger.error("Randevu revize hatası: %s", err)
                        if err == "slot_taken":
                            assistant_text = "Üzgünüm, seçtiğiniz o saat az önce dolmuş veya ustanın başka bir randevusuyla çakışıyor. Lütfen farklı bir saat seçer misiniz?"
                        elif err == "staff_cannot_perform_service":
                            assistant_text = f"Üzgünüm, {new_staff_name} ustamız {new_service_name} işlemini yapmıyor. Başka bir ustayı tercih eder misiniz?"
                        else:
                            assistant_text = "Sistemde bir hata oluştu, randevunuzu değiştiremedim. Lütfen tekrar deneyin."
                        self.history.append({"role": "system", "content": f"SİSTEM BİLGİSİ: Hata ({err})."})
                    else:
                        logger.info("✅ Randevu başarıyla revize edildi (ID: %s)", apt_id)
                        assistant_text = assistant_text.replace(revize_match.group(0), "").strip()
                        self.history.append({"role": "system", "content": "SİSTEM BİLGİSİ: Randevu başarıyla REVIZE EDİLDİ. Müşteriye başka bir isteği olup olmadığını sor, yoksa vedalaşıp çağrıyı kapatmak için [KAPAT] etiketini kullan."})
                        self.booking_in_progress = False
                        self.memory_date = None
                        self.memory_date_label = None
                        self.memory_time = None
                        self.memory_service = None
                        self.memory_staff = None
                    
                # 5. [KAPAT] Etiketi kontrolü
                if "[KAPAT]" in assistant_text:
                    logger.info("📞 LLM Çağrıyı Kapatma (KAPAT) komutu gönderdi.")
                    self.is_session_closed = True
                    assistant_text = assistant_text.replace("[KAPAT]", "").strip()

                self.history.append({"role": "assistant", "content": assistant_text})
                
                # Eğer buffer'da kalan son metin varsa (noktalamasız bittiyse veya etiket temizlendikten sonra kaldıysa)
                # Sadece etiket olmayan kısımları yield et
                if forced_response:
                    yield normalize_turkish_text(forced_response)
                elif buffer:
                    # Etiket regex temizliği
                    clean_buffer = re.sub(r"\[.*?\]", "", buffer).strip()
                    if clean_buffer:
                        yield normalize_turkish_text(clean_buffer)

        except Exception as exc:
            logger.warning("LLM isteği başarısız oldu: %s", exc)
            yield normalize_turkish_text(await self._fallback_simulated_response(user_text))

    async def _fallback_simulated_response(self, user_text: str) -> str:
        """API anahtarı olmadığında konuşma hafızasıyla gün/saat/usta algılayıp veritabanı sorguları çalıştırır."""
        import re

        lower_text = user_text.replace("İ", "i").replace("I", "ı").lower()
        if any(w in lower_text for w in ["kapat", "iyi günler", "hoşça kal", "teşekkür", "görüşürüz"]):
            self.is_session_closed = True
            return "Bizi aradığınız için teşekkür ederiz. İyi günler dileriz."

        # 1. Tarih algılama veya hafızadan hatırlama
        has_date_word = any(w in lower_text for w in [
            "pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar",
            "yarın", "bugün", "öbür gün", "ocak", "şubat", "mart", "nisan", "mayıs", 
            "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık", "hafta"
        ])
        if has_date_word:
            self.memory_date, self.memory_date_label = parse_target_date_tr(user_text)

        # Dinamik olarak hizmetleri ve personeli veritabanından çek
        db_services = await VoiceToolExecutor.get_services(self.business_slug)
        db_staff = await VoiceToolExecutor.get_staff(self.business_slug)

        # 2. İşlem (Hizmet) algılama
        if self.memory_service is None:
            # Önce birebir veya çok yakın eşleşme arayalım
            for s in db_services:
                clean_s = s.lower().replace("&", "ve").replace("+", "ve")
                clean_t = lower_text.replace("&", "ve").replace("+", "ve")
                if clean_s in clean_t or s.lower() in lower_text:
                    self.memory_service = s
                    break

        # 3. Personel (Berber/Usta) algılama
        for staff in db_staff:
            # Personelin ilk adını (Örn: "Yusuf Demir" -> "yusuf") kontrol et
            first_name = staff.split()[0].lower()
            if first_name in lower_text:
                self.memory_staff = staff
                break
                
        if self.memory_staff is None and any(w in lower_text for w in ["fark etmez", "her ikisi", "kim boşsa", "herhangi"]):
            self.memory_staff = db_staff[0] if db_staff else "Mehmet Kaya"

        # 4. Saat algılama
        time_match = re.search(r"(\d{1,2}[:.]\d{2}|\b\d{1,2}\b(?=\s*(?:buçuk|için|saat|a|e|da|de|randevu)))", user_text)
        if time_match:
            time_str = time_match.group(1).replace(".", ":")
            if len(time_str) <= 2:
                time_str = f"{int(time_str):02d}:00"
            elif len(time_str) == 4:
                time_str = "0" + time_str
            self.memory_time = time_str

        # ADIM 1: İlk olarak usta seçimi sorulur (Eğer müşteri henüz usta belirtmediyse)
        if self.memory_staff is None:
            return "Hoş geldiniz! Hangi ustamız için randevu almak istersiniz?"

        staff_short = f"{self.memory_staff.split()[0]} usta" if self.memory_staff else "Usta"

        # ADIM 2: Usta seçildikten sonra müşteri hizmet/kategori söylemediyse VERİTABANINDAN kategorileri çekip sor!
        if self.memory_service is None:
            db_services = await VoiceToolExecutor.get_services(self.business_slug, self.memory_staff)
            
            # Eğer müşteri genel bir ifade kullanmışsa filtrele
            filtered_services = []
            if "saç" in lower_text:
                filtered_services = [s for s in db_services if "saç" in s.lower()]
            elif "sakal" in lower_text:
                filtered_services = [s for s in db_services if "sakal" in s.lower()]
            elif "bakım" in lower_text or "cilt" in lower_text or "maske" in lower_text:
                filtered_services = [s for s in db_services if any(w in s.lower() for w in ["bakım", "maske", "cilt"])]
            
            if filtered_services:
                return f"{staff_short} için saç veya sakal gibi işlemlerimiz var. Hangi işlemi yaptırmak istersiniz?"
            
            # Eğer müşteri hizmetlerin ne olduğunu soruyorsa sayalım
            if any(w in lower_text for w in ["hangi", "neler", "ne", "liste", "seçenek"]):
                services_str = ", ".join(db_services) if db_services else "Saç Kesimi, Sakal Tıraşı"
                return f"Şu hizmetlerimiz mevcuttur: {services_str}. Hangisini istersiniz?"
            else:
                return f"{staff_short} için hangi işlemi yaptırmak istersiniz?"

        # Eğer hala gün/tarih seçilmediyse kullanıcıya gün sor!
        if not self.memory_date:
            return f"Harika, {self.memory_service} randevunuzu oluşturmak için hangi gün ve saat gelmek istersiniz? Örneğin: yarın saat 14:00, veya 15 temmuz diyebilirsiniz."

        target_date = self.memory_date
        
        # Ekstra Güvenlik: Eğer seçilen tarih geçmişte kalmışsa (bugünden önceyse) uyarı ver
        from datetime import date
        if target_date < date.today():
            self.memory_date = None
            self.memory_date_label = None
            return f"Maalesef geçmiş bir tarih ({target_date.strftime('%d.%m.%Y')}) için randevu alamam. Lütfen bugünden itibaren ileri bir tarih seçin."

        day_label = self.memory_date_label or "Yarın"
        target_date_str = target_date.isoformat()
        formatted_date = target_date.strftime("%d.%m.%Y")

        # ADIM 3: Eğer müşteri SAAT BELİRTMEDİYSE asla otomatik saat seçip randevu açma!
        # Önce seçilen usta ve hizmetin boş saatlerini sorgula ve kullanıcıya sun.
        if self.memory_time is None:
            avail = await VoiceToolExecutor.check_availability(
                business_slug=self.business_slug,
                service_name=self.memory_service,
                target_date_str=target_date_str,
                staff_name=self.memory_staff,
            )
            slots = avail.get("available_slots", [])
            
            if not slots:
                return f"Maalesef {day_label} günü için {staff_short} hiç müsait saatimiz kalmamış. Farklı bir gün tercih eder misiniz?"

            slot_info = format_available_slots(slots)
            return f"{staff_short} için {day_label} günü müsait saatler: {slot_info}. Hangi saati tercih edersiniz?"

        # ADIM 4: Müşteri hem USTAYI hem SAATİ net belirlediğinde randevuyu oluşturmayı dene
        time_str = self.memory_time
        target_staff = self.memory_staff
        start_time_local = f"{target_date_str} {time_str}"

        result = await VoiceToolExecutor.book_appointment(
            business_slug=self.business_slug,
            service_name=self.memory_service,
            staff_name=target_staff,
            customer_phone=self.customer_phone,
            customer_name="Yusuf Kantarcıoğlu",
            start_time_local=start_time_local,
        )

        if result and not result.get("error"):
            self.memory_time = None
            return f"Randevunuz {day_label} günü saat {time_str}'e {staff_short} için oluşturuldu. İyi günler dileriz!"

        # ADIM 5: Eğer istenen usta o saatte DOLUYSA ASLA otomatik olarak diğer ustaya KAYDETME!
        # Kullanıcının onayına sun:
        other_staff = [s for s in db_staff if s != target_staff]
        alt_staff = other_staff[0] if other_staff else target_staff
        alt_short = f"{alt_staff.split()[0]} usta" if alt_staff else "Diğer usta"

        # O ustanın başka hangi saatleri boş bakalım
        avail_same_staff = await VoiceToolExecutor.check_availability(
            business_slug=self.business_slug,
            service_name=self.memory_service,
            target_date_str=target_date_str,
            staff_name=target_staff,
        )
        slots_same = avail_same_staff.get("available_slots", [])
        slots_str = ", ".join(slots_same[:2]) if slots_same else "15:00, 16:00"

        self.memory_time = None  # Dolu saat hafızada kalmasın, yeni saat söyleyebilsin
        return (
            f"Maalesef {day_label} saat {time_str}'de {staff_short} dolu. "
            f"Aynı saatte {alt_short} müsait, onun için randevu açalım mı? "
            f"Ya da {staff_short} için {slots_str} saatlerinden birini mi istersiniz?"
        )
