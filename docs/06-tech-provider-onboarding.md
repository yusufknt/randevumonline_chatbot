# 06. Tech Provider Onboarding — Çoklu Firma + Üretim

`randevumonline.com` firmalara randevu hizmeti veren bir SaaS. Firmalar kendi
WA numaralarını / IG hesaplarını **Embedded Signup** ile bağlar; biz onların
DM'lerine **firma adına** cevap üretiriz.

Meta nezdinde **Tech Provider (TP)** modeline karşılık gelir — Solution
Partner değil. Conversation ücretini Meta **doğrudan firmaya** faturalar.

> **Önkoşul:** [§02](./02-meta-app.md), [§03](./03-whatsapp-cloud-test.md), [§04](./04-whatsapp-flow.md) tamam. Bu döküman **üretim için**; self-test yetiyorsa atlanabilir.
>
> **Meta:**
> - [Solution Providers overview](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__solution-providers__overview.md)
> - [Get started for Tech Providers](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__solution-providers__get-started-for-tech-providers.md)
> - [TP App Review](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__solution-providers__app-review.md)
> - [Embedded Signup overview](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__embedded-signup__overview.md)
> - [Embedded Signup v4 implementation](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__embedded-signup__implementation.md)
> - [Onboarding customers as TP](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__embedded-signup__onboarding-customers-as-a-tech-provider.md)
> - [account_update webhook](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__webhooks__reference__account_update.md)

## 6.1 Model karşılaştırması

| Model | Credit line | Faturalama | Bizim mi? |
|---|---|---|---|
| **Tech Provider** | Yok | Meta → müşteri firma | ✅ |
| **Solution Partner** | Var | Bize/müşteriye | ❌ |
| **Tech Partner** | TP + Meta Business Partner statüsü | — | ❌ |

## 6.2 Token mimarisi

| Token | Scope | Yaşam | Saklama |
|---|---|---|---|
| Per-tenant **Business Integration System User token** | Müşteri firmanın WABA'sı | 60 gün (default template) | Vault: `vault://wa/<slug>/business_token` |
| App Secret | App-level webhook signature | Sınırsız | `.env` (tek değer, [§2.2](./02-meta-app.md#22-app-secret)) |
| Kendi sales system user token'ı | Yalnız sizin demo WABA'nız | Permanent | Vault |

> Tech Provider modelinde **per-tenant business token'lar `.env`'de tutulmaz** — N tenant olunca rotation imkânsız. Hepsi vault'ta `vault://wa/<slug>/business_token` path'inde.

## 6.3 Business Verification

Tech Provider onboarding ilerleyemez bu olmadan.

Meta Business Suite → **Settings → Business Info**:
- Vergi levhası / ticaret sicili
- Yetkili kişi kimlik
- Şirket adresi tevsiki

DemiraySoft / Kütahya Tasarım Teknokent kayıtlarınızı kullanın.

## 6.4 App Review (Tech Provider için)

App Dashboard → **Use cases → WhatsApp → Tech Provider onboarding → Begin App Review**. Standard Access ile kendi WABA'nızı test edebilirsiniz; başka business'lar için **Advanced Access** zorunlu.

### Zorunlu izinler

| Kanal | İzin | Submission içeriği |
|---|---|---|
| WhatsApp | `whatsapp_business_messaging` | Bir mesajın app'inizden gönderildiği + WA client'ta alındığı screen recording |
| WhatsApp | `whatsapp_business_management` | App'in (veya WA Manager'ın) template oluşturduğu screen recording |
| Instagram (yeni akış) | `instagram_business_basic` + `instagram_business_manage_messages` | DM gönderim/alım recording |
| Instagram (legacy) | `instagram_basic`, `instagram_manage_messages`, `pages_messaging`, `pages_manage_metadata` | — yalnız Page'e bağlı IG için |

> "Requesting unnecessary permissions is a common reason for rejection." Sadece kullandığınızı isteyin.

### Submission kuralları

- **Her izin için ayrı video** — birden fazla izni tek video'da göstermek otomatik reject.
- Reviewer için randevumonline.com paneline test user hesabı.
- Privacy Policy + Data Deletion callback URL'leri yayında olmalı.

## 6.5 Embedded Signup akışı

### 6.5.1 Facebook Login for Business → Settings

App Dashboard → **Facebook Login for Business → Settings → Client OAuth settings**. Şu toggle'ları **Yes** yap:
- Client OAuth login
- Web OAuth login
- Enforce HTTPS
- Embedded Browser OAuth Login
- Use Strict Mode for redirect URIs
- **Login with the JavaScript SDK** (Embedded Signup için zorunlu)

**Allowed Domains** ve **Valid OAuth redirect URIs**'a Embedded Signup butonunu host edeceğin tüm domain'leri ekle (HTTPS şart).

### 6.5.2 Configuration oluştur

App Dashboard → **Facebook Login for Business → Configurations → Create from template → "WhatsApp Embedded Signup Configuration With 60 Expiration Token"**.

→ Çıkan **`config_id`**'yi kopyala → `.env` → `EMBEDDED_SIGNUP_CONFIG_ID`.

> Gereksiz asset eklemeyin (Catalog vs.) — flow'da müşteri seçim ekranında takılır.

### 6.5.3 `account_update` webhook subscribe

App Dashboard → **Webhooks → WhatsApp → `account_update`** field'ı subscribe et. Embedded Signup tamamlanan her müşteri için event bildirir.

### 6.5.4 Frontend

```html
<script async defer crossorigin="anonymous"
        src="https://connect.facebook.net/en_US/sdk.js"></script>
<script>
  window.fbAsyncInit = function() {
    FB.init({
      appId: '<META_APP_ID>',
      autoLogAppEvents: true, xfbml: true, version: 'v25.0'
    });
  };

  // Session logging — phone_number_id, waba_id, business_id buradan
  window.addEventListener('message', (event) => {
    if (!event.origin.endsWith('facebook.com')) return;
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'WA_EMBEDDED_SIGNUP') {
        fetch('/api/onboarding/whatsapp/session', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(data)
        });
      }
    } catch (e) {}
  });

  // Response callback — exchangeable code, TTL: 30 SANIYE
  const fbLoginCallback = (response) => {
    if (response.authResponse) {
      fetch('/api/onboarding/whatsapp/exchange', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ code: response.authResponse.code })
      });
    }
  };

  const launchWhatsAppSignup = () => {
    FB.login(fbLoginCallback, {
      config_id: '<EMBEDDED_SIGNUP_CONFIG_ID>',
      response_type: 'code',
      override_default_response_type: true,
      extras: { setup: {} }
    });
  };
</script>
<button onclick="launchWhatsAppSignup()">WhatsApp'ı bağla</button>
```

> Final ekrandan X ile çıkmak da **`FINISH`** sayılır.

### 6.5.5 Backend — 3 server-to-server adım

**1) Code → business token (TTL 30 sn!):**
```bash
curl --get 'https://graph.facebook.com/v25.0/oauth/access_token' \
  -d 'client_id=<APP_ID>' \
  -d 'client_secret=<APP_SECRET>' \
  -d 'code=<CODE>'
# → <BUSINESS_TOKEN>. Vault'a yaz.
```

**2) Webhook'u client WABA'ya bağla:**
```bash
curl -X POST 'https://graph.facebook.com/v25.0/<WABA_ID>/subscribed_apps' \
  -H 'Authorization: Bearer <BUSINESS_TOKEN>'
# → {"success": true}
```

**3) Phone number'ı Cloud API'ye register et:**
```bash
curl 'https://graph.facebook.com/v25.0/<PHONE_NUMBER_ID>/register' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <BUSINESS_TOKEN>' \
  -d '{ "messaging_product": "whatsapp", "pin": "<6_DIGIT_PIN>" }'
```

PIN 2FA için — Vault'a tenant kaydında tut.

**4) Müşteri WhatsApp Manager'dan payment method ekler** — bu adım bizim API'mizden değil, panelde CTA göster: "WhatsApp Manager'da ödeme yöntemi ekle" → https://business.facebook.com/wa/manage/home/.

### 6.5.6 Onboarding limitleri

- **Default:** rolling 7 günde 10 yeni müşteri.
- Business Verification + App Review + Access Verification tamamsa: **200 / 7 gün**.
- 200+ için Meta Business Partner başvurusu.

WhatsApp Manager → **Partner overview** panelinden anlık sayım.

## 6.6 Tenant DB şeması

Embedded Signup callback handler her yeni firma için `businesses` dokümanına yazar:

```js
{
  contact: {
    phone: "<sabit hat>",
    whatsapp_number: "<müşteri-yüzü WA hattı>",
  },
  channels: {
    whatsapp: {
      enabled: true,
      phone_number_id: "<session logging'ten>",
      business_account_id: "<WABA ID>",
      waba_owner_business_id: "<firmanın Meta Business portfolio ID'si>",
      business_token_ref: "vault://wa/<slug>/business_token",
      token_expires_at: "<ISO 60 gün sonrası>",
      register_pin_ref: "vault://wa/<slug>/register_pin",
      subscribed_at: "<timestamp>",
      payment_method_ready: false,  // account_update webhook ile true'ya çekilir
      flow_id: null                 // scripts/create_flow.py sonrası dolar — §4.3
    },
    instagram: { /* benzer */ }
  }
}
```

Inbound webhook payload'undaki `phone_number_id` (WA) / `recipient.id` (IG) → DB'de tenant bul → o tenant'ın token'ıyla cevap gönder.

## 6.7 Token yaşam döngüsü

**WhatsApp business token** (60-gün template):
- `fb_exchange_token` long-lived swap'i **bu token tipi için yok**.
- Süre dolunca firma Embedded Signup'ı **yeniden tetikler** (panelde "Yeniden bağla" CTA'sı).
- Cron her gece: `token_expires_at < now + 7 gün` → reconnect e-postası + paneline banner.
- Webhook'tan `OAuthException` (code 190) → token revoked → tenant `enabled: false`.

**Instagram token:**
- App Dashboard token'ı 60-gün; Business Login flow token'ı 1-saat → `/refresh_access_token` ile uzatılır.

## 6.8 Üretim checklist'i

### 6.8.1 Meta
- [ ] App Live mode.
- [ ] Business Verification tamam.
- [ ] Privacy Policy + Terms of Service URL'leri.
- [ ] Data Deletion callback URL (`/api/meta/data-deletion`) yayında.
- [ ] Tech Provider onboarding sayfası tamamlandı.
- [ ] App Review (Advanced Access) — WA 2 izin + IG 2 izin.
- [ ] FBLfB → Settings → Allowed Domains'e production domain eklendi.
- [ ] FBLfB → Configurations → Embedded Signup config oluşturuldu.
- [ ] Webhook subscriptions: `messages` + **`account_update`**.

### 6.8.2 Backend
- [ ] `PUBLIC_BASE_URL` üretim HTTPS domain'i (Caddy/Nginx + Let's Encrypt).
- [ ] `app/webhooks.py` per-tenant routing (`phone_number_id` / `recipient.id`).
- [ ] Code → token swap **30 saniye içinde** tamamlanıyor.
- [ ] Per-tenant `subscribed_apps` POST Embedded Signup finalize'inde otomatik.
- [ ] `account_update` handler payment_method_ready'i günceller.
- [ ] Token expiry cron (gece, 7 gün kala reconnect).
- [ ] Token revoke fallback (`enabled: false` + email).
- [ ] Vault entegrasyonu canlı (per-tenant token'lar `.env`'de değil).
- [ ] Rate limiting (slowapi) + DDoS koruması.
- [x] Flow JSON **7.3** + Data API **4.0** — `flow_token_signature` HS256 JWT manifest seviyesinde aktif; backend doğrulaması roadmap'te ([§4.8](./04-whatsapp-flow.md#48-yol-haritası)).
- [ ] **Per-business `WA_APP_SECRET`** ([§2.2](./02-meta-app.md#22-app-secret) uyarısı) eğer çoklu app altında tenant varsa.

### 6.8.3 Frontend
- [ ] Embedded Signup butonu (`config_id`, `version: 'v25.0'`).
- [ ] `WA_EMBEDDED_SIGNUP` postMessage listener (`event.origin.endsWith('facebook.com')`).
- [ ] Bağlantı durumu: connected / payment_method_ready bekleniyor / token expiring / revoked.
- [ ] "Yeniden bağla" + "Ödeme yöntemi ekle" CTA'ları.
- [ ] **Bildirim numarası** zorunlu form alanı ([§6.6](#66-tenant-db-şeması)).

### 6.8.4 Yasal & operasyonel
- [ ] KVKK aydınlatma metni — bot ilk mesajında **"Bu sohbet otomatik bir asistan tarafından yönetiliyor"** uyarısı (Meta policy gereği).
- [ ] Firma sözleşmesinde TP rolü açıkça (faturalama firmaya).
- [ ] Loglama & alerting (Sentry/Grafana): token expiry, signature mismatch, `subscribed_apps` fail, `account_update`.
- [ ] Onboarding limit monitor (Partner overview).

## 6.9 Akış özeti

```
Firma paneline girer
  → "WhatsApp bağla" → FBLfB Embedded Signup popup
  → kendi FB + Business + WABA + numara seçer, izin verir
  → frontend: code (TTL 30 sn) + session payload backend'e
  → backend: code → business_token → subscribed_apps → register
  → DB'ye businesses.channels.whatsapp yazılır, vault'a token konur
  → firma WhatsApp Manager'dan payment method ekler
  → account_update webhook → payment_method_ready=true
  → bot canlıda
```

---

**Sonraki:** [07. Hata kılavuzu](./07-hata-kilavuzu.md) — tüm hata kodları.
