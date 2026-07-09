# 07. Hata Kılavuzu

Tüm projenin merkezi troubleshooting referansı. Hata mesajları kanal ve
akışlara göre gruplandırılmıştır.

> **Meta error code referansları:**
> - [WA Cloud API messages errors](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__webhooks__reference__messages__errors.md)
> - [Embedded Signup errors](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__embedded-signup__errors.md)
> - [WA Flows error codes](./Developers%20Facebook%20Documentation/output/fb-whatsapp-flows/documentation__business-messaging__whatsapp__flows__reference__error-codes.md)

## 7.1 Webhook subscription

| Belirti | Olası neden | Çözüm |
|---|---|---|
| **403 Forbidden** (Verify and save sırasında) | Verify token Meta UI ile birebir eşleşmiyor; `.env` değişti ama uvicorn restart yok | Token'ı yeniden yapıştır, uvicorn Ctrl-C → yeniden başlat |
| Webhook POST **401 invalid_signature** | `WA_APP_SECRET` / `IG_APP_SECRET` boş veya yanlış (`app/channels/whatsapp/client.py:verify_signature`) | [§2.2](./02-meta-app.md#22-app-secret) — secret'ı yeniden al, `.env`'e koy, restart |
| Webhook hiç tetiklenmiyor | ngrok URL Meta UI'da güncel değil; `messages` field subscribe edilmemiş | <http://127.0.0.1:4040> ile trafiği gör; Meta'da callback URL'i güncelle; `messages` subscribe et |
| **IG webhook hiç gelmiyor** — verify ✅, subscription ✅, tester ✅ ama ngrok'a 0 POST | **App "Development" modunda.** Yeni Instagram Login akışında Meta gerçek DM event'lerini Dev modunda forward etmez (WA Cloud API'den farkı budur). Meta UI'daki *"To receive webhooks, app mode should be set to 'Live'"* uyarısı tam bunu anlatır | App Dashboard sol üst → mod chip'i **Development → Live**. App review gerekmez; Basic Settings (Privacy Policy URL, kategori, ikon) yeterli. Detay: [§5.2 uyarı kutusu](./05-instagram-test.md#52-webhook-subscribe) |
| IG webhook gelir ama log "**Eşleşen business yok: ig_user_id=...**" | DB'deki `channels.instagram.ig_user_id`, Meta UI'da "API setup with Instagram business login → Generate access tokens" tablosunda görünen ID ile eşleşmiyor. NOT: token'la `/me` çağrısının döndüğü ID **app-scoped**'dır, webhook'ta gelen ID **değildir** | Meta UI'daki tabloda gözüken ID'yi al (17841… formatında), `db/seed.py` + Mongo `businesses.channels.instagram.ig_user_id` alanına yaz |

## 7.2 WhatsApp Cloud — gönderim

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Outbound curl **401 OAuthException** | 24h temp token expire oldu | [§3.2](./03-whatsapp-cloud-test.md#32-temp-token) — Generate token tekrar |
| **(#131030) Recipient phone number not in allowed list** | Test number 5 doğrulanmış recipient ile sınırlı | [§3.4](./03-whatsapp-cloud-test.md#34-recipient-ekle-5-limitli) — Manage phone number list |
| **(#100) Invalid parameter** (Flow CTA mesajında) | `flow_id` `null` veya manifest `INVALID_PROPERTY_*` ile reddedildi | [§4.3](./04-whatsapp-flow.md#43-flow-yarat--publish--flow_id) — `scripts/create_flow` çalıştır, `flow_id`'yi DB'ye yaz |
| Token revoked / `OAuthException` code 190 | Müşteri Embedded Signup'ı iptal etti veya token expired | Tenant `enabled: false`, panele "Yeniden bağla" CTA'sı ([§6.7](./06-tech-provider-onboarding.md#67-token-yaşam-döngüsü)) |

## 7.3 WhatsApp orchestrator (kod tarafı)

| Belirti | Olası neden | Çözüm |
|---|---|---|
| `Eşleşen business yok: phone_number_id=...` | DB'de `channels.whatsapp.phone_number_id` placeholder veya farklı | [§3.5](./03-whatsapp-cloud-test.md#35-db-seedinde-phone-number-idyi-gerçek-değerle-değiştir) — seed güncelle |
| WhatsApp'a mesaj atılıyor ama webhook hiç tetiklenmiyor | WABA varsayılan **"WA DevX Webhook Events 1P App"**'ine bağlı, senin app'ine değil | [§3.3](./03-whatsapp-cloud-test.md#33-webhook-subscribe) — `POST /<WABA_ID>/subscribed_apps` ile senin app'ini bağla |
| `Secret bulunamadı: vault://wa/...` runtime hatası | `.env` değişken adı eksik/yanlış | `vault://wa/berber_mehmet_kutahya/access_token` → env adı `WA_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN` (büyük harf, `/` → `_`) |
| Log'da `Flow CTA gönderilemedi: {'error': 'flow_not_configured'}`, kullanıcıya fallback mesajı gidiyor | DB'de `channels.whatsapp.flow_id` boş/null | `python -m scripts onboard` ile Flow yarat veya `python -m scripts set-flow-id <slug> <FLOW_ID>` ile mevcut flow_id'yi yaz ([§4.3](./04-whatsapp-flow.md#43-flow-yarat--publish--flow_id)). Test number kullanıyorsan DRAFT mode için [§4.3.2](./04-whatsapp-flow.md#432-draft-mode-business-verification-olmadan-test) bakın. |

## 7.4 WhatsApp Flow endpoint

| HTTP | Anlam | Tipik neden | Çözüm |
|---|---|---|---|
| **421** | Decrypt fail | Private key yanlış / public key Meta'ya yüklenmedi / çift eşleşmiyor | [§4.2](./04-whatsapp-flow.md#42-rsa-anahtar-çifti) — `python -m scripts gen-keys` + `python -m scripts upload-key` |
| **421** + log `Password was given but private key is not encrypted` | `.env`'de `WA_FLOW_PRIVATE_KEY_PASSPHRASE` dolu ama anahtar passphrase'siz üretilmiş | `WA_FLOW_PRIVATE_KEY_PASSPHRASE=` (boş) yap → uvicorn restart |
| **427** | flow_token geçersiz | Token formatı bozuk; eski/expire session; HMAC fail (yoksa atla) | Kullanıcı CTA'ya yeniden dokunsun (yeni token oluşturulur) |
| **432** | Signature fail | `WA_APP_SECRET` yanlış (Flow endpoint imzası da app secret ile) | [§2.2](./02-meta-app.md#22-app-secret) |

## 7.5 Flow JSON publish

| Belirti | Olası neden | Çözüm |
|---|---|---|
| `INVALID_PROPERTY_TYPE` `max-length` | Eski sürümde int verilmiş | Mevcut kodda string `"200"` — `scripts/create_flow` ile flow'u yeniden yarat, `flow_id`'yi güncelle |
| `MISSING_REQUIRED_PROPERTY` `data_api_version` | Flow JSON üst seviyede `data_api_version` yok | Manifest'te `data_api_version: "4.0"` olduğundan emin ol (`app/channels/whatsapp/flow_manifest.py`) |
| `UNSUPPORTED_FLOW_JSON_VERSION` | `version` Meta'nın beklediği aralıkta değil | `wa_flow_json_version` ≥ "7.3" — config: `app/core/config.py` |
| `Validation errors` (CTA gönderiminde) | Flow yayınlanmamış (DRAFT) veya frozen | `scripts/create_flow` publish çıktısını kontrol et; WA Manager → Flows → status |
| `(#139000) Blocked by Integrity` (publish veya CTA gönderiminde) | WABA Business Verification'dan geçmemiş | Beklenen davranış. Test number'da DRAFT Flow yalnız **Flow Builder Preview** ile denenebilir; Cloud API üzerinden gönderim için BV şart ([§6.3](./06-tech-provider-onboarding.md#63-business-verification)) |

## 7.6 Flow runtime davranışı

| Belirti | Olası neden | Çözüm |
|---|---|---|
| CTA mesajı geldi ama tıklayınca açılmıyor | Public key Meta'da "Missing" görünüyor | [§4.2](./04-whatsapp-flow.md#42-rsa-anahtar-çifti) — `python -m scripts upload-key` yeniden çalıştır |
| Kullanıcı "Onayla"ya basıyor ama "✅ Randevunuz onaylandı" gelmiyor | nfm_reply webhook ngrok'a düşmüyor; `messages` field subscribe değil | [§3.3](./03-whatsapp-cloud-test.md#33-webhook-subscribe) kontrol et |
| Kullanıcı not yazıp slot dolduktan sonra geri dönünce not boş | Flow JSON eski sürüm — Form `init-values` yok | `python -m scripts create-flow` ile yeniden yarat ([§4.6.1](./04-whatsapp-flow.md#461-race-condition-slot)) |

## 7.7 Instagram

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Outbound `(#10) Application does not have permission` | Hedef kullanıcı 24h penceresi dışında veya hesap Personal | Önce kullanıcı sana DM atsın; IG hesabını Professional'a çevir ([§5 önkoşul](./05-instagram-test.md)) |
| Webhook hiç tetiklenmiyor | IG-via-Page (legacy) akışı denenmiş ama Page bağlı değil | [§5.1](./05-instagram-test.md#51-token--ig-id) — "Instagram business login" akışını kullan |
| Log `IG send HTTP 401/400 ... OAuth` + "token süresi dolmuş olabilir" | 60-gün long-lived token expire oldu | `python -m scripts ig-refresh-token <slug>` → yeni token'ı `.env`'e yaz, uvicorn restart ([§5.1](./05-instagram-test.md#51-token--ig-id)) |
| Quick Reply / persistent menu butonuna tıklamada bot cevap vermiyor | `messaging_postbacks` field subscribe edilmemiş | [§5.2](./05-instagram-test.md#52-webhook-subscribe) — webhook'a `messaging_postbacks`'i ekle |
| "Randevu Al" mesajı geliyor ama buton açılmıyor / "fallback telefon" metni geliyor | `business.contact.booking_url` boş veya placeholder | [§5.3](./05-instagram-test.md#53-db-seed-ig-id--booking_url) — seed'e gerçek URL koy, `python -m db.seed` |
| `python -m scripts ig-menu set ...` `(#100) Invalid parameter` | `composer_input_disabled`/locale yanlış veya `<IG_ID>` placeholder | Önce [§5.3](./05-instagram-test.md#53-db-seed-ig-id--booking_url)'ü tamamla; sonra menü kurulumunu çalıştır |
| Persistent menu güncellendi ama mevcut sohbette eski menü görünüyor | Menü güncellemesi anlık değil — yeni thread'lere uygulanır | Mevcut thread için: kullanıcı IG inbox'ında pull-to-refresh yapsın |
| Bot ana menüyü tekrar tekrar gönderiyor (loop) | Debounce kapatılmış veya `conversation.context.ig_last_menu_at` yazılmıyor | `MENU_DEBOUNCE_SECONDS` (`flow.py`) > 0 mı kontrol et; conversations koleksiyonunda alanı doğrula |

## 7.8 Embedded Signup (Tech Provider)

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Code → token swap 4xx | Code expire oldu (TTL **30 sn**) | Frontend → backend latency'yi düşür; cold start yok |
| `subscribed_apps` POST 4xx | Yanlış token tipi (sales SUT) veya WABA permission yok | Business token'ı `code → token` swap'tan al, app token kullanma |
| `register` POST `(#10000)` | PIN eksik/yanlış format (6 hane) | PIN'i E.164 olmayan 6 haneli sayı olarak yolla |
| Onboarding sayısı `10/7gün` limitine takıldı | Default TP limiti | Business Verification + App Review + Access Verification ile 200/7gün'e çık ([§6.5.6](./06-tech-provider-onboarding.md#656-onboarding-limitleri)) |

## 7.9 Genel teşhis

ngrok inspector: <http://127.0.0.1:4040> — gelen GET/POST'ları body'siyle, response status'ünü, headers'ı ile gösterir. Webhook hatalarında **ilk bakılacak yer**.

uvicorn loglarında aranacak pattern'lar:
- `Flow request decrypt başarısız` → §7.4 (421)
- `Geçersiz flow_token` → §7.4 (427)
- `Eşleşen business yok` → §7.3
- `Secret bulunamadı` → §7.3
- `İşletme bildirim hedefi` → §7.3
