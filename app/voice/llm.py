"""
FAZ 3 - Sesli Asistan (Voice Agent) LLM ve Diyalog Yöneticisi.

Bu modül, telefon konuşmalarına özel kısa, insani ve doğal Türkçe yanıtlar
üretmek üzere Groq / Ollama entegrasyonu sağlar.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

import httpx

from app.core.config import get_settings
from app.voice.tools import VoiceToolExecutor

logger = logging.getLogger(__name__)

VOICE_SYSTEM_PROMPT = """Sen RandevumOnline sesli asistanısın.
Müşterilerle telefonda konuşuyorsun.
Kurallar:
1. Kısa, doğal ve en fazla 1-2 cümlelik Türkçe cevaplar ver.
2. Müşteri randevu istediğinde önce tarihi ve hizmeti öğrenip müsait saatleri kontrol et.
3. Onay aldığında randevuyu kaydet.
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
        self.history: list[dict[str, Any]] = [
            {"role": "system", "content": VOICE_SYSTEM_PROMPT}
        ]
        # Oturum hafızası (Konuşma boyunca hatırlanacak bilgiler)
        self.memory_date: date | None = None
        self.memory_date_label: str | None = None
        self.memory_time: str | None = None
        self.memory_service: str = "Saç Kesimi"
        self.memory_staff: str | None = None

    async def generate_response(self, user_text: str) -> str:
        """Kullanıcı metnini alır ve sesli asistandan kısa bir cevap döndürür."""
        if not user_text.strip():
            return ""

        self.history.append({"role": "user", "content": user_text})

        # Eğer API anahtarı yoksa test ve simülasyon ortamı için akıllı yedek yanıtlar ver
        if not self.settings.groq_api_key:
            return await self._fallback_simulated_response(user_text)

        try:
            async with httpx.AsyncClient(timeout=self.settings.ai_request_timeout_s) as client:
                resp = await client.post(
                    f"{self.settings.groq_base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.settings.groq_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.settings.groq_model,
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

        # 2. İşlem (Hizmet) algılama
        if any(w in lower_text for w in ["saç sakal", "saç ve sakal", "ikisi"]):
            self.memory_service = "Saç + Sakal"
        elif "sakal" in lower_text:
            self.memory_service = "Sakal Tıraşı"
        elif any(w in lower_text for w in ["fön", "yıkama"]):
            self.memory_service = "Saç Yıkama & Fön"
        elif "çocuk" in lower_text:
            self.memory_service = "Çocuk Saç Kesimi"

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

        is_booking_intent = any(w in lower_text for w in ["evet", "onay", "tamam", "olur", "al", "istiyorum", "oluştur"])

        # Eğer saat hafızada varsa VEYA saat söylendiyse VEYA usta adı verilip saat zaten biliniyorsa
        if self.memory_time or time_match or (is_booking_intent and any(c.isdigit() for c in user_text)):
            time_str = self.memory_time or "14:00"

            # Eğer müşteri personel belirtmediyse soralım!
            if self.memory_staff is None and not any(w in lower_text for w in ["evet", "onay", "tamam"]):
                return f"{day_label} günü ({formatted_date}) saat {time_str} için {self.memory_service} randevusu almak istiyorsunuz. Mehmet usta için mi yoksa Yusuf usta için mi alalım?"

            target_staff = self.memory_staff or "Mehmet Kaya"
            start_time_local = f"{target_date_str} {time_str}"

            result = await VoiceToolExecutor.book_appointment(
                business_slug="berber_mehmet_kutahya",
                service_name=self.memory_service,
                staff_name=target_staff,
                customer_phone="+905321112233",
                customer_name="Yusuf Kantarcıoğlu",
                start_time_local=start_time_local,
            )
            # Randevu alındıktan sonra saati sıfırla ki yeni işlem yapabilsin
            self.memory_time = None

            if result and not result.get("error"):
                return f"Harika! Randevunuz {day_label} günü ({formatted_date}) saat {time_str} için {target_staff} ustaya ({self.memory_service}) başarıyla kaydedildi. İyi günler dileriz!"

            # Eğer istenen personel doluysa diğer personeli (Mehmet / Yusuf) kontrol et ve randevu ver!
            alt_staff = "Yusuf Demir" if target_staff == "Mehmet Kaya" else "Mehmet Kaya"
            alt_result = await VoiceToolExecutor.book_appointment(
                business_slug="berber_mehmet_kutahya",
                service_name=self.memory_service,
                staff_name=alt_staff,
                customer_phone="+905321112233",
                customer_name="Yusuf Kantarcıoğlu",
                start_time_local=start_time_local,
            )
            if alt_result and not alt_result.get("error"):
                return f"Maalesef {day_label} günü saat {time_str}'de {target_staff} usta dolu! Ancak {alt_staff} usta müsait olduğu için randevunuzu {alt_staff} ustaya ({self.memory_service}) kaydettim. İyi günler dileriz!"

            return f"Maalesef {day_label} günü ({formatted_date}) saat {time_str} için hem Mehmet hem de Yusuf usta dolu! Lütfen farklı bir saat tercih edin."

        elif any(w in lower_text for w in ["randevu", "saat", "boş", "var mı", "kesim", "pazar", "cuma", "cumartesi", "yarın", "bugün"]):
            avail = await VoiceToolExecutor.check_availability(
                business_slug="berber_mehmet_kutahya",
                service_name=self.memory_service,
                target_date_str=target_date_str,
            )
            slots = avail.get("available_slots", [])
            slot_info = ", ".join(slots[:3]) if slots else "14:00, 15:00, 16:00"
            return f"Harika, {day_label} günü ({formatted_date}) için {slot_info} saatlerimiz müsait. Hangi saat ve hangi ustamız (Mehmet veya Yusuf) için randevu almak istersiniz?"

        else:
            return "Randevum Online'a hoş geldiniz, hangi gün, saat ve ustamız (Mehmet veya Yusuf) için saç kesimi randevusu almak ister misiniz?"
