# Randevum Online — Sesli Yapay Zeka Asistanı (Voice Bot) Geliştirme Kılavuzu & Walkthrough

Bu doküman, Randevum Online projesine eklenen **Gerçek Zamanlı Sesli Yapay Zeka Asistanı (Voice AI Agent)** altyapısının mimarisini, oluşturulan çekirdek modülleri, canlı telefon görüşmesi simülasyonunu ve veritabanı entegrasyonu doğrulama adımlarını detaylandırır.

---

## 1. Mimari Özet & Başarılanlar

Sıfırdan kurulan Sesli Asistan altyapımız, telefon üzerinden arayan müşterilerle kesintisiz, çok turlu bir diyalog kurabilen ve doğrudan gerçek **MongoDB** veritabanı ile etkileşime geçebilen uçtan uca bir mimaridir.

```
[Müşteri / Canlı Mikrofon] 
       ↕ (Ses Akışı / PCM)
[Asterisk TCP AudioSocket / Canlı Test Betiği]
       ↕
[STT Motoru (SpeechRecognition / Whisper)]
       ↕ (Metin)
[VoiceLLMEngine (Dinamik Saat Ayrıştırma & Konuşma Geçmişi)]
       ↕ (Tool Calls: check_availability & book_appointment)
[Gerçek MongoDB Veritabanı (customers, conversations, appointments)]
       ↕ (Yanıt Metni)
[TTS Motoru & Canlı Hoparlör Çıktısı]
```

---

## 2. Oluşturulan Çekirdek Modüller (`app/voice/`)

Tüm sesli asistan mimarisi clean code prensiplerine uygun şekilde **`app/voice/`** dizini altında yapılandırılmıştır:

| Modül | Sorumluluk | Öne Çıkan Özellikler |
| :--- | :--- | :--- |
| **`config.py`** | Sesli asistan yapılandırması | Çevresel değişkenler (`.env`), Asterisk IP/Port ayarları ve zaman aşımı limitleri. |
| **`models.py`** | Pydantic veri modelleri | AudioSocket çerçeveleri, STT/TTS akış tipleri ve araç çağrı şemaları. |
| **`audio_socket.py`** | Asterisk TCP AudioSocket Sunucusu | 8kHz 16-bit PCM çift yönlü ses akışı ve UUID oturum yönetimi. |
| **`stt.py`** | Sesi Yazıya Çevirme (STT) | Konuşma bitişi algılama (VAD) ve Türkçe transkripsiyon motoru. |
| **`llm.py`** | Yapay Zeka Konuşma Motoru | Çok turlu diyalog geçmişi (`history`), dinamik saat yakalayıcı (`regex`) ve veritabanı çakışma engelleyici. |
| **`tools.py`** | Veritabanı Araç Katmanı | `check_availability` ve `book_appointment` ile doğrudan gerçek MongoDB bağlamı. |
| **`tts.py`** | Metinden Sese Dönüştürme (TTS) | Türkçe ses sentezleyici katmanı. |
| **`pipeline.py`** | Uçtan Uca Boru Hattı | STT $\rightarrow$ LLM $\rightarrow$ TTS senkronizasyonu ve çift yönlü akış yönetimi. |

---

## 3. Canlı Görüşme ve Veritabanı Entegrasyonu

### 3.1 Kesintisiz Telefon Görüşmesi Akışı (`scripts/test_voice_live_mic.py`)
Müşteriyle tek soruluk bir soru-cevap yerine, görüşme tamamlanana kadar çalışan bir **sonsuz döngü (`while True:`)** kurulmuştur:
1. **Mikrofon Kaydı:** 5 saniye boyunca müşterinin konuşmasını dinler ve metne dönüştürür.
2. **Yapay Zeka Mantığı:** LLM konuşma geçmişine bakarak müşterinin randevu isteyip istemediğini, saat belirtip belirtmediğini veya onay verip vermediğini analiz eder.
3. **Canlı Seslendirme:** Asistan yanıtını macOS hoparlöründen doğal Türkçe ses olarak okur ve hemen ardından bir sonraki tur için mikrofonu otomatik açar.
4. **Görüşme Sonu:** Müşteri *"kapat"*, *"iyi günler"* veya *"teşekkürler"* dediğinde vedalaşarak görüşmeyi sonlandırır.

### 3.2 MongoDB Müşteri ve Görüşme (`_id`) Eşleştirmesi
Randevu oluşturulurken (`create_appointment` çağrısında):
- Müşterinin telefon numarası veritabanındaki **`customers`** koleksiyonunda aranır. Kayıt yoksa otomatik olarak yeni müşteri oluşturulur ve `_id` referansı randevuya bağlanır.
- Görüşmenin yapıldığı kanal için **`conversations`** koleksiyonundan `voice` oturum kimliği alınır.

### 3.3 Çakışma Engelleyici (Conflict Prevention)
Müşteri daha önce alınmış veya dolu bir saat için randevu talep ettiğinde:
- Motor `slot_already_booked` / `conflict` hatasını yakalar.
- Asistan müşteriye net bir geri bildirim verir:
  > *"Maalesef seçtiğiniz 14:00 saati için veritabanımızda zaten bir randevu bulunuyor ve dolu! Lütfen başka bir saat tercih edin."*

---

## 4. Test ve İzleme Araçları

### 4.1 Canlı Sesli Görüşme Testi
Terminal üzerinden canlı mikrofon ve hoparlörle test başlatmak için:
```bash
python3 -m scripts.test_voice_live_mic
```

### 4.2 Veritabanı Özet Görüntüleyici (`scripts/show_db.py`)
Docker konteyneri içerisindeki işletmeleri, müşterileri ve alınan randevuları tek komutla tablo halinde listelemek için:
```bash
docker exec randevum_api python -m scripts.show_db
```

**Örnek Çıktı:**
```text
=================================================================
                MONGODB VERİTABANI ÖZETİ
=================================================================

🏢 İŞLETMELER (3 kayıt):
   • Berber Mehmet             | Kimlik (Slug): berber_mehmet_kutahya

👥 MÜŞTERİLER (3 kayıt):
   • Yusuf Kantarcıoğlu        | Telefon: +905321112233

📅 KAYITLI RANDEVULAR:
   KAYNAK     | TARİH & SAAT (UTC)   | DURUM      | TUTAR
   ----------------------------------------------------------
   VOICE      | 2026-07-10 11:00     | confirmed  | 250 TL
   VOICE      | 2026-07-10 13:00     | confirmed  | 250 TL
   WHATSAPP   | 2026-07-11 14:00     | confirmed  | 380 TL
```

---

## 5. Doğrulama ve Sonuçlar

- ✅ **Gerçek Zamanlı Kayıt:** Sesli bot üzerinden alınan randevular MongoDB `appointments` tablosuna `source: "voice"` ve `status: "confirmed"` olarak başarıyla işlenmektedir.
- ✅ **Clean Repository:** Geçici ses dosyaları temizlenmiş ve `.gitignore` dosyasına `*.wav` eklenerek projenin temizliği garanti altına alınmıştır.

### Hızlı Komut Referansı
```bash
python3 -m scripts.test_voice_live_mic
docker exec randevum_api python -m scripts.show_db
```