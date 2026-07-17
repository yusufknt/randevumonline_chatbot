# 03. WhatsApp Cloud API — Self-Test

Meta'nın ücretsiz test number'ıyla **App Review / Business Verification /
payment olmadan** kendi telefonunuza mesaj alıp gönderme akışı.

> **Önkoşul:** [§01](./01-yerel-kurulum.md) + [§02](./02-meta-app.md) tamam — uvicorn + ngrok ayakta.
>
> **Meta:**
> - [WA Cloud API → Get Started](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__get-started.md)
> - [Phone Numbers](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__business-phone-numbers__phone-numbers.md)
> - [Access Tokens](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__access-tokens.md)
> - [Send Messages](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__messages__send-messages.md)

## 3.1 Test number + Phone Number ID

App Dashboard → **WhatsApp → Step 1. Try it out**.

- **Test number** otomatik atanır (ör. `+1 555 XXX XXXX`). Bedava, payment yok.
- **Phone Number ID** sağda kopyalanır (`<PHONE_NUMBER_ID>`). Graph API URL'lerinde geçer (`/v25.0/<PHONE_NUMBER_ID>/messages`).
- **WABA ID** — yönetim API'leri için (`<WABA_ID>`); mesaj atmak için gerekmez.

> Gerçek değerleri `.env` ve Mongo `businesses.channels.whatsapp` altında tutulur — bu döküman boyunca `<PHONE_NUMBER_ID>` / `<WABA_ID>` placeholder'ları geçer.

> Bu sayfadaki **Step 2 → "Register your WhatsApp phone number / Add payment / Test your registered number"** butonlarına **dokunmayın**. Yalnız sizin gerçek production numaranızı kayıtlamak için.

## 3.2 Temp token

Aynı **Step 1** sayfası → **Access token → Generate token** → 24 saatlik temp token (`EAA…`) çıkar.

```bash
# .env
WA_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN=EAA...
```

→ uvicorn yeniden başlat.

> **Uyarı (temp token):** Bu sayfa **yenilendiğinde** token görünmez olur (gösterimi geçici, kendisi de 24 saatte expire). Token'ı aldıktan sonra **hemen** `.env`'ye yapıştır ve `python -m scripts upload-key` / `create-flow` adımlarını koş. `python -m scripts setup` sihirbazı bu yüzden Tenant token'larını **en son adıma (7/7)** koyar — sayfayı yenilemen gerekmesin diye.
>
> Kalıcı için: **Business Settings → System Users → Generate Token** (`whatsapp_business_messaging` + `whatsapp_business_management` izinleri).

## 3.3 Webhook subscribe

App Dashboard → **WhatsApp → Step 2. Production setup → Configure Webhooks** kutusu:

1. **Callback URL:** `https://xxxx.ngrok-free.app/webhooks/whatsapp` ([§1.6](./01-yerel-kurulum.md#16-servisleri-başlat-her-oturum) ngrok URL'i + `/webhooks/whatsapp`).
2. **Verify token:** `.env`'deki `WA_VERIFY_TOKEN` ile birebir aynı ([§2.4](./02-meta-app.md#24-webhook-verify-token)).
3. **Verify and save** → 200 + challenge echo.
4. **Webhook fields** listesinde **`messages`** satırını **Subscribe** edin.
5. **WABA → senin app'ine subscribe et** (kritik):

   ```bash
   set -a && source .env && set +a && \
   curl -X POST "https://graph.facebook.com/v25.0/<WABA_ID>/subscribed_apps?access_token=$WA_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN"
   # Doğrula:
   curl "https://graph.facebook.com/v25.0/<WABA_ID>/subscribed_apps?access_token=..."
   ```

   Yeni oluşturulan test number'lar varsayılan olarak Meta'nın **"WA DevX Webhook Events 1P App"** uygulamasına subscribe olur — senin app'in webhook URL'in dolu olsa bile mesaj **gelmez**. Yukarıdaki POST senin app'ini WABA'ya bağlar.

Hata olursa: [§07.1 Webhook verify 403](./07-hata-kilavuzu.md#71-webhook-verify-403).

## 3.4 Recipient ekle (5 limitli)

Test number yalnız doğrulanmış 5 numaraya mesaj atabilir.

App Dashboard → **WhatsApp → Step 1** → **Recipient dropdown → Manage phone number list → + Add phone number** → kendi numaranızı `+90...` formatıyla yazın → WhatsApp'a gelen 6 haneli kodu girin.

> Eklenmeyen numaralar `(#131030) Recipient phone number not in allowed list` döner — [§07](./07-hata-kilavuzu.md).

## 3.5 DB seed'inde Phone Number ID'yi gerçek değerle değiştir

`db/seed.py:87`:

```python
"phone_number_id": "WA_PNID_PLACEHOLDER",
```

→

```python
"phone_number_id": "<PHONE_NUMBER_ID>",   # §3.1'den
```

```bash
.venv/bin/python -m db.seed
```

Eşleştirme: `app/core/db.py:find_business_by_wa_phone_number_id` inbound
payload'daki `metadata.phone_number_id`'yi DB'deki bu alanla eşler.

## 3.6 Outbound test (bot → telefon)

```bash
curl -X POST "https://graph.facebook.com/v25.0/<WA_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <TEMP_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "905XXXXXXXXX",
    "type": "text",
    "text": { "body": "merhaba" }
  }'
```

Veya UI'daki **Send message** butonuyla `Order Confirmation` template'i.

## 3.7 Inbound test (telefon → bot)

1. Telefondan test number'a "merhaba" yazın.
2. ngrok inspector (`http://127.0.0.1:4040`) → POST `/webhooks/whatsapp` görmelisiniz.
3. uvicorn loglarında `handle_whatsapp_payload` çalışır.
4. Cevap olarak **WhatsApp Flow CTA** mesajı düşmeli ("Randevu Al" butonlu).

> Flow CTA'sı düşmüyorsa, henüz Flow yaratılmamış olabilir — [§04](./04-whatsapp-flow.md)'e geçin. CTA olmadan da bot cevap üretebilmesi için bot şu an WhatsApp tarafında AI çalıştırmıyor; mesaj yalnız Flow CTA'sıyla yanıtlanıyor (mimari: `app/core/orchestrator.py:handle_whatsapp_payload`).

---

**Sonraki:** [04. WhatsApp Flow — Randevu](./04-whatsapp-flow.md)
