# 01. Yerel Kurulum

Repoyu ilk klonladıktan sonra **bir kez** yapılır. Sonraki oturumlarda yalnız
§1.6 (uvicorn + ngrok) tekrarlanır.

## 1.1 Python venv + bağımlılıklar

Python 3.12+ gerekir. Ubuntu'da `venv`/`pip` ayrı paket olabilir (taze kurulumda
`python3 -m venv` "ensurepip is not available" verir) — önce onları kurun:

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip
```

```bash
cd ~/projects/randevumonline-chatbot
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn --version  # smoke check
```

> Sistem-genel `pip install` yapmayın. Aktivasyon istemezseniz `.venv/bin/python` doğrudan çalışır.
>
> **sudo yoksa** (yalnız apt erişimi olmayan ortam): pip'i venv içine elle
> bootstrap'layabilirsiniz —
> `python3 -m venv --without-pip .venv && curl -fsSL https://bootstrap.pypa.io/get-pip.py | .venv/bin/python`
> ardından yukarıdaki `pip install -r requirements.txt` aynen çalışır.

## 1.2 MongoDB 8.0 (WSL Ubuntu, native — Docker yok)

apt 8.0 resmi reposundan kurulur (sudo gerekir). `mongodb-org` metapaketi
`mongod` **ve** `mongosh`'u PATH'e koyar. Idempotent: kuruluysa atlar.
(Kurulum mantığı: `scripts/install_mongo.sh`.)

```bash
bash scripts/install_mongo.sh
```

WSL'de `systemd` çoğunlukla kapalı olduğundan MongoDB'yi ev dizinindeki veri
klasöründen elle başlatmak en sorunsuz yoldur. **Her oturumda:**

```bash
mongod --dbpath ~/data/db --fork --logpath ~/data/mongod.log   # başlat
mongosh --quiet --eval 'db.runCommand({ping:1})'               # doğrula → { ok: 1 }
mongod --dbpath ~/data/db --shutdown                           # durdur
```

> **systemd alternatifi (opsiyonel):** `/etc/wsl.conf` → `[boot] systemd=true`,
> PowerShell'de `wsl --shutdown`, sonra `sudo systemctl enable --now mongod` da
> çalışır. Bu yol veriyi `/var/lib/mongodb`'de tutar — yukarıdaki `--dbpath
> ~/data/db` yöntemiyle **karıştırma**, ikisi ayrı veritabanıdır.

## 1.3 ngrok

```bash
sudo snap install ngrok                          # veya https://ngrok.com/download
ngrok config add-authtoken <NGROK_AUTHTOKEN>     # https://dashboard.ngrok.com/get-started/your-authtoken
```

## 1.4 Groq API key (AI Müşteri Temsilcisi — opsiyonel)

Instagram ana menüsündeki **"Müşteri Temsilcisi"** butonu, Groq'un OpenAI-uyumlu
endpoint'iyle çalışan bir AI sohbeti açar (DB bilgilerinden yanıt; randevu için
web sitesine yönlendirir). Lokal Ollama gerekmez. Bu adım **opsiyoneldir** —
kapalıyken buton telefon numarasına düşer.

1. https://console.groq.com/keys → **Create API Key** → `gsk_...`'i kopyala.
2. `.env`'de (§1.5):

```bash
AI_ENABLED=true
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.3-70b-versatile   # daha hızlı: llama-3.1-8b-instant
```

> Detay ve test senaryosu: [docs/05-instagram-test.md §5.8](./05-instagram-test.md).
> `GROQ_BASE_URL` değiştirilerek Ollama gibi OpenAI-uyumlu yerel sağlayıcılar da bağlanabilir.

## 1.5 `.env` dosyası

### 1.5.1 İnteraktif sihirbaz (önerilen)

Her alan için ne işe yaradığını anlatan, link veren ve uygun olanları
otomatik üreten (verify token, RSA anahtarı) bir sihirbaz var:

```bash
.venv/bin/python -m scripts setup
```

- `python -m scripts setup --show` mevcut `.env`'i özet tablo olarak gösterir.
- `python -m scripts setup --section <ad>` tek bir bölümü tekrar çalıştırır (`mongo`, `verify`, `app_secret`, `flow_keys`, `ai`, `tenants`, `fastapi`).
- Tüm script'ler: `python -m scripts -h` ile yardım.
- Boş enter → mevcut değer korunur.
- Eski `.env` `/.env.bak` olarak yedeklenir.

### 1.5.2 Elle düzenleme

Sihirbazı atlamak isterseniz örneği kopyalayıp elle doldurun:

```bash
cp .env.example .env
```

İlk kurulumda doldurulacak ana değişkenler:

| Değişken | Kaynak | Ref |
|---|---|---|
| `MONGODB_URL` | `mongodb://localhost:27017` | §1.2 |
| `AI_ENABLED` + `GROQ_API_KEY` | Groq console (opsiyonel — IG müşteri temsilcisi) | §1.4 |
| `PUBLIC_BASE_URL` | ngrok forwarding URL'i | §1.6 |
| `WA_VERIFY_TOKEN` | `openssl rand -hex 16` | [§2.4](./02-meta-app.md#24-webhook-verify-token) |
| `IG_VERIFY_TOKEN` | `openssl rand -hex 16` | [§2.4](./02-meta-app.md#24-webhook-verify-token) |
| `WA_APP_SECRET` | Meta App Dashboard | [§2.2](./02-meta-app.md#22-app-secret) |
| `IG_APP_SECRET` | Aynı App Secret | [§2.2](./02-meta-app.md#22-app-secret) |
| `WA_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN` | Cloud API token | [§3.2](./03-whatsapp-cloud-test.md#32-temp-token) |
| `IG_BERBER_MEHMET_KUTAHYA_ACCESS_TOKEN` | IG Business Login | [§5.1](./05-instagram-test.md#51-token--ig-id) |
| `WA_FLOW_PRIVATE_KEY_PATH` | `secrets/flow_private.pem` | [§4.2](./04-whatsapp-flow.md#42-rsa-anahtar-çifti) |

> `app/core/db.py:get_secret()` `vault://wa/<slug>/access_token` referansını `WA_<SLUG>_ACCESS_TOKEN` env değişkenine map eder (büyük harfe, `/` → `_`).
>
> `.env` her değiştiğinde uvicorn'u Ctrl-C → yeniden başlatın (`--reload` env'i otomatik yenilemez).

## 1.6 Servisleri başlat (her oturum)

İki ayrı terminal:

```bash
# Terminal 1 — backend
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 — public tunnel
ngrok http 8000
# → Forwarding satırından: https://xxxx.ngrok-free.app
# → .env'deki PUBLIC_BASE_URL'i güncelleyip uvicorn'u yeniden başlat
```

- ngrok inspector: <http://127.0.0.1:4040> — gelen GET/POST'ları body'siyle gösterir.
- Free tier'da URL her restartta değişir — Meta UI'daki callback URL'lerini de güncellemeyi unutmayın.

## 1.7 İlk seed

```bash
.venv/bin/python -m db.seed
# → businesses=3, staff=7, services=26, customers=2, appointments=1, conversations=1
```

> Bu script DB'yi **sıfırlar** (test/dev için tasarlandı). Üretimde çalıştırmayın.

Seed 3 örnek işletme oluşturur:
- `berber_mehmet_kutahya` — basit kuaför, oda yok.
- `ayse_guzellik_kadikoy` — oda gerektiren hizmetler.
- `pati_dostu_cankaya` — veteriner, molalı mesai.

Kanal-özel placeholder ID'leri ([§3.5](./03-whatsapp-cloud-test.md#35-db-seedinde-phone-number-idyi-gerçek-değerle-değiştir) WA `phone_number_id`, [§5.3](./05-instagram-test.md#53-db-seed-ig-id--booking_url) IG `ig_user_id` + `booking_url`) kendi Meta hesabınızdan aldığınız gerçek değerlerle değiştirip seed'i yeniden çalıştıracaksınız.

---

**Sonraki:** [02. Meta App temelleri](./02-meta-app.md)
