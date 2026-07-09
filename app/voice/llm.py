"""
FAZ 3 - Sesli Asistan (Voice Agent) LLM ve Diyalog Yöneticisi.

Bu modül, telefon konuşmalarına özel kısa, insani ve doğal Türkçe yanıtlar
üretmek üzere Groq / Ollama entegrasyonu sağlar.
"""

from __future__ import annotations

import logging
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


class VoiceLLMEngine:
    """Sesli aramalar için LLM diyalog yöneticisi."""

    def __init__(self, business_slug: str = "berber_mehmet_kutahya") -> None:
        self.business_slug = business_slug
        self.settings = get_settings()
        self.history: list[dict[str, Any]] = [
            {"role": "system", "content": VOICE_SYSTEM_PROMPT}
        ]

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
        """API anahtarı olmadığında veritabanı sorguları yaparak gerçekçi akış sunar."""
        import re
        from datetime import date, timedelta

        lower_text = user_text.lower()
        if any(w in lower_text for w in ["kapat", "iyi günler", "hoşça kal", "teşekkür"]):
            return "Bizi aradığınız için teşekkür ederiz. İyi günler dileriz."

        time_match = re.search(r"(\d{1,2}[:.]\d{2})", user_text)
        is_booking_intent = any(w in lower_text for w in ["evet", "onay", "tamam", "olur", "al"])

        if time_match or is_booking_intent:
            time_str = time_match.group(1).replace(".", ":") if time_match else "14:00"
            if len(time_str) == 4:
                time_str = "0" + time_str

            tomorrow_str = (date.today() + timedelta(days=1)).strftime(f"%Y-%m-%d {time_str}")
            result = await VoiceToolExecutor.book_appointment(
                business_slug="berber_mehmet_kutahya",
                service_name="Saç Kesimi",
                staff_name="Mehmet Kaya",
                customer_phone="+905321112233",
                customer_name="Yusuf Kantarcıoğlu",
                start_time_local=tomorrow_str,
            )
            if result and not result.get("error"):
                return f"Harika! Randevunuz yarın saat {time_str} için Yusuf Kantarcıoğlu adına veritabanımıza başarıyla kaydedildi. İyi günler dileriz!"
            return f"Maalesef seçtiğiniz {time_str} saati için veritabanımızda zaten bir randevu bulunuyor ve dolu! Lütfen başka bir saat tercih edin."

        elif any(w in lower_text for w in ["randevu", "saat", "yarın", "boş", "var mı", "kesim"]):
            tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
            avail = await VoiceToolExecutor.check_availability(
                business_slug="berber_mehmet_kutahya",
                service_name="Saç Kesimi",
                target_date_str=tomorrow_str,
            )
            slots = avail.get("available_slots", [])
            slot_info = ", ".join(slots[:3]) if slots else "14:00"
            return f"Harika, yarın için {slot_info} saatlerimiz müsait. Hangi saat için randevu almak istersiniz?"

        else:
            return "Randevum Online'a hoş geldiniz, yarın için saç kesimi randevusu almak ister misiniz?"
