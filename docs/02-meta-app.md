# 02. Meta App Temelleri

Meta App: **`<APP_NAME>`** (App ID `<APP_ID>`, Live mode, Business type). Gerçek değerler `.env` (`META_APP_ID`, ileride yazılırsa) ve Meta App Dashboard'ta tutulur.
Bu döküman App-seviyesindeki **her kanalda ortak** ayarları toplar. Kanala
özgü adımlar §3 (WhatsApp), §4 (WhatsApp Flow), §5 (Instagram), §6 (Tech
Provider) altında.

> Meta:
> [`fb-development/`](./Developers%20Facebook%20Documentation/output/fb-development/),
> [`fb-graph-api-webhooks/docs__graph-api__webhooks.md`](./Developers%20Facebook%20Documentation/output/fb-graph-api-webhooks/docs__graph-api__webhooks.md)

## 2.1 App Roles

Meta App Dashboard → **App roles → Roles**.

- `Administrator` rolünde olmadan WA/IG ürünlerinde token üretemezsiniz.
- Başkasına test ettirecekseniz **Tester** rolüyle ekleyin.
- IG self-test için **Instagram Tester** rolü gerekir; davet mobil IG → **Settings → Apps and Websites → Tester Invites**'tan kabul edilir.

> **Test users** sekmesi WA/IG için işe yaramaz (simüle FB hesapları).

## 2.2 App Secret

Meta App Dashboard → **App settings → Basic → App secret → Show**.

- **Tek değer**, hem WhatsApp hem Instagram webhook signature doğrulaması için kullanılır.
- `.env` → `WA_APP_SECRET` ve `IG_APP_SECRET` aynı string.
- Webhook signature başlığı: `X-Hub-Signature-256` (kod: `app/channels/whatsapp/client.py:verify_signature`).

> **UYARI (multi-tenant):** Mevcut implementasyon **tüm WA tenant numaralarının aynı Meta App altında olduğu varsayımıyla tek `WA_APP_SECRET` kullanır**. Farklı app'ler altında çoklu tenant kurulumu için `app/webhooks.py`'da business-bazlı secret lookup gerekir (roadmap — [§6.5](./06-tech-provider-onboarding.md#65-yol-haritası)).

## 2.3 App Mode

- **Development:** yalnız App Roles'ta listelenen kullanıcılar mesaj alabilir.
- **Live:** advanced access izinleri varsa herkese açık. Tester'lar Live modda da çalışır.

App'iniz zaten Live; geliştirici/tester olduğunuz sürece App Review beklemeden test edebilirsiniz (Standard Access yeterli).

## 2.4 Webhook verify token

Webhook ilk aboneliğinde Meta `GET /webhooks/<channel>?hub.mode=subscribe&hub.verify_token=...&hub.challenge=...` çağrısı yapar; backend `challenge`'ı echo'lar.

- Verify token = sizin belirlediğiniz rastgele string. Meta UI'a girdiğiniz değer `.env`'deki ile **birebir aynı** olmalı.
- Üretmek için: `openssl rand -hex 16`
- WA ve IG için **ayrı** string kullanın (biri sızsa diğeri etkilenmesin).

Kod: `app/webhooks.py:_verify_subscription`. 403 dönüyorsa token eşleşmiyor ya da uvicorn yeni `.env`'i okumadı.

## 2.5 Hangi ürünleri etkinleştirmek lazım

App Dashboard → **Use cases / Products** listesi:

| Ürün | Ne için | Detay |
|---|---|---|
| **WhatsApp** | Cloud API + Flow | [§3](./03-whatsapp-cloud-test.md), [§4](./04-whatsapp-flow.md) |
| **Instagram** | Messaging API | [§5](./05-instagram-test.md) |
| **Webhooks** | İki kanal için tek webhook endpoint subscription'ları | [§3.3](./03-whatsapp-cloud-test.md#33-webhook-subscribe), [§5.2](./05-instagram-test.md#52-webhook-subscribe) |
| **Facebook Login for Business** | Yalnız çoklu firma onboarding'i için | [§6](./06-tech-provider-onboarding.md) |

> **Marketing API, Pixel, Catalog, Conversions API, Audience Network, Pages CRUD, Threads, Limited Login — hiçbiri gerekli değil**. Dokümanlarıyla uğraşmayın.

## 2.6 App Dashboard → Settings → Basic — diğer alanlar

| Alan | Test için zorunlu mu | Üretim için zorunlu mu |
|---|---|---|
| App Domains | hayır (ngrok subdomain'i ekleyebilirsin) | ✅ |
| Privacy Policy URL | ✅ (Live mode için şart) | ✅ |
| Terms of Service URL | ✅ | ✅ |
| App Icon, Category | hayır | ✅ |
| Data Deletion callback URL | hayır | ✅ ([§6](./06-tech-provider-onboarding.md)) |

> Bu sayfadaki **Start verification** (Business / Access) butonlarına test aşamasında **DOKUNMAYIN** — App Review submit'e ya da belge yüklemeye yönlendirir. Yalnız üretim için ([§6.3](./06-tech-provider-onboarding.md#63-business-verification)).

---

**Sonraki:** [03. WhatsApp Cloud — self-test](./03-whatsapp-cloud-test.md)
