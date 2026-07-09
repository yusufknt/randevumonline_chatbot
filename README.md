# RandevumOnline Chatbot

WhatsApp (ve opsiyonel Instagram) DM üzerinden gelen mesajları karşılayıp
MongoDB'de randevu oluşturan, çok-kiracılı (multi-tenant) Python servisi.

- **WhatsApp:** [WhatsApp Flows](docs/04-whatsapp-flow.md) tabanlı 6-ekran randevu sihirbazı. AI yok — gelen mesaj CTA'lı Flow mesajını tetikler, müşteri formu doldurur, endpoint randevuyu yaratır.
- **Instagram:** Postback-driven menü (Quick Replies ana menü + hizmetler için metin listesi + Button Template) + opsiyonel **AI Müşteri Temsilcisi**. Serbest text deterministik regex ile dispatch edilir; randevu **web sitesinde** tamamlanır (`booking_url`). Persistent Menu + Ice Breakers Meta profile yazılır.
- **Instagram AI (opsiyonel):** Ana menüdeki **"Müşteri Temsilcisi"** butonu (`AI_ENABLED=true` + `GROQ_API_KEY` ile) Groq tabanlı bir sohbeti açar. AI yalnız işletmenin DB bilgilerine (hizmet/fiyat, çalışma saati, adres/konum, personel, uygun randevu saatleri) göre yanıtlar; randevu için `booking_url`'e yönlendirir, çözemediğinde gerçek personele (telefon) aktarır. Kapalıyken buton eski davranışına (telefon) düşer. IG kurulumu: [`docs/05-instagram-test.md`](docs/05-instagram-test.md).

## Kurulum

```bash
git clone <repo-url> randevumonline-chatbot && cd randevumonline-chatbot
```

**Önkoşullar:** Python 3.12+, MongoDB 8, ngrok. (Opsiyonel: Groq API key — IG AI müşteri temsilcisi.)

Kurulum komutları tek bir kanonik yerde — burada tekrarlanmaz:

- **Yerel kurulum (referans):** [`docs/01-yerel-kurulum.md`](docs/01-yerel-kurulum.md) — venv, MongoDB, ngrok, `.env` sihirbazı, seed, servisleri başlatma.
- **Sıralı yürüyüş (happy-path):** [`docs/09-kurulum-yuruyusu.md`](docs/09-kurulum-yuruyusu.md) — ne, hangi sırayla, hangi komut; sihirbazda ne cevaplanmalı.
- **Tüm dökümanların haritası:** [`docs/00-index.md`](docs/00-index.md) — Meta App, WhatsApp Cloud / Flow, Instagram, Tech Provider, hata kılavuzu.

## Dizin yapısı

```
.
├── app/                          FastAPI uygulaması
│   ├── main.py                   ASGI entry; static mount; lifespan
│   ├── webhooks.py               WA + IG webhook + Flow endpoint route'ları
│   ├── core/                     kanal-bağımsız çekirdek
│   │   ├── config.py             pydantic-settings (.env)
│   │   ├── db.py                 motor + DAO + secret resolver + indeks
│   │   ├── orchestrator.py       mesaj → WA Flow CTA / IG dispatch / IG AI → cevap
│   │   ├── ai.py                 Groq (OpenAI-uyumlu) tool-use döngüsü — IG müşteri temsilcisi
│   │   ├── tools.py              AI tool seti + DB implementasyonları (business_id izole)
│   │   ├── booking.py            create_appointment + slot kontrol + format_price
│   │   ├── availability.py       slot hesabı (saatler, izinler, çakışma, oda)
│   │   └── format.py             kanal/araç çıktısı için ortak metin biçimlendirme (saf fonksiyonlar)
│   ├── voice/                    Sesli Randevu Asistanı (Voice Agent)
│   │   ├── audio_socket.py       Asterisk TCP AudioSocket asenkron sunucusu (8010 portu)
│   │   ├── stt.py                faster-whisper ile konuşmayı metne dökme (STT) + VAD
│   │   ├── llm.py                Groq / Ollama kısa-öz Türkçe sesli asistan beyni
│   │   ├── tools.py              MongoDB randevu kontrolü & booking entegrasyonu
│   │   ├── tts.py                Piper TTS ile metni 8kHz PCM sese dönüştürme
│   │   └── pipeline.py           STT -> LLM -> TTS akış ve söz kesme (barge-in) yöneticisi
│   └── channels/
│       ├── whatsapp/
│       │   ├── client.py         parse, signature, send_text
│       │   ├── flow_sender.py    CTA mesajı gönder + flow_token üret/parse
│       │   ├── flow.py           şifreli endpoint handler + ekran builder'ları
│       │   ├── flow_manifest.py  6-ekran Flow JSON manifesti
│       │   └── flow_crypto.py    RSA-OAEP + AES-128-GCM
│       └── instagram/
│           ├── client.py         parse, signature, text/quick_replies/button_template/generic_template
│           └── flow.py           regex/postback dispatcher + "Müşteri Temsilcisi" (AI) giriş noktası
├── db/
│   ├── models.py                 Pydantic v2 koleksiyon modelleri
│   ├── seed.py                   3 örnek işletme + indeks
│   └── README.md                 şema kararları, indeks listesi
├── scripts/                      tek giriş: `python -m scripts <komut>`
│   ├── __main__.py               CLI dispatcher
│   ├── setup_env.py              .env sihirbazı
│   ├── wa_ops.py                 WA Flow kurulum: RSA keys + Meta API + MongoDB
│   ├── ig_menu.py                IG Persistent Menu + Ice Breakers
│   ├── ig_token.py               IG 60-gün long-lived token yenileme
│   ├── local_flow_test.py        6-ekran Flow endpoint lokal simülasyonu
│   └── gen_test_token.py         Flow Builder Preview için flow_token üret
├── docs/                         00-08 numaralı kurulum + ürün dökümanları
├── secrets/                      RSA private/public PEM (gitignore)
├── .env.example                  şablon — setup_env.py burayı baz alır
└── requirements.txt
```

## Script'ler

Tüm yardımcı script'ler tek giriş üzerinden: `python -m scripts <komut>`. Tam yardım: `python -m scripts -h`.

| Komut | İş |
|---|---|
| `python -m scripts setup` | `.env` interaktif sihirbazı (link verir, otomatik üretir) |
| `python -m scripts setup --show` | Mevcut `.env` özet tablosu |
| `python -m scripts setup --section <ad>` | Tek bölüm: `mongo`, `verify`, `app_secret`, `flow_keys`, `ai`, `tenants`, `fastapi` |
| `python -m scripts gen-keys [--force]` | `secrets/flow_{private,public}.pem` üret |
| `python -m scripts upload-key` | Public key'i Meta'ya yükle (env veya `--phone-number-id` + `--access-token`) |
| `python -m scripts create-flow` | Flow yarat + publish (env veya `--waba-id` + `--access-token` + `--public-base-url`) |
| `python -m scripts onboard` | Tenant için zincir: keys → upload-key → subscribe → create-flow → mongo |
| `python -m scripts set-flow-id <slug> <id>` | Mongo `business.channels.whatsapp.flow_id`'yi elle güncelle |
| `python -m scripts ig-refresh-token <slug>` | IG 60-gün long-lived token'ı yenile (çıktıdaki yeni token'ı `.env`'e yaz) |
| `python -m scripts ig-menu set <slug>` | IG Persistent Menu + Ice Breakers kur |
| `python -m scripts ig-menu get <slug>` | Mevcut IG menü kurulumunu görüntüle |
| `python -m scripts ig-menu delete <slug>` | IG Persistent Menu + Ice Breakers sil |
| `python -m scripts gen-test-token <slug>` | Flow Builder Preview için flow_token üret |
| `python -m scripts test-flow <token>` | 6-ekran Flow endpoint lokal simülasyonu |
| `python -m db.seed` | DB'yi sıfırla + 3 örnek işletme yükle |

Eksik argümanlar interaktif olarak sorulur; env değişkenleri (PHONE_NUMBER_ID, WABA_ID, ACCESS_TOKEN, PUBLIC_BASE_URL) varsa otomatik kullanılır.

## Mimari (özet)

```
WhatsApp Cloud API                 Instagram Graph API
        │                                  │
        ▼                                  ▼
  FastAPI /webhooks/whatsapp        FastAPI /webhooks/instagram
        │                                  │
   send Flow CTA mesajı        ┌── regex/postback dispatch ──► Quick Replies / metin listesi
        │                      │           │                   / Button Template ─► booking_url
        ▼                      └── "Müşteri Temsilcisi" ──► state=ai_active
  /webhooks/whatsapp/flow                  │
  (şifreli data_exchange)        core.ai (Groq) + core.tools ──► MongoDB (oku)
        │                                  │
        └─► booking.create_appointment ─► MongoDB ◄── booking_url (web sitesi)
```

Detay: [`docs/04-whatsapp-flow.md`](docs/04-whatsapp-flow.md).

## Stack

- **Python 3.12+**, FastAPI, motor (async MongoDB), pymongo (seed sync).
- **Pydantic v2** + pydantic-settings.
- **cryptography** — RSA-OAEP + AES-128-GCM (Flow endpoint).
- **httpx** — Meta Graph API + Groq (OpenAI-uyumlu) çağrıları.
- **Groq** — Instagram AI müşteri temsilcisi (OpenAI-uyumlu `/chat/completions`, tool-use).

## Bilinen sınırlar

- WhatsApp tarafında `online_booking_mode = "showcase"` (Vitrin) henüz yok.
- "Randevularım listele/iptal" Flow'u, hatırlatma cron'u, seanslı işlemler — yol haritasında (`docs/04-whatsapp-flow.md §4.8`).
- Multi-tenant `WA_APP_SECRET` tek değer; farklı app'ler altında çoklu tenant için kod genişletilmeli (`docs/02-meta-app.md §2.2`).
- Flow JSON 7.3 / Data API 4.0 kullanıyor; `flow_token_signature` JWT backend'de henüz doğrulanmıyor (X-Hub-Signature-256 zaten cover ediyor).
