# 04. WhatsApp Flow — Randevu Akışı

WhatsApp Flow tabanlı 6-ekran randevu sihirbazı. WA tarafında AI yok;
gelen mesaj doğrudan Flow CTA mesajını tetikler, müşteri Flow'u
doldurur, endpoint randevuyu yaratır.

> **Önkoşul:** [§03](./03-whatsapp-cloud-test.md) tamam (Cloud API webhook çalışıyor).
>
> **Meta:**
> - [Flows overview](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows.md)
> - [Sending a Flow](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__guides__sendingaflow.md)
> - [Implementing your Flow Endpoint](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__guides__implementingyourflowendpoint.md)
> - [Receiving Flow Response](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__guides__receiveflowresponse.md)
> - [Flow JSON reference](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__reference__flowjson.md)
> - [Components reference](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__reference__components.md)
> - [Error codes](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__reference__error-codes.md)
> - [Encryption](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__guides__whatsapp-business-encryption.md)

## 4.1 Akış (kullanıcı gözünden)

```
müşteri → herhangi bir text
bot     → CTA mesajı [Randevu Al]
müşteri → CTA'ya dokun → Flow uygulaması açılır
          1. AD_SOYAD  (Ad + Soyad)
          2. SERVICE   (Hizmet — DB'den taze)
          3. STAFF     (Personel — "Fark etmez" seçeneği; tek personel ise atlanır)
          4. DAY       (Müsait günler)
          5. TIME      (O günün :00/:30 slotları)
          6. CONFIRM   (Özet + Randevu Notu opsiyonel + "Onayla")
bot     → "✅ Randevunuz onaylandı..." özet metni
```

Her "Devam" basışı endpoint'e şifreli HTTP POST atar; sonraki ekran data'sı DB'den taze gelir (race-safe).

## 4.2 RSA anahtar çifti

Flow endpoint'e gelen payload AES-128-GCM ile şifrelidir; AES anahtarı ise
RSA-OAEP-SHA256 ile (Meta'nın imzaladığı public key kullanarak) şifrelenir.

```bash
.venv/bin/python -m scripts gen-keys
# → secrets/flow_private.pem
# → secrets/flow_public.pem
```

`.env`:
```
WA_FLOW_PRIVATE_KEY_PATH=secrets/flow_private.pem
WA_FLOW_PRIVATE_KEY_PASSPHRASE=          # passphrase'siz üretildi
```

Public key'i Meta'ya yükle (her phone_number_id için bir kez):

```bash
.venv/bin/python -m scripts upload-key \
  --phone-number-id <PHONE_NUMBER_ID> --access-token EAA...
# veya env değişkenleriyle: PHONE_NUMBER_ID=... ACCESS_TOKEN=... python -m scripts upload-key
```

> Meta her isteği imzalayıp döner — public key WA Cloud Manager'da "Signed" görünmeli. "Missing" durursa Flow publish edilemez.

> **Not (Meta UI):** Yeni WhatsApp Manager arayüzünde **Phone Numbers** sayfasında artık "Business encryption key" sekmesi **yok** — yükleme/imza yalnız Graph API üzerinden yapılır. Flow editör sayfasındaki *"Bu, Akış ile uç noktanız arasındaki veri alışverişinin şifrelenmesini sağlayacak. Aşağıdaki talimatları izleyin"* uyarısı bu adıma yönlendirir.

Yüklemeyi API ile doğrula:

```bash
set -a && source .env && set +a && \
curl -s "https://graph.facebook.com/v25.0/<PHONE_NUMBER_ID>/whatsapp_business_encryption?access_token=$WA_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN" \
  | python3 -m json.tool
# Beklenen: "business_public_key_signature_status": "VALID"
```

**Sık karşılaşılan tuzaklar:**
- `.env`'de `WA_FLOW_PRIVATE_KEY_PASSPHRASE=` **boş olmalı** (anahtar passphrase'siz üretildiyse). Dolu bırakırsan endpoint `421 Misdirected Request` döner — log'da `Password was given but private key is not encrypted`.
- Access token expire olduysa `upload-key` `(#100) Object does not exist or missing permissions` der; API Setup'tan token'ı yenile ([§3.2](./03-whatsapp-cloud-test.md#32-temp-token)).
- Token izni: `whatsapp_business_messaging` yeterli (Meta resmi spec — [encryption guide](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__guides__whatsapp-business-encryption.md)). Başka business adına çalışıyorsan **Advanced Access** lazım.

**Doğrulama yanıt durumları:**
- `VALID` → her şey yolunda, Flow şifrelemesi aktif.
- `MISMATCH` → yüklenen public key Meta'nın imzaladığı versiyonla uyuşmuyor. `gen-keys --force` + `upload-key`'i tekrar çalıştır.

**Public key'i yeniden yüklemen gereken durumlar** ([Meta resmi spec](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__guides__implementingyourflowendpoint.md#L52-55)):
- Numara yeniden register edildiğinde
- Meta webhook `messages.errors` içinde `public-key-missing` veya `public-key-signature-verification` hatası gönderdiğinde

## 4.3 Flow yarat + publish + flow_id

### 4.3.1 Standart yol — `onboard` (önerilen)

`onboard` aşağıdaki 5 adımı sırayla çalıştırır; her argüman `env`'den
veya interaktif olarak sorulur:

```
1. RSA anahtar çifti (mevcutsa atlar)
2. Public key Meta'ya yükle (upload-key)
3. WABA → uygulamanızı webhook'a subscribe et
4. Flow JSON'ı Meta'ya POST et, endpoint URI'sini bağla, publish et
5. Mongo: phone_number_id + WABA ID + flow_id business kaydına yazılır
```

```bash
.venv/bin/python -m scripts onboard \
  --phone-number-id <PHONE_NUMBER_ID> \
  --waba-id <WABA_ID> \
  --access-token EAA... \
  --public-base-url https://xxxx.ngrok-free.app
  # --business-slug berber_mehmet_kutahya  (default)
```

`onboard` başarılı çıkarsa Mongo güncellenmiş demektir — `set-flow-id`
komutuna gerek kalmaz. Yalnızca sonradan elle güncelleme gerekirse:

```bash
.venv/bin/python -m scripts set-flow-id berber_mehmet_kutahya <FLOW_ID>
```

> Manifestin nasıl üretildiği: `app/channels/whatsapp/flow_manifest.py:build_flow_json`. Tek tenant için tek manifest yeterli; her tenant kendi `flow_id`'sini DB'de tutar.

### 4.3.2 DRAFT mode (Business Verification olmadan test)

Business Verification olmayan WABA'da `onboard`'un adım 4'ü
`(#139000) Blocked by Integrity` döner — bu **beklenen** davranıştır.
Flow `DRAFT` halinde kalır; Cloud API üzerinden CTA göndermek için
BV zorunludur ([§6.3](./06-tech-provider-onboarding.md#63-business-verification)).

DRAFT durumda iki test yöntemi vardır:

**Yöntem A — `WA_FLOW_MODE=draft` (ileride BV + publish sonrası):**

```bash
# .env
WA_FLOW_MODE=draft
```

> ⚠️ **BV olmadan Cloud API Flow CTA göndermek mümkün değildir.** `WA_FLOW_MODE=draft` parametresi, BV yapıldıktan sonra Flow henüz PUBLISHED değilken test etmek içindir. BV'siz WABA'da `mode=draft` olsa bile `#139000 Blocked by Integrity` hatası alınır. BV öncesi test için Yöntem B'yi kullanın.

**Yöntem B — Flow Builder Preview (simülatör, telefon gerektirmez):**

1. Lokal `flow.json` üret:
   ```bash
   .venv/bin/python -c "
   from app.channels.whatsapp.flow_manifest import build_flow_json
   import json
   data = json.loads(build_flow_json())
   open('flow.json','w',encoding='utf-8').write(
     json.dumps(data, indent=2, ensure_ascii=False))
   "
   ```

2. [WhatsApp Manager → Flows](https://business.facebook.com/wa/manage/flows/) →
   **Create flow** → Category: `APPOINTMENT_BOOKING` → boş şablon seç.

3. Editor'da JSON paneli → **Ctrl+A → Delete** → `flow.json` içeriğini yapıştır → **Save**.

4. **Endpoint** sekmesi → URI: `<PUBLIC_BASE_URL>/webhooks/whatsapp/flow` → **Save**
   → "Health check request successful" görülmeli.

5. **Preview** sekmesi → **Run** → AD_SOYAD → SERVICE → STAFF → DAY → TIME →
   CONFIRM → her adımda uvicorn `Flow endpoint action=data_exchange screen=...` logu.

   > `flow_token` alanını boş bırakın. Backend, `flows-builder-` prefix'li
   > token'ları `WA_FLOW_PREVIEW_BUSINESS_SLUG` env'indeki (veya fallback olarak
   > `berber_mehmet_kutahya`) tenant ile çalıştırır.

Manifest güncellendiğinde: adım 1'i tekrarlayın, Flow Builder Editor'a
yapıştırın → **Save** → Preview'ı yeniden başlatın. Ya da CLI ile:

```bash
curl -X POST "https://graph.facebook.com/v25.0/<FLOW_ID>/assets" \
  -F "name=flow.json" -F "asset_type=FLOW_JSON" \
  -F "file=@flow.json;type=application/json" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

> Flow Builder Preview yalnızca simülatör test eder; gerçek telefona mesaj gitmez.
> Üretim / gerçek mobil test için BV + `onboard` zinciri gerekir.

## 4.4 Mimari

```
[Müşteri] ──text──▶ /webhooks/whatsapp
                          │
                          ▼
                  send_booking_flow → interactive.type=flow (CTA mesajı)
                          │
[Müşteri] ──tap CTA──────▶ Flow app açılır

  Her ekran arası:
    Flow app ──şifreli POST──▶ /webhooks/whatsapp/flow
                                     │
                                     ├─ X-Hub-Signature-256 doğrula → 432
                                     ├─ RSA-OAEP-SHA256 ile AES key çöz → 421
                                     ├─ AES-128-GCM ile payload çöz
                                     ├─ flow_token parse → 427
                                     ├─ action route et (data_exchange / BACK / ping)
                                     └─ AES-GCM ile yanıt şifrele (ters IV)
                                          │
                                          ▼ base64 plaintext
    Flow app ◀────────────── şifreli yanıt

  CONFIRM "Onayla":
    Endpoint create_appointment'ı çağırır.
    Başarı → screen: "SUCCESS" payload → Flow kapanır
           → nfm_reply webhook'a gelir → orchestrator özet metni yollar.
    Slot dolu → screen: "CONFIRM" + error_message → snackbar.
```

İlgili dosyalar:
- `app/channels/whatsapp/flow_sender.py` — `send_booking_flow`, `make_flow_token`, `parse_flow_token`.
- `app/channels/whatsapp/flow.py` — `handle_endpoint_request`, ekran builder'ları (`_build_*`).
- `app/channels/whatsapp/flow_crypto.py` — RSA-OAEP + AES-128-GCM.
- `app/channels/whatsapp/flow_manifest.py` — 6-ekran Flow JSON.
- `app/webhooks.py:whatsapp_flow_endpoint` — `/webhooks/whatsapp/flow`.

## 4.5 Flow token

```
biz:<business_oid_hex>:conv:<conversation_oid_hex>:<32-hex-nonce>
```

- `32-hex-nonce` = `secrets.token_hex(16)` = 128-bit. Meta: "token tahmin edilemez olmalı" (Implementing Endpoint guide).
- Endpoint çağrısı geldiğinde `parse_flow_token` ile business + conversation çözülür.
- Form tamamlandığında `nfm_reply.response_json` da `flow_token` taşır (double-check için).

> Üretimde HMAC imzası + TTL eklenmesi roadmap'te (replay'e karşı).

## 4.6 Davranış kuralları

### 4.6.1 Race condition (slot)

Müşteri form'u doldururken slot başkasının olabilir. CONFIRM `data_exchange`:
- `create_appointment` `slot_taken` döndürürse aynı ekran `error_message` ile döner; kullanıcı snackbar görür, geri dönüp başka saat seçer.
- Kullanıcının yazdığı **`notes` değeri Form `init-values: {notes: "${data.notes}"}` üzerinden korunur** (manifest CONFIRM screen).

### 4.6.2 "Fark etmez" personel

STAFF ekranında `staff_id = "any"` seçilirse, CONFIRM aşamasında o saate uygun ilk personel atanır (`booking.find_staff_available_at`).

### 4.6.3 Endpoint hata kodları (Meta spec)

| Kod | Anlam | Davranış |
|---|---|---|
| 200 | Normal akış | Şifreli base64 yanıt (text/plain) |
| 421 | Decrypt fail | Mobil istemci public key'i yeniden çeker |
| 427 | flow_token geçersiz | CTA disable edilir, `error_msg` döner |
| 432 | Signature fail | Generic error |

### 4.6.4 Dropdown limiti

`MAX_DROPDOWN_ROWS = 200` (image yok → Meta limiti 200). Daha fazla
hizmet/personel/gün olan tenant'larda ilk 200 listelenir.

### 4.6.5 CTA payload

`flow_action_payload.data` boş `{}` olamaz (Meta non-empty obje ister).
AD_SOYAD ilk ekranı dış data almadığı için `data` alanı **komple omit**
edilir.

## 4.7 docs/sistem.md ile farklar

Bunlar **kasıtlı** tasarım kararlarıdır.

| sistem.md kuralı | WA Flow davranışı | Neden |
|---|---|---|
| §1 telefon + SMS doğrulama | YOK; doğrudan AD_SOYAD | WA Cloud zaten `wa_id`'yi doğrulanmış olarak iletir |
| `ai_settings.confirmation_required` | Yok sayılır; status doğrudan `confirmed` | CONFIRM ekranı zaten manuel onay |
| `online_booking_mode = "showcase"` | Henüz yok | Roadmap §4.8 |
| §5.1/§5.2 "Randevularım listele/iptal" | WA Flow tarafında yok | Roadmap §4.8 |

## 4.8 Yol haritası

- [ ] Per-WABA RSA anahtarları (şu an tek tenant tek anahtar).
- [ ] `flow_token` HMAC imza + TTL (replay koruması).
- [x] Flow JSON **7.3** + Data API **4.0** (`flow_token_signature` JWT — manifest seviyesinde aktif). Meta: [`changelogs.md`](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__changelogs.md).
- [ ] **JWT verify implementasyonu**: `flow_token_signature` HS256 JWT'sini App Secret ile doğrula (şu an alan görmezden geliniyor; X-Hub-Signature-256 zaten request body imzalıyor — `app/channels/whatsapp/flow.py`).
- [ ] **Per-business `WA_APP_SECRET`** ([§2.2](./02-meta-app.md#22-app-secret) uyarısı).
- [ ] `update_data` action ile gerçek-zamanlı bağımlı dropdown'lar (endpoint çağrısı azalır).
- [ ] Hatırlatma mesajı cron'u (işletme `ai_settings.reminder_minutes_before`).
- [ ] "Randevularım" + iptal Flow'u (yeni manifest + `cancel_count` auto-block).
- [ ] Vitrin (showcase) modu alternatif routing.
- [ ] Seanslı işlemler (Service modeline `session_count` / `parent_service_id`).

---

**Sonraki:** [05. Instagram self-test](./05-instagram-test.md) (opsiyonel) veya [06. Tech Provider](./06-tech-provider-onboarding.md) (üretim).
