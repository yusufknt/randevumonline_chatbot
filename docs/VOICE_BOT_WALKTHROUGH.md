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
| **`tts.py`** | Metinden Sese Dönüştürme (TTS) | Ses API'si, Edge Neural TTS ve Piper TTS fallback desteği ile Türkçe doğal ses. |
| **`pipeline.py`** | Uçtan Uca Boru Hattı | STT $\rightarrow$ LLM $\rightarrow$ TTS senkronizasyonu ve Half-Duplex akış yönetimi. |
| **`rtp_server.py`** | UDP RTP Sunucusu | Asenkron SIP sinyalleşmesi, VAD enerji hesabı ve Zero-Delay hazır ses oynatıcısı. |

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

### 3.4 Çok Personelli (Berber Mehmet & Yusuf Usta) Akıllı Randevu Yönetimi
Sesli asistan sadece tek bir ustayı değil, işletmedeki farklı personelleri ayırt edebilecek yeteneğe kavuşturulmuştur:
- **Personel Algılama:** Konuşma sırasında müşterinin Mehmet Kaya veya Yusuf Demir ustayı tercih edip etmediği algılanır.
- **Aktif Yönlendirme:** Müşteri sadece gün ve saat belirtip usta seçmediyse asistan proaktif olarak sorar:
  > *"Pazar günü (12.07.2026) saat 09:00 için Saç Kesimi randevusu almak istiyorsunuz. Mehmet usta için mi yoksa Yusuf usta için mi alalım?"*
- **Otomatik Alternatif Önerisi / Yedekleme:** Tercih edilen ustanın o saatte dolu olması durumunda, sistem diğer ustanın müsaitliğini kontrol eder ve müşteriyi mağdur etmeden randevuyu uygun ustaya kaydeder.

---

## 4. İleri Düzey İletişim Özellikleri

### 4.1 Zero-Delay Startup (Sıfır Gecikmeli Karşılama)
Gelen aramaların ilk saniyelerinde yaşanabilecek sessizlik (dead-air) problemini ortadan kaldırmak için, önceden sentezlenmiş statik bir ses dosyası (`app/voice/assets/greeting.alaw`) kullanılır. 
- Telefon açılır açılmaz LLM veya TTS süreçleri beklenmeden doğrudan RTP üzerinden bu ses oynatılır.
- Oynatma sırasında arka planda asistan modülleri hazırlanır.
- Eğer ses dosyası bulunamazsa, sistem dinamik olarak LLM->TTS (On-the-fly) karşılama modeline kusursuz bir şekilde geri döner (Fallback).

### 4.2 Half-Duplex (Telsiz) Konuşma Modu
Asistan konuşurken müşterinin ortamındaki gürültüler (Barge-in / Söz Kesme) nedeniyle asistanın cümlesini yarıda kesmesi engellenmiştir.
- Asistan `SPEAKING` durumundayken gelen müşteri ses paketleri kasıtlı olarak yoksayılır.
- Asistan konuşmasını tamamladığı an `LISTENING` moduna geçer ve mikrofon tam kapasiteyle açılır.
- Bu sayede kesintili diyalogların ve hatalı algılamaların önüne geçilmiş, tıpkı bir insanla telsiz görüşmesi yapılıyormuş gibi stabil bir akış elde edilmiştir.

---

## 5. Test ve İzleme Araçları

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

📅 KAYITLI DETAYLI RANDEVULAR (12 kayıt):
   TARİH & SAAT (TR)   | MÜŞTERİ ADI            | USTA (PERSONEL)    | HİZMET             | DURUM      | TUTAR
   ---------------------------------------------------------------------------------------------------------
   12.07.2026 - 09:00  | Yusuf Kantarcıoğlu     | Mehmet Kaya        | Saç Kesimi         | confirmed  | 250 TL
   12.07.2026 - 15:00  | Yusuf Kantarcıoğlu     | Mehmet Kaya        | Saç Kesimi         | confirmed  | 250 TL
   12.07.2026 - 15:00  | Yusuf Kantarcıoğlu     | Yusuf Demir        | Saç Kesimi         | confirmed  | 250 TL
```

---

## 5. Doğrulama ve Sonuçlar

- ✅ **Gerçek Zamanlı Kayıt & Çoklu Personel Desteği:** Sesli bot üzerinden alınan randevular seçilen ustaya (Mehmet Kaya / Yusuf Demir) göre MongoDB `appointments` tablosuna `source: "voice"` ve `status: "confirmed"` olarak işlenmektedir.
- ✅ **Detaylı Raporlama:** `show_db.py` betiği randevuları Türkiye saati (+3), müşteri adı, usta adı ve hizmet bilgileriyle birlikte detaylı tablo olarak sunmaktadır.
- ✅ **Statik Tip Güvenliği (`0 errors, 0 warnings`):** Ses modülü (`app/voice/`) ve çekirdek yapay zeka katmanındaki tüm eksik tip anotasyonları (`Any`) ile olası null erişim riski taşıyan noktalar giderilmiştir.
- ✅ **Clean Repository:** Geçici ses dosyaları temizlenmiş ve `.gitignore` dosyasına `*.wav` eklenerek projenin temizliği garanti altına alınmıştır.

### Hızlı Komut Referansı
```bash
python3 -m scripts.test_voice_live_mic
docker exec randevum_api python -m scripts.show_db
#.venv/bin/python3 -m scripts.show_db

```