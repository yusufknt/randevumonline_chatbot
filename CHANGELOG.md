# Changelog

Tüm önemli değişiklikler bu dosyada belgelenecektir.

## [Unreleased]

### Added (Eklenenler)
- **Production Health Check**: `/health` endpoint'i eklendi. SIP listener durumu, LLM/STT/TTS API hazır olma durumu, MongoDB ve Randevu API durumu canlı olarak kontrol edilebilir.
- **Gelişmiş Uçtan Uca (E2E) Loglama**: Gelen çağrılarda Remote IP, Remote Port, Session ID detayları eklendi. Ses paketi alma başlangıcı, LLM timeout logları, TTS stream başlangıcı ve Randevu API çağrısı sonuçları loglara dahil edildi.
- **Voice Bot Production Ready**: 
  - `AudioSocketServer` (TCP 8010), FastAPI'nin `lifespan` olaylarına dahil edildi, böylece uygulama başladığında ses botu arka planda otomatik olarak dinlemeye başlıyor.
  - Canlı çağrılar ve NetGSM testleri için `pipeline.py` ve `audio_socket.py` içine daha detaylı (barge-in, LLM ve TTS durumları) debug logları eklendi.
- **Hazır Karşılama Sesi (Zero-Delay Startup)**: Telefon açıldığında LLM/TTS bekleme süreleri (30-40 sn) tamamen ortadan kaldırıldı. Asistan çağrıyı yanıtlar yanıtlamaz, projeye eklenen hazır `.alaw` (G.711) ses dosyası ağa aktarılıyor ve sıfır gecikmeyle karşılama yapıyor.

### Changed (Değiştirilenler)
- **Telsiz Mantığı (Half-Duplex) Geçişi**: Barge-in (söz kesme) mimarisi projeden tamamen silindi. Asistan konuşurken gelen tüm müşteri ses paketleri kasıtlı olarak yoksayılıyor. Böylece arka plan gürültüsüyle asistanın cümlesinin yarıda kesilmesi problemi kökünden çözüldü. Müşteri, ancak asistan konuşmasını tamamladığında (LISTENING modu) dinleniyor.
- **Usta Bazlı Hizmet Filtreleme**: Müşteri bir usta seçtiğinde, asistan artık sadece o ustanın verebildiği hizmetleri sayıyor ve onaylıyor (Yapay zeka promptlarına ve yedek sistemlere `staff_name` filtresi eklendi).
- **Docker Compose**: `docker-compose.yml` üzerindeki komut production (canlı sunucu) ortamı için `--reload` kapatılarak optimize edildi. Geliştirme modu yoruma alındı.
- **Pipeline Yalıtımı**: Asterisk üzerinden birden fazla çağrı aynı anda gelebileceği (multi-session) ihtimaline karşı `VoicePipeline`, her yeni `ID` paketinde (yani her yeni oturumda) oturuma özel olarak örnekleniyor (instantiated). Daha önce sunucu bazlı globale atanıyordu, bu da eşzamanlı çağrılarda state çakışması yaratabilirdi.
- **Local Testler İsteğe Bağlı**: `scripts/test_voice_live_mic.py` sadece geliştirme için isteğe bağlı (opsiyonel) tutuldu, ana akış üretim odaklı hale getirildi.

### Fixed (Düzeltilenler)
- **Kritik Hata (Exception) Toleransı**: STT çözümleme (transcribe), LLM cevap üretimi (timeout dahil), TTS ses üretimi ve Randevu API (create_appointment) fonksiyonları `try-except` blokları ile korumaya alındı. 
- Beklenmeyen AudioSocket istemci kopmalarında, zorunlu reset (ConnectionResetError) durumlarında veya hatalı/bozuk paket başlıklarında (struct.error) uygulamanın çökmesi tamamen engellendi. Fallback mekanizmaları devreye alındı.
