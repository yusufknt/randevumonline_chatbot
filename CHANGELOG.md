# Changelog

Tüm önemli değişiklikler bu dosyada belgelenecektir.

## [Unreleased]

### Added (Eklenenler)
- **Production Health Check**: `/health` endpoint'i eklendi. SIP listener durumu, LLM/STT/TTS API hazır olma durumu, MongoDB ve Randevu API durumu canlı olarak kontrol edilebilir.
- **Gelişmiş Uçtan Uca (E2E) Loglama**: Gelen çağrılarda Remote IP, Remote Port, Session ID detayları eklendi. Ses paketi alma başlangıcı, LLM timeout logları, TTS stream başlangıcı ve Randevu API çağrısı sonuçları loglara dahil edildi.
- **Voice Bot Production Ready**: 
  - `AudioSocketServer` (TCP 8010), FastAPI'nin `lifespan` olaylarına dahil edildi, böylece uygulama başladığında ses botu arka planda otomatik olarak dinlemeye başlıyor.
  - Canlı çağrılar ve NetGSM testleri için `pipeline.py` ve `audio_socket.py` içine daha detaylı (barge-in, LLM ve TTS durumları) debug logları eklendi.

### Changed (Değiştirilenler)
- **Docker Compose**: `docker-compose.yml` üzerindeki komut production (canlı sunucu) ortamı için `--reload` kapatılarak optimize edildi. Geliştirme modu yoruma alındı.
- **Pipeline Yalıtımı**: Asterisk üzerinden birden fazla çağrı aynı anda gelebileceği (multi-session) ihtimaline karşı `VoicePipeline`, her yeni `ID` paketinde (yani her yeni oturumda) oturuma özel olarak örnekleniyor (instantiated). Daha önce sunucu bazlı globale atanıyordu, bu da eşzamanlı çağrılarda state çakışması yaratabilirdi.
- **Local Testler İsteğe Bağlı**: `scripts/test_voice_live_mic.py` sadece geliştirme için isteğe bağlı (opsiyonel) tutuldu, ana akış üretim odaklı hale getirildi.

### Fixed (Düzeltilenler)
- **Kritik Hata (Exception) Toleransı**: STT çözümleme (transcribe), LLM cevap üretimi (timeout dahil), TTS ses üretimi ve Randevu API (create_appointment) fonksiyonları `try-except` blokları ile korumaya alındı. 
- Beklenmeyen AudioSocket istemci kopmalarında, zorunlu reset (ConnectionResetError) durumlarında veya hatalı/bozuk paket başlıklarında (struct.error) uygulamanın çökmesi tamamen engellendi. Fallback mekanizmaları devreye alındı.
