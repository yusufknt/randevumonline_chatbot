# Veritabanı Şeması

MongoDB üzerinde 6 koleksiyon. Tüm sorgular `business_id` ile filtrelenir (multi-tenant).

## Dosyalar

- `models.py` — Pydantic v2 modelleri (tip referansı; runtime'da instantiate edilmiyor, DB raw dict).
- `seed.py` — 3 örnek işletme + örnek müşteri/randevu/sohbet yükler, indeksleri kurar.

## Koleksiyonlar

| Koleksiyon | Amaç |
|---|---|
| `businesses` | Firma kimliği, sahibi, çalışma saatleri, kanal config (WA/IG), AI ayarları, abonelik |
| `staff` | Personel. Kendi çalışma saatleri ve verebildiği hizmetler |
| `services` | Hizmetler (süre, fiyat, hangi personeller verebilir, oda gerekir mi) |
| `customers` | WA `wa_id` veya IG `user_id` ile eşleşir; işletme bazında ayrı tutulur |
| `appointments` | Randevular (UTC saatlerle), durum, kaynak kanal, sohbet referansı |
| `conversations` | Sohbet logu + state + working memory (`context`); (işletme, kanal, thread) için tek doküman |

## Tasarım kararları

**Multi-tenant:** Tüm dokümanlarda `business_id` ana ayırıcı. Bileşik indekslerin ilk alanı her zaman `business_id`.

**Para:** `Decimal128` (float kullanmayın). `seed.py:_d()` yardımcısı dönüştürür. Aralıklı fiyatlar için `price` + opsiyonel `price_max` (`docs/sistem.md §2`).

**Saat dilimi:** `start_time` / `end_time` UTC. İşletme saatleri lokal `HH:MM`; `business.timezone` (`Europe/Istanbul`) ile çevrilir.

**Secret'lar:** WA/IG `access_token` doğrudan tutulmaz; `vault://...` referansı. PoC'de env'den okunur (`app/core/db.py:get_secret`).

**Müşteri eşleştirme:**
- WhatsApp: `wa_id` (E.164'siz, "905...").
- Instagram: Graph API `sender.id` (PSID).
- Aynı kişi WA ve IG'den ayrı kayıt; istenirse merge mantığı eklenebilir.

## Önerilen indeksler

`seed.py:ensure_indexes()` ve `app/core/db.py:init_indexes()` aynı seti kurar:

```
businesses    : business_id (unique), business_type,
                contact.whatsapp_number (unique sparse),
                channels.whatsapp.phone_number_id (sparse),
                channels.instagram.ig_user_id (sparse)
staff         : (business_id, is_active)
services      : (business_id, is_active),
                (business_id, category)
customers     : (business_id, whatsapp_id) unique sparse,
                (business_id, instagram_user_id) unique sparse,
                (business_id, phone),
                (business_id, is_blocked)
appointments  : (business_id, staff_id, start_time),
                (business_id, status, start_time),
                (customer_id, start_time),
                (status, start_time)            # hatırlatma cron'u
conversations : (business_id, channel, channel_thread_id) unique,
                (business_id, state, last_active_at)
```

`appointments`'a TTL **koymayın** — geçmiş kayıt KVKK için saklanır.

## Çalıştırma

```bash
.venv/bin/python -m db.seed
```

> Bu script DB'yi **sıfırlar** (test/dev için). Üretimde çalıştırmayın. Mongo kurulumu: `docs/01-yerel-kurulum.md §1.2`.
