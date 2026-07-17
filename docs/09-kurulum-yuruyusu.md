# 09. Sıfırdan Kurulum — Sıralı Yürüyüş

> Happy-path checklist: **ne yapılır, hangi sırayla, hangi komut**. Komutların
> *neden*'i, edge-case'leri ve tüm varyantları numaralı dökümanlarda — her adım
> ilgili §'ye link verir. Tek konuyu derinlemesine okumak istersen doğrudan o
> dökümana git: [00-index](./00-index.md).

İlk kurulum ~30 dk. Yarısı browser'da (Meta App Dashboard), yarısı terminalde.

**Sözlük:**
- `.env` = aktif değişkenler (uvicorn bunu okur).
- `.env.example` = şablon (sürüm kontrolünde; `setup_env` baz alır).
- `.env.bak` = `setup_env`'in otomatik yedeği. Test ettikten sonra silmen güvenli.

---

## A. Önkoşullar (terminalde, bir kez)

Detaylar + systemd varyantı: [§1.1](./01-yerel-kurulum.md#11-python-venv--bağımlılıklar) · [§1.2](./01-yerel-kurulum.md#12-mongodb-80-wsl-ubuntu-native--docker-yok) · [§1.3](./01-yerel-kurulum.md#13-ngrok).

```bash
cd ~/projects/randevumonline-chatbot
sudo apt install -y python3-venv python3-pip          # taze Ubuntu'da gerekir
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

bash scripts/install_mongo.sh                          # MongoDB 8.0 apt'den kur (mongod + mongosh, bir kez)
mongod --dbpath ~/data/db --fork --logpath ~/data/mongod.log   # başlat (her oturum)
mongosh --quiet --eval 'db.runCommand({ping:1})'       # doğrula → { ok: 1 }

sudo snap install ngrok
ngrok config add-authtoken <AUTH_TOKEN>                # dashboard.ngrok.com/get-started/your-authtoken
```

> **Tuzak:** `uvicorn` PATH'te değildir — venv aktive olsa bile her zaman `.venv/bin/uvicorn`.

---

## B. `.env` doldur (interaktif sihirbaz)

Sihirbazın ne sorduğu ve her alanın anlamı: [§1.5](./01-yerel-kurulum.md#15-env-dosyası).

```bash
.venv/bin/python -m scripts setup
```

7 bölüm sıralı — bu yürüyüşte ne cevaplanmalı:

| # | Bölüm | Yanıt |
|---|---|---|
| 1 | MongoDB | Enter (default) |
| 2 | LLM | **1** (Groq) → model Enter → Groq API key yapıştır ([§1.4](./01-yerel-kurulum.md#14-groq-api-key-ai-müşteri-temsilcisi--opsiyonel)) |
| 3 | Verify token'lar | **Y** (otomatik üret) |
| 4 | App Secret | C.2'de doldur, şimdilik boş Enter |
| 5 | RSA anahtarları | **Y** (üret) → passphrase Enter |
| 6 | Tenant token'ları | **n** (D.1'de döneceğiz) |
| 7 | PUBLIC_BASE_URL | D.3'te güncelleyeceğiz, default Enter |

Sonunda **"Bu değerlerle .env yazılsın mı?"** → **Y**. Özet için: `.venv/bin/python -m scripts setup --show`.

---

## C. Meta App tarafı (browser'da)

App-seviyesi ortak ayarların tamamı: [§02](./02-meta-app.md). WA test number detayı: [§03](./03-whatsapp-cloud-test.md).

| Adım | Yapılacak |
|---|---|
| **C.1** App Roles | Sol menü → **App roles** → Administrator olduğunu doğrula ([§2.1](./02-meta-app.md#21-app-roles)) |
| **C.2** App Secret | **App settings → Basic → App secret → Show** → kopyala → `setup --section app_secret` → yapıştır → Y ([§2.2](./02-meta-app.md#22-app-secret)) |
| **C.3** WA test number | **WhatsApp → Step 1. Try it out** → not al: **Phone Number ID**, **WABA ID**, **Generate token** (24h `EAA…`) ([§3.1](./03-whatsapp-cloud-test.md#31-test-number--phone-number-id)) |
| **C.4** Recipient doğrula | Aynı sayfa → **Recipient → Manage phone number list → + Add** → kendi WA numaran → 6 haneli kod ([§3.4](./03-whatsapp-cloud-test.md#34-recipient-ekle-5-limitli)) |
| **C.5** Webhook subscribe | **Step 2 → Configure Webhooks** — D.3 sonrası yapılacak (D.4'e bak) |

> **Step 2'deki "Register" / "Add payment" / "Test registered number" butonlarına DOKUNMA** — yalnız gerçek production numarası için.

---

## D. Backend + tunnel + DB seed

### D.1 Tenant access token'ı

> **Önce ngrok'u başlat, sonra token al** — temp token sayfa yenilenince kaybolur (Meta UI) ve 24 saatte expire. Detay: [§3.2](./03-whatsapp-cloud-test.md#32-temp-token).

```bash
.venv/bin/python -m scripts setup --section tenants
```

Berber için **y**, WA token C.3'tekini yapıştır, IG boş, diğer iki tenant **n**.

### D.2 Seed kişiselleştir + yükle

`db/seed.py` → **Berber Mehmet** bloğunda `channels.whatsapp.phone_number_id`'yi C.3'teki gerçek değerle değiştir ([§3.5](./03-whatsapp-cloud-test.md#35-db-seedinde-phone-number-idyi-gerçek-değerle-değiştir)). Sonra:

```bash
.venv/bin/python -m db.seed       # → businesses=3, staff=7, services=26, customers=2, appointments=1, conversations=1
```

> Seed DB'yi **sıfırlar** (test/dev). Kanal-özel alanlar: WA → [§3.5](./03-whatsapp-cloud-test.md#35-db-seedinde-phone-number-idyi-gerçek-değerle-değiştir), IG → [§5.3](./05-instagram-test.md#53-db-seed-ig-id--booking_url).

### D.3 Backend + ngrok başlat

```bash
# Terminal 1
.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Terminal 2
ngrok http 8000                   # → Forwarding: https://abc12def.ngrok-free.app
# Terminal 3
.venv/bin/python -m scripts setup --section fastapi   # yeni ngrok URL'i → Y
```

Sonra **Terminal 1 → Ctrl-C → tekrar başlat** (`--reload` env değişikliğini otomatik almaz). Beklenen startup logu ve detay: [§1.6](./01-yerel-kurulum.md#16-servisleri-başlat-her-oturum).

### D.4 Webhook'u Meta'da subscribe (C.5'e dön)

**WhatsApp → Configure Webhooks** ([§3.3](./03-whatsapp-cloud-test.md#33-webhook-subscribe)):
- **Callback URL:** `<PUBLIC_BASE_URL>/webhooks/whatsapp`
- **Verify token:** `.env`'deki `WA_VERIFY_TOKEN`
- **Verify and save** → yeşil tik → **`messages`** field → Subscribe.

Tüm endpoint URL'leri: [§00 — Endpoint haritası](./00-index.md#endpoint-haritası). ngrok inspector ile canlı izle: <http://127.0.0.1:4040>.

### D.5 İlk smoke test (Flow olmadan)

Telefondan test number'a "merhaba" yaz. **Beklenen:** uvicorn `flow_not_configured` warning'i + fallback metni — DB'de `flow_id` yok henüz; E adımı bunu kuracak.

---

## E. WhatsApp Flow

Mimari + RSA + publish detayları: [§04](./04-whatsapp-flow.md). **Yeni hesap / Business Verification yoksa Yol 2'yi (Preview) kullan** — Yol 1 `Blocked by Integrity` ile takılır.

### Yol 1 — Publish (üretim, BV gerekli)

```bash
.venv/bin/python -m scripts onboard   # PHONE_NUMBER_ID / WABA_ID / ACCESS_TOKEN sorar, PUBLIC_BASE_URL Enter
```

Zincir (otomatik): RSA → public key upload → WABA subscribe → Flow create+publish → `flow_id` Mongo'ya yazılır. Sonradan elle güncelleme: `set-flow-id <slug> <FLOW_ID>`. Publish hataları: [§7.5](./07-hata-kilavuzu.md#75-flow-json-publish).

### Yol 2 — Flow Builder Preview (BV olmadan test, telefon gerektirmez)

Test numarasında Cloud API CTA `(#139000) Blocked by Integrity` ile reddedilirse, Flow JSON'ı Flow Builder UI'da **Preview Interactive mode** ile uçtan uca test et. Endpoint encrypt/decrypt + manifest + business logic gerçekten çalışır; telefona mesaj gitmez. Adım adım: [§4.3.2](./04-whatsapp-flow.md#432-draft-mode-business-verification-olmadan-test).

> `WA_FLOW_MODE=draft` BV'siz CTA göndermeyi **sağlamaz**; yalnız BV var ama henüz publish edilmemiş durum içindir.

---

## F. Test

Telefondan test number'a "merhaba" yaz → bot CTA mesajı ("…`[Randevu Al]`") → CTA'ya dokun → 6 ekran (Ad+Soyad · Hizmet · Personel · Gün · Saat · Onay) → "✅ Randevunuz onaylandı" özeti.

```
Flow endpoint action=data_exchange screen=AD_SOYAD … screen=CONFIRM
[whatsapp → 9054...] ✅ Randevunuz onaylandı....
```

Mongo'da doğrula:
```bash
echo 'db.appointments.find().sort({created_at:-1}).limit(1).pretty()' | mongosh randevum_chatbot
```

---

## G. En sık hatalar

Tam tablo: [07. Hata kılavuzu](./07-hata-kilavuzu.md).

| Belirti | Çözüm |
|---|---|
| `uvicorn: command not found` | `.venv/bin/uvicorn` ile çağır |
| `ServerSelectionTimeoutError: localhost:27017` | MongoDB çalışmıyor — `mongod --dbpath ~/data/db --fork --logpath ~/data/mongod.log` |
| `Webhook 403 Verify and save` | `.env` verify token = Meta UI birebir mi? uvicorn restart? ([§7.1](./07-hata-kilavuzu.md#71-webhook-subscription)) |
| `flow_not_configured` warning | `onboard` çalıştır veya Yol 2 ile test et ([§7.3](./07-hata-kilavuzu.md#73-whatsapp-orchestrator-kod-tarafı)) |
| `(#139000) Blocked by Integrity` | BV yok — E Yol 2 (Preview) |

---

## H. Sonraki açılış (aynı makine)

WSL oturumunda MongoDB otomatik başlamaz. Sırayla:

```bash
mongod --dbpath ~/data/db --fork --logpath ~/data/mongod.log   # 1) DB
.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000   # 2) T1
ngrok http 8000                                                 # 3) T2
```

ngrok URL değiştiyse: `setup --section fastapi` + uvicorn restart + Meta UI'daki Callback URL'i güncelle. Temp token 24h dolduysa: WhatsApp → Generate token + `setup --section tenants`. Detay: [§1.6](./01-yerel-kurulum.md#16-servisleri-başlat-her-oturum).

---

## I. Üretime geçiş

1. **Business Verification** — Meta Business Suite → Settings, 3-5 iş günü ([§6.3](./06-tech-provider-onboarding.md#63-business-verification)).
2. BV onaylanınca `WA_FLOW_MODE`'u `.env`'den kaldır → `onboard` ile publish.
3. Çoklu firma → Embedded Signup ([§06](./06-tech-provider-onboarding.md)).
4. Üretim domain (Caddy + Let's Encrypt) → ngrok'tan sabit domain'e geç; `PUBLIC_BASE_URL` + Meta callback URL'leri güncelle.

---

**Toplam:** ~30 dk + BV beklenirken Yol 2 ile geliştirme. BV onaylanınca ~5 dk'da üretime geç.
