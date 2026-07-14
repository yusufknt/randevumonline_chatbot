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

VOICE_SYSTEM_PROMPT = """Sen {business_name} sesli asistanısın. Müşterilerle telefonda en kısa, net ve anlaşılır şekilde konuşursun.
Gereksiz uzatmalardan kaçın. En fazla 1-2 kısa cümle kur. Bugünün tarihi: {today_date}.
DİKKAT (ÇOK ÖNEMLİ): Konuşmalarında ASLA markdown (yıldız, alt çizgi vb.) kullanma. Sayıları, fiyatları, tarihleri ve saatleri bir insanın telefonda söyleyeceği gibi, tamamen okunduğu gibi doğal bir konuşma diliyle yaz (örn: "15:00" yerine "öğleden sonra üç" veya "saat on beş", "250 TL" yerine "iki yüz elli lira", "15.07.2026" yerine "on beş temmuz"). Müşteriye karşı son derece doğal, gerçekçi ve akıcı bir telefon görüşmesi yapıyormuş gibi davran.

Diyalog Akışı SIKICA ŞU SIRAYLA OLMALIDIR:
1. ADIM: Personel Seçimi: Müşteriye ilk olarak hangi ustayı ({staff_list}) tercih ettiğini sor. (Müşteri usta söylemeden asla devam etme).
2. ADIM: Gün Bilgisi: Usta seçildikten sonra "Hangi gün randevu istersiniz?" diye sor.
3. ADIM: Saat Seçimi (MÜSAİTLİK SORGULAMA): Müşteri usta ve GÜN seçtiğinde, o günkü müsait saatleri öğrenmek zorundasın. Bunun için metnin sonuna GİZLİ şu kodu ekle:
[KONTROL: Usta Adı | YYYY-MM-DD]
(Örnek: "15 Temmuz için müsaitlik durumuna hemen bakıyorum... [KONTROL: Mehmet Kaya | 2026-07-15]")
Sistem sana boş saatleri gizlice verecek. Sistemden saatler geldiğinde müşteriye saatleri okurken KISALT (Örn: "9:00, 10:00, 11:00, 12:00" yerine "9'dan 12'ye kadar boş" şeklinde blok halinde söyle) ve hangi saati seçtiğini sor.
4. ADIM: Hizmet Seçimi: Müşteri saati seçtikten SONRA, "Hangi hizmeti almak istersiniz?" diye sor. (Müşteri "saç" derse, elindeki [{services_list}] listesinden saçla ilgili olanları filtreleyerek netleştir).
5. ADIM: Randevu Onayı: Müşteri her şeyi seçtiğinde işlemi onayla ve metnin sonuna ASLA OKUNMAYACAK şu gizli kodu ekle:
[RANDEVU: Usta Adı | Hizmet Adı | YYYY-MM-DD HH:MM]
DİKKAT: Randevuyu onayladıktan sonra müşteriye MUTLAKA "Başka bir isteğiniz var mı?" diye sor.
Örnek: Randevunuzu oluşturdum, başka bir isteğiniz var mı? [RANDEVU: Yusuf Demir | Saç Kesimi | 2026-07-15 14:30]

İPTAL VE REVİZE İŞLEMLERİ:
Müşterinin sistemdeki aktif randevuları şunlardır:
[{user_appointments}]
Eğer müşteri var olan bir randevusunu İPTAL ETMEK isterse:
Hangi randevuyu iptal edeceğinden emin olduktan sonra cevabının en sonuna ŞU KODU KESİNLİKLE EKLE (eklemezsen iptal olmaz!): [IPTAL: Randevu_ID]

Eğer müşteri var olan bir randevusunu REVİZE ETMEK (saatini değiştirmek) isterse:
1. Önce [KONTROL: Usta Adı | Yeni Tarih] etiketiyle yeni saatin müsaitliğine bak.
2. Müşteri boş saatlerden birini seçtiğinde, cevabının en sonuna ŞU KODU KESİNLİKLE EKLE (eklemezsen revize olmaz!): [REVIZE: Randevu_ID | YYYY-MM-DD HH:MM]
Örnek: Randevunuzu revize ettim, başka bir isteğiniz var mı? [REVIZE: 6a50ef... | 2026-07-15 14:30]
"""



def parse_target_date_tr(text: str) -> tuple[date, str]:
    """Türkçe tarih ifadelerini ('15 temmuz', '2 hafta sonra cuma', 'yarın' vb.) algılayıp gerçek takvim tarihini döndürür."""
    import re
    from datetime import date, timedelta

    today = date.today()
    lower = text.lower()

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

    # 2. Hafta İlerletme (Örn: 2 hafta sonra)
    weeks_to_add = 0
    if "haftaya" in lower or "haftada" in lower:
        weeks_to_add = 1
    
    week_match = re.search(r"(\d+|bir|iki|üç|dört|beş)\s*hafta\s*sonra", lower)
    if week_match:
        val = week_match.group(1)
        if val == "bir": weeks_to_add = 1
        elif val == "iki": weeks_to_add = 2
        elif val == "üç": weeks_to_add = 3
        elif val == "dört": weeks_to_add = 4
        elif val == "beş": weeks_to_add = 5
        elif val.isdigit(): weeks_to_add = int(val)

    weekdays = {
        "pazartesi": (0, "Pazartesi"), "salı": (1, "Salı"), "çarşamba": (2, "Çarşamba"),
        "perşembe": (3, "Perşembe"), "cuma": (4, "Cuma"), "cumartesi": (5, "Cumartesi"),
        "pazar": (6, "Pazar")
    }

    # Haftanın günü belirtilmiş mi? (Örn: 2 hafta sonra Cuma)
    for tr_name, (target_wd, display_name) in weekdays.items():
        if tr_name in lower:
            days_ahead = (target_wd - today.weekday()) % 7
            if days_ahead == 0 and weeks_to_add == 0:
                days_ahead = 7  # Önümüzdeki o gün
            target_date = today + timedelta(days=days_ahead + (weeks_to_add * 7))
            label = display_name
            if weeks_to_add > 0:
                label = f"{weeks_to_add} hafta sonra {display_name}"
            elif "haftaya" in lower:
                label = f"Haftaya {display_name}"
            return target_date, label

    if weeks_to_add > 0:
        return today + timedelta(days=weeks_to_add * 7), f"{weeks_to_add} hafta sonra"

    # 3. Göreceli ifadeler
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
        self.memory_time_pref: str | None = None

        # Süre ve Tur Limiti Koruması (Graceful Exit / Fallback)
        self.session_start_time: float = time.time()
        self.turn_count: int = 0
        self.is_session_closed: bool = False




    async def generate_response(self, user_text: str) -> str:
        """Kullanıcı metnini alır ve sesli asistandan kısa bir cevap döndürür."""
        if not user_text.strip():
            return ""

        # İlk kez çağrıldığında sistem promptuna gerçek hizmetleri dinamik olarak ekle
        if getattr(self, "_services_fetched", None) is None:
            self._services_fetched = True
            db_services = await VoiceToolExecutor.get_services(self.business_slug)
            db_staff = await VoiceToolExecutor.get_staff(self.business_slug)
            db_business = await VoiceToolExecutor.get_business_info(self.business_slug)
            # Sabit telefon no ile müşteri randevularını çek (Gerçek senaryoda çağrı numarasından alınır)
            user_apts = await VoiceToolExecutor.get_customer_appointments(self.business_slug, "+905321112233")
            
            services_str = ", ".join(db_services) if db_services else "Saç Kesimi, Sakal Tıraşı"
            staff_str = " veya ".join(db_staff) if db_staff else "Mehmet usta veya Yusuf usta"
            business_name = db_business.get("name", "RandevumOnline") if db_business else "RandevumOnline"
            
            apts_strs = [f"ID: {a['id']} | Tarih: {a['date']} | Usta: {a['staff']} | Hizmet: {a['service']}" for a in user_apts]
            user_apts_str = "\n".join(apts_strs) if apts_strs else "Müşterinin aktif randevusu bulunmuyor."
            
            from datetime import datetime
            from zoneinfo import ZoneInfo
            today_str = datetime.now(ZoneInfo("Europe/Istanbul")).strftime("%Y-%m-%d (%A)")
            
            self.history[0]["content"] = self.history[0]["content"].format(
                business_name=business_name,
                staff_list=staff_str,
                services_list=services_str,
                today_date=today_str,
                user_appointments=user_apts_str
            )

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
            aggregated_assistant_text = ""
            for _ in range(2):
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
                    
                    import re
                    
                    # 1. KONTROL ETİKETİNİ YAKALA (Müsaitlik Sorgusu)
                    kontrol_match = re.search(r"\[KONTROL:\s*([^|]+)\|\s*([^\]]+)\]", assistant_text)
                    if kontrol_match:
                        staff_name = kontrol_match.group(1).strip()
                        date_str = kontrol_match.group(2).strip()
                        
                        logger.info("🔍 LLM Müsaitlik Sorgusu Tetikledi! Usta: %s, Tarih: %s", staff_name, date_str)
                        
                        # Gizli etiketi metinden çıkar
                        clean_text = assistant_text.replace(kontrol_match.group(0), "").strip()
                        if clean_text:
                            aggregated_assistant_text += clean_text + " "
                            
                        self.history.append({"role": "assistant", "content": clean_text})
                        
                        # Veritabanından saatleri çek (check_availability parametre sırası: business, service, date, staff)
                        # Hizmet henüz belli olmadığı için service_name="Belirsiz" gönderiyoruz.
                        avail = await VoiceToolExecutor.check_availability(self.business_slug, "Belirsiz", date_str, staff_name)
                        if "error" in avail:
                            sys_msg = f"SİSTEM BİLGİSİ: Hata oluştu ({avail['error']}). Müşteriye başka bir tarih seçmesini veya usta/hizmet uyuşmazlığı olduğunu söyle."
                        else:
                            slots = ", ".join(avail["available_slots"]) if avail["available_slots"] else "Maalesef dolu"
                            sys_msg = f"SİSTEM BİLGİSİ: {staff_name} için {date_str} tarihindeki boş saatler: {slots}. Müşteriye bunları okuyarak seçmesini iste."
                            
                        self.history.append({"role": "user", "content": sys_msg})
                        continue  # 2. tura dön ve saatlerle birlikte yeni cevabı al!

                    # 2. RANDEVU GİZLİ ETİKETİNİ YAKALA VE VERİTABANINA KAYDET
                    match = re.search(r"\[RANDEVU:\s*([^|]+)\|\s*([^|]+)\|\s*([^\]]+)\]", assistant_text)
                    if match:
                        staff_name = match.group(1).strip()
                        service_name = match.group(2).strip()
                        datetime_str = match.group(3).strip()
                        
                        logger.info("📅 LLM Randevu Oluşturma Tetiklendi! Usta: %s, Hizmet: %s, Zaman: %s", staff_name, service_name, datetime_str)
                        
                        result = await VoiceToolExecutor.book_appointment(
                            business_slug=self.business_slug,
                            service_name=service_name,
                            staff_name=staff_name,
                            customer_phone="+905321112233",  # Sesli asistan arayan numarayı normalde dışarıdan alır
                            customer_name="Sesli Müşteri",
                            start_time_local=datetime_str,
                        )
                        
                        if "error" in result:
                            err = result["error"]
                            logger.error("Randevu oluşturma hatası: %s", err)
                            if err == "staff_cannot_perform_service":
                                assistant_text = f"Özür dilerim, ancak {staff_name} ustamız {service_name} işlemini yapmıyor. Lütfen diğer ustamızı veya farklı bir hizmeti tercih edebilir misiniz?"
                            elif err == "slot_taken":
                                assistant_text = f"Üzgünüm, seçtiğiniz o saat az önce dolmuş. Lütfen farklı bir saat söyler misiniz?"
                            elif err == "staff_not_found" or err == "service_not_found":
                                assistant_text = f"Maalesef hizmet veya usta eşleşmedi. Lütfen tekrar eder misiniz?"
                            else:
                                assistant_text = f"Sistemde bir hata oluştu, randevuyu kaydedemedim. Lütfen tekrar deneyin."
                        else:
                            logger.info("✅ Randevu başarıyla veritabanına işlendi (ID: %s)", result.get("appointment_id"))
                            assistant_text = assistant_text.replace(match.group(0), "").strip()

                    # 3. İPTAL GİZLİ ETİKETİNİ YAKALA VE VERİTABANINA KAYDET
                    iptal_match = re.search(r"\[IPTAL:\s*([^\]]+)\]", assistant_text)
                    if iptal_match:
                        apt_id = iptal_match.group(1).strip()
                        logger.info("🗑️ LLM Randevu İptali Tetiklendi! ID: %s", apt_id)
                        
                        success = await VoiceToolExecutor.cancel_appointment(apt_id)
                        if not success:
                            assistant_text = "Maalesef randevunuzu iptal ederken bir sorun oluştu. Lütfen tekrar deneyin."
                        else:
                            logger.info("✅ Randevu iptal edildi (ID: %s)", apt_id)
                            assistant_text = assistant_text.replace(iptal_match.group(0), "").strip()
                            
                    # 4. REVİZE GİZLİ ETİKETİNİ YAKALA VE VERİTABANINA KAYDET
                    revize_match = re.search(r"\[REVIZE:\s*([^|]+)\|\s*([^\]]+)\]", assistant_text)
                    if revize_match:
                        apt_id = revize_match.group(1).strip()
                        new_start = revize_match.group(2).strip()
                        logger.info("🔄 LLM Randevu Revizesi Tetiklendi! ID: %s, Yeni Zaman: %s", apt_id, new_start)
                        
                        result = await VoiceToolExecutor.reschedule_appointment(self.business_slug, apt_id, new_start)
                        if "error" in result:
                            err = result["error"]
                            logger.error("Randevu revize hatası: %s", err)
                            if err == "slot_taken":
                                assistant_text = "Üzgünüm, seçtiğiniz o saat az önce dolmuş. Lütfen farklı bir saat söyler misiniz?"
                            else:
                                assistant_text = "Sistemde bir hata oluştu, randevunuzu değiştiremedim. Lütfen tekrar deneyin."
                        else:
                            logger.info("✅ Randevu başarıyla revize edildi (ID: %s)", apt_id)
                            assistant_text = assistant_text.replace(revize_match.group(0), "").strip()
                    
                    self.history.append({"role": "assistant", "content": assistant_text})
                    return (aggregated_assistant_text + assistant_text).strip()

        except Exception as exc:
            logger.warning("LLM isteği başarısız oldu: %s", exc)
            return await self._fallback_simulated_response(user_text)

    async def _fallback_simulated_response(self, user_text: str) -> str:
        """API anahtarı olmadığında konuşma hafızasıyla gün/saat/usta algılayıp veritabanı sorguları çalıştırır."""
        import re

        lower_text = user_text.lower()
        if any(w in lower_text for w in ["kapat", "iyi günler", "hoşça kal", "teşekkür"]):
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
            staff_str = " mı, ".join([s.split()[0] + " usta" for s in db_staff]) if db_staff else "Mehmet usta mı, Yusuf usta"
            return f"Hoş geldiniz! Hangi ustamız için randevu almak istersiniz? {staff_str} mı?"

        staff_short = f"{self.memory_staff.split()[0]} usta" if self.memory_staff else "Usta"

        # ADIM 2: Usta seçildikten sonra müşteri hizmet/kategori söylemediyse VERİTABANINDAN kategorileri çekip sor!
        if self.memory_service is None:
            db_services = await VoiceToolExecutor.get_services(self.business_slug)
            
            # Eğer müşteri genel bir ifade kullanmışsa filtrele
            filtered_services = []
            if "saç" in lower_text:
                filtered_services = [s for s in db_services if "saç" in s.lower()]
            elif "sakal" in lower_text:
                filtered_services = [s for s in db_services if "sakal" in s.lower()]
            elif "bakım" in lower_text or "cilt" in lower_text or "maske" in lower_text:
                filtered_services = [s for s in db_services if any(w in s.lower() for w in ["bakım", "maske", "cilt"])]
            
            if filtered_services:
                services_str = ", ".join(filtered_services)
                return f"{staff_short} için {services_str} hizmetlerimiz var. Hangisini tercih edersiniz?"
            else:
                services_str = ", ".join(db_services[:4]) if db_services else "Saç Kesimi, Sakal Tıraşı, Saç + Sakal"
                return f"{staff_short} için hangi işlemi yaptırmak istersiniz? {services_str} vb. hizmetlerimiz mevcuttur."

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

            slot_info = ", ".join(slots[:4])
            return f"{staff_short} için {day_label} günü müsait saatler: {slot_info}. Hangi saati tercih edersiniz?"

        # ADIM 4: Müşteri hem USTAYI hem SAATİ net belirlediğinde randevuyu oluşturmayı dene
        time_str = self.memory_time
        target_staff = self.memory_staff
        start_time_local = f"{target_date_str} {time_str}"

        result = await VoiceToolExecutor.book_appointment(
            business_slug=self.business_slug,
            service_name=self.memory_service,
            staff_name=target_staff,
            customer_phone="+905321112233",
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
