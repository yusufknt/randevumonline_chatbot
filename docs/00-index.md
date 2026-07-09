# 00. RandevumOnline Chatbot — Dökümantasyon Haritası

Bu klasör projenin tüm operasyonel dökümanlarını içerir. Dosyalar
**numaralı**, **bir konseptin bir tek yerde** anlatıldığı, gerektikçe
diğer dökümanlara ve Meta'nın resmi dokümantasyonuna referans veren bir
yapıdadır.

## Akış sırası

| # | Dosya | Kim için |
|---|-------|---|
| 01 | [Yerel kurulum](./01-yerel-kurulum.md) | Repoyu ilk kez kuran herkes |
| 02 | [Meta App temelleri](./02-meta-app.md) | Webhook + token kavramları |
| 03 | [WhatsApp Cloud — self-test](./03-whatsapp-cloud-test.md) | Test number ile mesajlaşma |
| 04 | [WhatsApp Flow — randevu](./04-whatsapp-flow.md) | 6-ekran randevu sihirbazı |
| 05 | [Instagram — self-test](./05-instagram-test.md) | IG Business + Quick Replies / Button Template (hizmetler + randevu + bilgi) / Persistent Menu / Ice Breakers — AI yok |
| 06 | [Tech Provider onboarding](./06-tech-provider-onboarding.md) | Çoklu firma + Embedded Signup |
| 07 | [Hata kılavuzu](./07-hata-kilavuzu.md) | Tüm hatalar tek tabloda |
| 08 | [App Review submission](./08-app-review-submission.md) | Meta App Review başvuru formu — adım adım |
| 09 | [Sıfırdan kurulum — sıralı yürüyüş](./09-kurulum-yuruyusu.md) | 01-06'yı tek happy-path'e döken pratik checklist (komutlar sırayla + sihirbazda ne cevaplanmalı) |

> **İlk kez kuruyorsanız:** sıralı pratik yürüyüş için [09](./09-kurulum-yuruyusu.md)'u takip edin; her adım kavram/edge-case için 01-08'e referans verir. Tek konuyu derinlemesine okumak için doğrudan ilgili numaralı dökümana gidin. Instagram opsiyonel (05); Tech Provider modeli (06) yalnız üretim için.

## Diğer dökümanlar

| Dosya | İçerik |
|---|---|
| [`randevumonline-sistem.md`](./randevumonline-sistem.md) | Ürün spec'i — randevu akışı, hizmet kataloğu, işletme ayarları (kanal-bağımsız) |
| [`randevumonline-site.md`](./randevumonline-site.md) | Web/PWA tarafı (Flow değil) |
| [`Netgsm.md`](./Netgsm.md) | SMS sağlayıcı entegrasyon notu |
| [`VOICE_BOT_ROADMAP.md`](./VOICE_BOT_ROADMAP.md) | Telefon bot yol haritası (Asterisk + STT/TTS + Netgsm SIP Trunk) |
| [`Developers Facebook Documentation/`](./Developers%20Facebook%20Documentation/) | Meta'nın resmi dökümantasyonunun yerel kopyası (referans) |

## Endpoint haritası

Backend `app/webhooks.py`'de tanımlı tüm uçlar. Meta Dashboard'daki webhook konfigürasyonu için **tam URL** = `<PUBLIC_BASE_URL><PATH>` (örn. `https://abc.ngrok-free.app/webhooks/whatsapp`).

| Yöntem | Path | Kim çağırır | Amaç | Doc |
|---|---|---|---|---|
| `GET` | `/healthz` | Operatör | Liveness probe | — |
| `GET` | `/webhooks/whatsapp` | Meta (subscription verify) | `hub.challenge` echo | [§3.3](./03-whatsapp-cloud-test.md#33-webhook-subscribe) |
| `POST` | `/webhooks/whatsapp` | Meta (gelen mesaj) | inbound message + status | [§3.3](./03-whatsapp-cloud-test.md#33-webhook-subscribe) |
| `POST` | `/webhooks/whatsapp/flow` | WhatsApp client (Flow) | şifreli data exchange | [§4.4](./04-whatsapp-flow.md#44-mimari) |
| `GET` | `/webhooks/instagram` | Meta (subscription verify) | `hub.challenge` echo | [§5.2](./05-instagram-test.md#52-webhook-subscribe) |
| `POST` | `/webhooks/instagram` | Meta (gelen mesaj) | inbound DM | [§5.2](./05-instagram-test.md#52-webhook-subscribe) |

> **Meta UI'da nereye gider:**
> - WA webhook callback: `<PUBLIC_BASE_URL>/webhooks/whatsapp`
> - IG webhook callback: `<PUBLIC_BASE_URL>/webhooks/instagram`
> - Flow endpoint URI (otomatik — `create-flow`/`onboard` Meta'ya yazar): `<PUBLIC_BASE_URL>/webhooks/whatsapp/flow`

## Notasyon

- `§X.Y` — bu klasördeki bir dökümanın bölüm numarası.
- `Meta: <path>` — `docs/Developers Facebook Documentation/output/...` altındaki resmi dökümana referans.
- `app/...`, `db/...` — kod yolu.

## Versiyon

- Flow JSON sürümü: **7.3** (`app/channels/whatsapp/flow_manifest.py`)
- Data API sürümü: **4.0** — Meta payload'a `flow_token_signature` (HS256 JWT) ekler; backend henüz doğrulamıyor (X-Hub-Signature-256 zaten cover ediyor)
- WA Graph API sürümü: `v25.0` | IG Graph API sürümü: `v25.0` (config: `app/core/config.py` — `wa_graph_base_url` / `ig_graph_base_url`)
