# 05. Instagram — Self-Test

IG Business hesabınızdan postback-driven (AI'sız) DM botu ile mesajlaşma.
**Instagram Login** (yeni, Page'siz) akışı kullanılır — legacy "Facebook Login"
akışına dokunma.

> **Önkoşul:** [§01](./01-yerel-kurulum.md) + [§02](./02-meta-app.md) tamam.
>
> **Ön şart:** IG hesabınız **Business** veya **Creator** tipinde olmalı.
> Personal hesap webhook abone olamaz.
> Mobil IG → **Settings → Account type and tools → Switch to Professional**.
>
> **Meta:**
> - [Instagram API with Instagram Login — Get Started](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__get-started.md)
> - [Messaging API](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api.md)
> - [Quick Replies](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api__quick-replies.md)
> - [Button Template](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api__button-template.md)
> - [Generic Template](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api__generic-template.md)
> - [Persistent Menu](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api__persistent-menu.md)
> - [Ice Breakers](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api__ice-breakers.md)

## 5.1 Token + IG ID

App Dashboard → **Instagram → API setup with Instagram business login**:

1. **Generate access tokens → Add Instagram account** → IG hesabınla giriş yap →
   izinleri onayla (`instagram_business_basic`, `instagram_business_manage_messages`, ...).
2. Listede:
   - **Token** (`IGAA…`, 60-gün long-lived) → `.env` →
     `IG_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN=IGAA...`
   - **Instagram User ID** (`<IG_ID>`, ~17 hane) → not al.

→ uvicorn yeniden başlat.

> 60 gün sonra token uzatılmalı:
> `python -m scripts ig-refresh-token berber_mehmet_kutahya` → çıktıdaki yeni
> `IG_..._ACCESS_TOKEN` değerini `.env`'e yaz. Token süresi dolarsa gönderimler
> 401/OAuth verir ve log doğrudan bu komuta yönlendirir.
>
> **"API setup with Facebook login" sekmesini KULLANMAYIN** — legacy IG-via-Page
> akışı; ekstra Page bağlama + App Review submit ister.

## 5.2 Webhook subscribe

Aynı sayfada → **2. Configure webhooks**:

1. **Callback URL:** `https://xxxx.ngrok-free.app/webhooks/instagram`
2. **Verify token:** `.env`'deki `IG_VERIFY_TOKEN` (WA'dan **farklı** bir string).
3. **Verify and save** → 200 + challenge echo.
4. **Subscribe fields:** `messages` ve **`messaging_postbacks` ZORUNLU**
   (button template / persistent menu / ice breaker tıklamaları postback olarak
   gelir; aboneliksiz kullanıcı butonlara tıklasa da botunuz cevap vermez).
   İsteğe bağlı: `message_reactions`; reklam/`ig.me` girişlerini karşılamak için
   `messaging_referrals` (kod referral'ı yakalar → karşılama menüsü).

> ### ⚠️ App Mode "Live" zorunlu (Instagram Login akışı için)
>
> WA Cloud API'den farklı olarak, **yeni Instagram Login (Page'siz) akışında**
> Meta, **Development modunda gerçek DM webhook'larını forward etmez** — tester
> hesap eklenmiş olsa bile. Verify ve subscription doğru gözükür ama hiçbir
> POST gelmez (ngrok inspector'da 0 trafik).
>
> **Çözüm:** App Dashboard sol üstte mod chip'ini **Development → Live** yap.
>
> - App review **gerekmez** — `instagram_business_manage_messages` Standard
>   Access seviyesinde Live'da çalışır.
> - Sadece Privacy Policy URL, kategori, ikon gibi temel "Basic Settings"
>   doldurulmuş olmalı.
> - Live'a geçtikten sonra **kendi tester IG hesabınla** mesajlaşmak yeterli;
>   review başka kullanıcılar için gerekecek.
>
> Meta UI'daki "*To receive webhooks, app mode should be set to 'Live'*"
> uyarısı tam olarak bu durumu anlatır. Hata kılavuzu: [§7.1](./07-hata-kilavuzu.md#71-webhook-subscription).

## 5.3 DB seed: IG ID + booking_url

`db/seed.py`:

```python
"channels": {
  "instagram": {
    "ig_user_id": "IG_USER_ID_PLACEHOLDER",   # §5.1 <IG_ID> ile değiştir
    ...
  },
},
"contact": {
  ...,
  "booking_url": "https://randevumonline.com/isletme/<slug>",
},
```

→ §5.1'deki `<IG_ID>` ile değiştir → `python -m db.seed`.

- Eşleştirme: `app/core/db.py:find_business_by_ig_user_id`
- `contact.booking_url` boş bırakılırsa "Randevu Al" tıklamasında bot kullanıcıya
  telefon numarasını döner (fallback metin).

## 5.4 Persistent Menu + Ice Breakers kurulumu

İşletme başına bir kerelik çalıştırılır; Meta tarafında IG profiline kalıcı menü
ve ilk açılışta görünen 4 hazır soruyu yazar (idempotent — yeniden çalıştırmak
sadece üzerine yazar).

```bash
# Kur
python -m scripts ig-menu set    berber_mehmet_kutahya

# Mevcut kurulumu görüntüle
python -m scripts ig-menu get    berber_mehmet_kutahya

# Sil
python -m scripts ig-menu delete berber_mehmet_kutahya
```

**Persistent Menu içeriği** (her IG thread'inde altta sabit):

| Buton | Tip | Davranış |
|---|---|---|
| 📅 Randevu Al | `web_url` | `business.contact.booking_url`'ı in-app browser'da açar |
| 💇 Hizmetler | `postback` (`IG:SERVICES`) | Aktif hizmetleri madde madde metin listesi olarak gönderir; booking_url varsa altında Button Template ("📅 Randevu Al" + "Menüye Dön") eklenir |
| ℹ️ Bilgi | `postback` (`IG:INFO`) | Çalışma saatleri + adres + telefon + 🗺️/💬 butonları |
| 👤 Personele Bağlan | `postback` (`IG:HUMAN`) | `conversation.state = "human_handoff"` |

> Persistent Menu güncellemeleri **anlık değildir**: mevcut thread'lerin menüyü
> görmesi için kullanıcının inbox'ı pull-to-refresh yapması gerekir. Yeni
> thread'ler güncel menüyü doğrudan görür.

**Ice Breakers** — yeni başlatan kullanıcının üstte gördüğü 3 hazır soru;
hepsi yukarıdaki postback payload'larıyla aynı handler'lara düşer (Randevu /
Hizmetler / Personel).

## 5.5 Inbound test

> IG, business → user yönünde **ilk teması blokluyor** (Meta policy). Test için
> ikinci bir IG hesabından (eş, arkadaş, başka telefon) hedef Business hesabına
> önce DM atın.

1. İkinci IG'den Business hesabınıza herhangi bir mesaj atın (örn "merhaba").
2. ngrok inspector → POST `/webhooks/instagram` görmelisiniz.
3. uvicorn loglarında `handle_instagram_payload` → **Quick Replies ana menü**
   gönderilir (4 buton).
4. Quick Reply'lerden birine basın → uvicorn loglarında postback event'i görün
   → ilgili cevap (booking link / hizmet listesi / bilgi paneli / handoff).
5. "📅 Randevu Al"e basınca: Button Template gelir; "Randevu Al" butonu
   in-app browser'da `booking_url`'ı açar.
6. "💇 Hizmetler"e basınca: `• Ad · süre dk · fiyat` formatında **madde madde
   metin listesi** gelir. `booking_url` tanımlıysa altında Button Template
   ("📅 Randevu Al" → `booking_url?src=ig`, "Menüye Dön") eklenir;
   `booking_url` yoksa son satırda telefon numarası yazar.
7. "ℹ️ Bilgi"ye basınca: tek Button Template — çalışma saatleri + adres + telefon
   metni + "🗺️ Haritada Aç" ve (WA açıksa) "💬 WhatsApp" butonları.
8. "👤 Personele Bağlan"a basınca: bot susar (state=human_handoff). Müşteri
   yazsa bile cevap gelmez (Meta inbox'tan manuel cevaplanır).

## 5.6 Outbound debug (manuel)

24h penceresi açıkken (önce kullanıcıdan DM gelmiş olmalı) düz text testi:

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/messages" \
  -H "Authorization: Bearer <IGAA_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": { "id": "<IGSID>" },
    "message": { "text": "merhaba" }
  }'
```

Quick Replies testi:

```bash
curl -X POST "https://graph.instagram.com/v25.0/<IG_ID>/messages" \
  -H "Authorization: Bearer <IGAA_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": { "id": "<IGSID>" },
    "message": {
      "text": "Test menü",
      "quick_replies": [
        {"content_type":"text","title":"📅 Randevu","payload":"IG:BOOK"},
        {"content_type":"text","title":"💇 Hizmetler","payload":"IG:SERVICES"}
      ]
    }
  }'
```

- `<IGSID>` = sana DM atan kullanıcının IG-scoped ID'si; webhook payload'unda
  `entry[].messaging[].sender.id` olarak gelir.
- Host'a dikkat: `graph.instagram.com` (legacy akış `graph.facebook.com`
  kullanıyordu).

## 5.7 Mimari

```
DM (text/quick_reply/postback)
    │
    ▼
app/webhooks.py:instagram_webhook  (X-Hub-Signature-256 doğrula → bg task)
    │
    ▼
app/core/orchestrator.py:handle_instagram_payload
  - parse_inbound (text / quick_reply / postback / unsupported / referral;
    echo & is_deleted atlanır)
  - idempotency: claim_inbound_message (tekrar webhook'lar atlanır)
  - business + customer + conversation upsert
  - quiet_hours guard (quiet_hours_message tanımlıysa tek seferlik bilgilendirme)
  - mark_seen + typing_on (görüldü/yazıyor göstergeleri)
  - state yönlendirmesi:
      • unsupported (görsel/sesli/sticker)  → nazik fallback (handoff'ta sessiz)
      • referral (reklam/ig.me)             → karşılama menüsü
      • serbest text + state=ai_active      → _instagram_ai_reply (Groq, §5.8)
      • serbest text + state=human_handoff  → bot sessiz (gerçek personel ilgilenir)
      • diğer her şey (postback dâhil)      → _instagram_deterministic
    │
    ▼
app/channels/instagram/flow.py:handle_event   (deterministik yol)
  - postback/QR payload varsa → ilgili handler (PB_BOOK/SERVICES/INFO/HUMAN/MENU)
  - serbest text → regex dispatch (sıra: APPT > SERVICES > BOOK > INFO > HUMAN)
  - hiçbiri kaçırsa → Quick Replies ana menü (5 dk debounce)
  - PB_HUMAN ("Müşteri Temsilcisi") → AI açıksa state=ai_active + welcome,
    kapalıysa human_handoff (telefon)
```

**Akış varsayılan olarak deterministik** — regex + postback dispatch + Meta'nın
zengin mesaj öğeleri (Quick Replies, Generic Template carousel, Button Template).
**"Müşteri Temsilcisi" butonuna basıldığında** (ve `AI_ENABLED=true` ise) sohbet
Groq tabanlı AI moduna geçer (§5.8). WhatsApp tarafındaki Flow yapısının IG
muadili: orada Flow JSON ekran sihirbazı, burada postback payload sözleşmesi +
web_url butonu.

### Postback payload sözleşmesi

`app/channels/instagram/flow.py` içinde sabit:

| Sabit | Değer | Tetikleyici |
|---|---|---|
| `PB_BOOK`     | `IG:BOOK`     | "Randevu Al" QR / persistent menu / ice breaker |
| `PB_SERVICES` | `IG:SERVICES` | "Hizmetler" — madde madde metin listesi (+ Button Template) |
| `PB_INFO`     | `IG:INFO`     | "Bilgi" — saat + adres + telefon + harita butonları |
| `PB_HUMAN`    | `IG:HUMAN`    | "Müşteri Temsilcisi" → AI açıksa state=ai_active (§5.8), kapalıysa human_handoff |
| `PB_MENU`     | `IG:MENU`     | "Menüye Dön" (Button Template'in son butonu) |

Yeni payload eklenecekse: `flow.py:_dispatch_payload` → handler ekle,
`scripts/ig_menu.py` → menü/ice breakers'a butonu yaz, bu dökümana satır ekle.

### Zengin mesaj öğelerinin kullanımı

| Öğe | Nerede | Neden |
|---|---|---|
| Quick Replies | Ana menü (4 buton) | En hızlı etkileşim, mobil IG'de yüksek dönüşüm |
| Persistent Menu | Tüm thread'lerde sabit (3-4 öğe) | Kullanıcı her zaman menüye ulaşabilsin, yazmasın |
| Ice Breakers | İlk açılış (3 hazır soru) | Yeni kullanıcıyı hemen harekete geçir |
| Text (madde listesi) | `_send_services` | Tüm hizmetleri tek mesajda `• ad · süre · fiyat` olarak göster |
| Button Template | `_send_book`, `_send_services` (booking_url varsa), `_send_info` | URL (booking/harita) + postback (Menüye Dön) karışık butonlar |

> **Generic Template (carousel) kullanılmıyor.** Önceki versiyonda hizmetler
> yana kaydırmalı carousel'da gösteriliyordu; şimdi sade metin listesi tercih
> edildi. Teknik referans için:
> [Generic Template](./Developers%20Facebook%20Documentation/output/fb-instagram-platform/docs__instagram-platform__instagram-api-with-instagram-login__messaging-api__generic-template.md)

## 5.8 Müşteri Temsilcisi (AI — Groq)

Ana menüdeki **"Müşteri Temsilcisi"** butonu (ve serbest metinde "canlı destek /
temsilci / yetkili / insan" kalıpları) AI sohbetini açar. AI, işletmenin **DB
bilgilerine** göre bir canlı müşteri hizmetleri temsilcisi gibi yanıtlar.

**Açma:** AI toggle `.env` bloğu (`AI_ENABLED` / `GROQ_API_KEY` / `GROQ_MODEL`)
tek kanonik yerde anlatılır — [§1.4 Groq API key](./01-yerel-kurulum.md#14-groq-api-key-ai-müşteri-temsilcisi--opsiyonel).
`AI_ENABLED=false` (varsayılan) iken buton eski davranışına (telefon numarası)
düşer; mevcut deterministik akış hiç değişmez.

> **Otomasyon ifşası (Meta politikası):** AI moduna girişte karşılama mesajı,
> kullanıcının otomatik bir asistanla konuştuğunu açıkça belirtir ve prompt asla
> "insan gibi davran" demez. İşletme özel `ai_settings.welcome_message` verirse
> sonuna bir bilgilendirme cümlesi eklenir; `ai_settings.ai_disclosure=""` ile
> kapatılabilir (sadece zaten ifşa içeren bir karşılama yazdıysan).

**Opsiyonel `ai_settings` alanları:**

| Alan | Etki |
|---|---|
| `ai_disclosure` | AI karşılamasına eklenen ifşa cümlesi (boş string → kapalı) |
| `quiet_hours_message` | Sessiz saatlerde gelen mesaja tek seferlik (6 sa debounce) otomatik yanıt; tanımsızsa bot tamamen sessiz kalır (eski davranış) |

**Çalışma şekli** (`app/core/ai.py` + `app/core/tools.py`):

- Groq, OpenAI-uyumlu `/chat/completions` + `tools` (function calling) kullanır;
  `GROQ_BASE_URL` değiştirilerek Ollama vb. de bağlanabilir.
- Her tur: system prompt (persona + bugünün tarihi + kurallar) + son
  `CONVERSATION_HISTORY_TURNS` mesaj + yeni mesaj → model tool çağırır →
  `tools.dispatch` çalışır → sonuç modele döner → düz metin çıkana kadar (max
  `AI_MAX_TOOL_ITERATIONS`) tekrarlanır.
- Tüm DB sorguları `business_id` ile izoledir (müşteri başka işletmeyi sorgulayamaz).

**Tool seti** (`tools.CUSTOMER_SERVICE_TOOL_NAMES` — bilgi + müsaitlik odaklı):

| Tool | İş |
|---|---|
| `get_business_info`        | adres, telefon, WhatsApp, e-posta, çalışma saatleri, özel günler, booking_url, harita, sosyal |
| `list_services`            | aktif hizmetler + süre + fiyat |
| `list_staff`               | personel (hizmet filtreli) |
| `list_available_slots`     | bir hizmet için en yakın uygun saatler |
| `list_staff_available_at`  | belirli saatte müsait personel |
| `get_customer_appointments`| müşterinin randevuları |
| `escalate_to_human`        | gerçek personele aktar → state=human_handoff (+ telefon) + `escalations` kuyruğuna kayıt |

> **Randevu DB'ye yazılmaz.** AI yeni randevu/iptal *yapmaz*; randevu almak
> isteyeni `booking_url`'e (web sitesi) yönlendirir. `create_appointment` /
> `cancel_appointment` tool'ları mevcut ama bu sete dâhil **değildir**.

**Durumlar (`conversations.state`):**

| State | Anlam | Serbest metin davranışı |
|---|---|---|
| `ai_active`     | AI sohbeti açık | Groq'a yönlendirilir |
| `human_handoff` | Gerçek personele aktarıldı | **Bot sessiz** (otomatik yanıt yok) |
| (diğer)         | Klasik menü | Regex dispatch |

AI modundan çıkış: herhangi bir menü postback'i (Ana Menü/Hizmetler/Bilgi/Randevu)
state'i `greeting`'e döndürür ve klasik akış devam eder.

**Hızlı test (AI açıkken):**
1. DM'den "Merhaba" → ana menü gelir.
2. **"Müşteri Temsilcisi"** → karşılama (welcome_message + otomasyon ifşası).
3. "Saç kesimi ne kadar?" → AI `list_services` ile fiyatı söyler.
4. "Yarın saat 15 müsait mi?" → AI `list_available_slots` ile yanıtlar.
5. "Randevu almak istiyorum" → AI `booking_url`'i paylaşır.
6. "Sizinle bir sorun yaşadım, yetkiliyle görüşmek istiyorum" → `escalate_to_human`
   → telefon verilir, sonraki serbest mesajlara bot yanıt vermez.

> Loglar: AI tool çağrıları `app.core.ai` / `app.core.tools` logger'larından
> `INFO` seviyede izlenir; tool turları `conversations.messages`'a `role:"tool"`
> olarak yazılır (denetim izi).

## 5.9 WhatsApp Flow'dan farkları

| | WhatsApp | Instagram |
|---|---|---|
| Booking akışı | 6-ekran Flow ([§04](./04-whatsapp-flow.md)) | Metin listesi + Button Template → web_url (site açılır) |
| Hizmet gösterimi | — | `• ad · süre · fiyat` metin listesi |
| AI kullanımı | Yok | Opsiyonel — "Müşteri Temsilcisi" (Groq, §5.8) |
| İlk teması | Kullanıcı veya bot | **Yalnız kullanıcı** |
| Token tipi | Permanent business token | 60-gün long-lived |
| Webhook fields | `messages` | `messages` + `messaging_postbacks` |
| Kalıcı menü | Yok | Persistent Menu (3-4 öğe, sabit) |
| Sıfırdan kullanıcı yardımı | — | Ice Breakers (3 hazır soru) |

## 5.10 Bilinen sınırlar

- **24h pencere:** Müşteri DM atmazsa siz bot olarak ilk mesajı atamazsınız
  (Meta policy). Persistent Menu mevcut sohbette görünür ama yeni tetikleyemez.
- **Text mesaj:** Max 1000 byte (UTF-8; Türkçe harf 2, emoji 4 byte). 1000 byte'ı
  aşan yanıtlar `send_text` tarafından kelime sınırında **otomatik parçalanır**.
- **Metin dışı mesaj:** Görsel/sesli/dosya/sticker'a bot içeriği göremediğini
  belirten nazik bir fallback ile yanıtlar (handoff state'inde sessiz kalır).
- **Quick Replies:** Max 13 buton, başlık 20 char (otomatik trunc edilir).
  Sadece mobil; desktop'ta gösterilmez.
- **Button Template:** Max 3 buton, text max 640 char. Sadece mobil.
- **Ice Breakers:** Max 4 soru; mevcut kurulumda 3 kullanılıyor (`ig_menu.py`).
- **Persistent Menu:** Max 5 öğe (Meta en iyi pratik). `webview_height_ratio`
  parametresi IG'de desteklenmiyor. Güncelleme anlık değil — inbox pull-to-refresh
  gerekir, yeni thread'ler güncel menüyü görür.
- **Standart Access:** Sadece app'e role atanmış kullanıcılar bot ile
  konuşabilir. Üretim için **Advanced Access** + App Review gerekir.
- **AI (Müşteri Temsilcisi):** Groq ücretsiz katmanı dakika/gün limitlidir
  (429 → kod otomatik backoff + 3 deneme yapar). 24h pencere AI moduna da uygulanır
  (müşteri yazmadan bot ilk mesajı atamaz). AI yalnız DB'deki bilgiyi söyler;
  randevuyu DB'ye yazmaz, `booking_url`'e yönlendirir.
- **Generic Template (carousel):** Teknik olarak destekleniyor (max 10 element,
  kart başına max 3 buton, title/subtitle 80 char, sadece mobil) ama bu projede
  kullanılmıyor — hizmetler sade metin listesiyle gösteriliyor.

---

**Sonraki:** [06. Tech Provider onboarding](./06-tech-provider-onboarding.md) —
çoklu firma + üretim için.
