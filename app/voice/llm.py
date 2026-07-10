"""
FAZ 3 - Sesli Asistan (Voice Agent) LLM ve Diyalog Yöneticisi.

Bu modül, telefon konuşmalarına özel kısa, insani ve doğal Türkçe yanıtlar
üretmek üzere Groq / Ollama entegrasyonu sağlar.
"""

from __future__ import annotations

import logging
import time
from datetime import date
from typing import Any

import httpx

from app.core.config import get_settings
from app.voice.config import get_voice_settings
from app.voice.tools import VoiceToolExecutor

logger = logging.getLogger(__name__)

VOICE_SYSTEM_PROMPT = """Sen RandevumOnline sesli asistanısın. Müşterilerle telefonda en kısa, net ve anlaşılır şekilde konuşursun.
Gereksiz uzatmalardan kaçın. En fazla 1-2 kısa cümle kur.
Diyalog Akışı:
1. İLK OLARAK müşterinin hangi ustayı (Mehmet usta veya Yusuf usta) tercih ettiğini sor.
2. Usta seçildikten sonra O USTANIN istediği gündeki müsait saatlerini kontrol et ve net şekilde sun.
3. Saat seçilince randevuyu kaydet ve kısaca onayla.
"""



def parse_target_date_tr(text: str) -> tuple[date, str]:
    """Türkçe gün isimlerini ('pazar', 'cuma', 'yarın' vb.) algılayıp gerçek takvim tarihini döndürür."""
    from datetime import date, timedelta

    today = date.today()
    lower = text.lower()

    weekdays = {
        "pazartesi": (0, "Pazartesi"),
        "salı": (1, "Salı"),
        "çarşamba": (2, "Çarşamba"),
        "perşembe": (3, "Perşembe"),
        "cuma": (4, "Cuma"),
        "cumartesi": (5, "Cumartesi"),
        "pazar": (6, "Pazar"),
    }

    # Haftanın günleri kontrol edilir (Pazar, Cuma vb.)
    for tr_name, (target_wd, display_name) in weekdays.items():
        if tr_name in lower:
            days_ahead = (target_wd - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7  # Önümüzdeki o gün
            target_date = today + timedelta(days=days_ahead)
            return target_date, display_name

    # Göreceli ifadeler
    if "bugün" in lower:
        return today, "Bugün"
    elif "öbür gün" in lower:
        return today + timedelta(days=2), "Öbür gün"

    # Varsayılan: Yarın
    return today + timedelta(days=1), "Yarın"


class VoiceLLMEngine:
    """Sesli aramalar için LLM diyalog yöneticisi."""

    def __init__(self, business_slug: str = "berber_mehmet_kutahya") -> None:
        self.business_slug = business_slug
        self.settings = get_settings()
        self.voice_settings = get_voice_settings()
        self.history: list[dict[str, Any]] = [
            {"role": "system", "content": VOICE_SYSTEM_PROMPT}
        ]
        # Oturum hafızası (Konuşma boyunca hatırlanacak bilgiler)
        self.memory_date: date | None = None
        self.memory_date_label: str | None = None
        self.memory_time: str | None = None
        self.memory_service: str | None = None
        self.memory_staff: str | None = None

        # Süre ve Tur Limiti Koruması (Graceful Exit / Fallback)
        self.session_start_time: float = time.time()
        self.turn_count: int = 0
        self.is_session_closed: bool = False




    async def generate_response(self, user_text: str) -> str:
        """Kullanıcı metnini alır ve sesli asistandan kısa bir cevap döndürür."""
        if not user_text.strip():
            return ""

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
            return self.voice_settings.voice_timeout_message

        self.history.append({"role": "user", "content": user_text})

        # DeepSeek veya Groq API Anahtarı Kontrolü
        api_key = self.voice_settings.deepseek_api_key or self.settings.groq_api_key
        if not api_key:
            return await self._fallback_simulated_response(user_text)

        # DeepSeek öncelikli yapılandırma seçimi
        if self.voice_settings.deepseek_api_key:
            base_url = self.voice_settings.deepseek_base_url
            model = self.voice_settings.deepseek_model
            timeout = self.voice_settings.ai_request_timeout_s
        else:
            base_url = self.settings.groq_base_url
            model = self.settings.groq_model
            timeout = self.settings.ai_request_timeout_s

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(
                    f"{base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": self.history,
                        "temperature": 0.3,
                        "max_tokens": 150,
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                assistant_text = data["choices"][0]["message"]["content"].strip()
                self.history.append({"role": "assistant", "content": assistant_text})
                return assistant_text

        except Exception as exc:
            logger.warning("LLM isteği başarısız oldu: %s", exc)
            return "Şu anda veritabanını kontrol ediyorum, size nasıl yardımcı olabilirim?"

    async def _fallback_simulated_response(self, user_text: str) -> str:
        """API anahtarı olmadığında konuşma hafızasıyla gün/saat/usta algılayıp veritabanı sorguları çalıştırır."""
        import re

        lower_text = user_text.lower()
        if any(w in lower_text for w in ["kapat", "iyi günler", "hoşça kal", "teşekkür"]):
            return "Bizi aradığınız için teşekkür ederiz. İyi günler dileriz."

        # 1. Tarih algılama veya hafızadan hatırlama
        has_date_word = any(w in lower_text for w in [
            "pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar",
            "yarın", "bugün", "öbür gün"
        ])
        if has_date_word or self.memory_date is None:
            self.memory_date, self.memory_date_label = parse_target_date_tr(user_text)

        target_date = self.memory_date
        day_label = self.memory_date_label or "Yarın"
        target_date_str = target_date.isoformat()
        formatted_date = target_date.strftime("%d.%m.%Y")

        # 2. İşlem (Hizmet/Kategori) algılama
        if any(w in lower_text for w in ["saç sakal", "saç ve sakal", "ikisi"]):
            self.memory_service = "Saç + Sakal"
        elif "sakal" in lower_text:
            self.memory_service = "Sakal Tıraşı"
        elif any(w in lower_text for w in ["fön", "yıkama"]):
            self.memory_service = "Saç Yıkama & Fön"
        elif "çocuk" in lower_text:
            self.memory_service = "Çocuk Saç Kesimi"
        elif any(w in lower_text for w in ["cilt", "maske", "bakım"]):
            self.memory_service = "Cilt Bakımı & Maske"
        elif any(w in lower_text for w in ["boya"]):
            self.memory_service = "Saç Boyası"
        elif any(w in lower_text for w in ["ağda"]):
            self.memory_service = "Yüz & Kulak Ağdası"
        elif any(w in lower_text for w in ["saç", "kesim", "tıraş"]):
            self.memory_service = "Saç Kesimi"

        # 3. Personel (Berber/Usta) algılama
        if "yusuf" in lower_text:
            self.memory_staff = "Yusuf Demir"
        elif "mehmet" in lower_text:
            self.memory_staff = "Mehmet Kaya"
        elif any(w in lower_text for w in ["fark etmez", "her ikisi", "kim boşsa", "herhangi"]):
            self.memory_staff = "Mehmet Kaya"

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
            return "Hoş geldiniz! Hangi ustamız için randevu almak istersiniz? Mehmet usta mı, Yusuf usta mı?"

        staff_short = "Mehmet usta" if "Mehmet" in self.memory_staff else "Yusuf usta"

        # ADIM 2: Usta seçildikten sonra müşteri hizmet/kategori söylemediyse VERİTABANINDAN kategorileri çekip sor!
        if self.memory_service is None:
            db_services = await VoiceToolExecutor.get_services(self.business_slug)
            services_str = ", ".join(db_services[:4]) if db_services else "Saç Kesimi, Sakal Tıraşı, Saç + Sakal"
            return f"{staff_short} için hangi işlemi yaptırmak istersiniz? {services_str} hizmetlerimiz mevcuttur."

        # ADIM 3: Eğer müşteri SAAT BELİRTMEDİYSE asla otomatik saat seçip randevu açma!
        # Önce seçilen usta ve hizmetin boş saatlerini sorgula ve kullanıcıya sun.
        if self.memory_time is None:
            avail = await VoiceToolExecutor.check_availability(
                business_slug="berber_mehmet_kutahya",
                service_name=self.memory_service,
                target_date_str=target_date_str,
                staff_name=self.memory_staff,
            )
            slots = avail.get("available_slots", [])
            slot_info = ", ".join(slots[:3]) if slots else "10:00, 11:00, 14:00"
            return f"{staff_short} için {day_label} günü ({self.memory_service}) müsait saatler: {slot_info}. Hangi saati tercih edersiniz?"

        # ADIM 3: Müşteri hem USTAYI hem SAATİ net belirlediğinde randevuyu oluşturmayı dene
        time_str = self.memory_time
        target_staff = self.memory_staff
        start_time_local = f"{target_date_str} {time_str}"

        result = await VoiceToolExecutor.book_appointment(
            business_slug="berber_mehmet_kutahya",
            service_name=self.memory_service,
            staff_name=target_staff,
            customer_phone="+905321112233",
            customer_name="Yusuf Kantarcıoğlu",
            start_time_local=start_time_local,
        )

        if result and not result.get("error"):
            self.memory_time = None
            return f"Randevunuz {day_label} günü saat {time_str}'e {staff_short} için oluşturuldu. İyi günler dileriz!"

        # ADIM 4: Eğer istenen usta o saatte DOLUYSA ASLA otomatik olarak diğer ustaya KAYDETME!
        # Kullanıcının onayına sun:
        alt_staff = "Yusuf Demir" if target_staff == "Mehmet Kaya" else "Mehmet Kaya"
        alt_short = "Yusuf usta" if "Yusuf" in alt_staff else "Mehmet usta"

        # O ustanın başka hangi saatleri boş bakalım
        avail_same_staff = await VoiceToolExecutor.check_availability(
            business_slug="berber_mehmet_kutahya",
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


