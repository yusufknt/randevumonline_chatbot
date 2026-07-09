# Online Randevu Sistemi

> Kuaför / Güzellik salonu online randevu akışı, hizmet kataloğu, müşteri ekranları ve işletme ayarlarının referans dokümanı.

> **Kapsam ve veri kaynağı (önemli):** Bu doküman **web randevu ürününün** tasarım referansıdır. Aşağıdaki hizmet/fiyat/saat tabloları **örnektir**; sistemin gerçek verisi her zaman **veritabanından (DB)** gelir. Instagram/WhatsApp AI asistanı da bu dokümandaki rakamları DEĞİL, DB'deki canlı veriyi (`list_services`, `get_business_info` vb. tool'lar) kullanır — bkz. **[Bölüm 7: Mesajlaşma Kanalları ve AI Asistanı](#7-mesajlaşma-kanalları-ve-ai-asistanı)**.

---

## 1. Randevu Oluşturma Akışı

| Adım | İşlem | Açıklama |
|:----:|-------|----------|
| 1 | Telefon numarası | Müşteri telefon numarasını girer |
| 2 | SMS doğrulama | 6 haneli kod ile doğrulama yapılır |
| 3 | Ad Soyad | Müşteri kimlik bilgisi alınır |
| 4 | Yeni Randevu | Hizmet seçim ekranı açılır |
| 5 | Hizmet seçimi | Aşağıdaki kategorilerden seçim yapılır |
| 6 | Usta seçimi | Müsait personel listesi gösterilir |
| 7 | Tarih & saat | Seçilen ustanın müsait saatleri listelenir |
| 8 | Onay | Randevu özeti ve onay |

---

## 2. Hizmet Kataloğu

### 2.1 Saç Bakımı (8 hizmet)

| Hizmet | Ücret |
|--------|-------|
| Lazer Saç Kesimi | 500 TL |
| Normal Saç Kesimi | 600 TL |
| Düz Fön Çekimi | 250 TL |
| Kırık Fön Çekimi | 300 TL |
| Mikro Kaynak İşlemi | 40–100 TL / adet *(gram, renk ve kaliteye göre)* |
| Brezilya Fön (Kalıcı Düzlük) | 3.000–6.000 TL *(saç uzunluğu ve yoğunluğuna göre)* |
| Keratin Nem Bakım | 2.000 TL |
| Keratin Botoks | 2.500 TL |

### 2.2 Renklendirme (12 hizmet)

| Hizmet | Ücret |
|--------|-------|
| Dip Boya — Standart | 600 TL |
| Dip Boya — Qos | 900 TL |
| Dip Boya — İndola | 1.000 TL |
| Dip Boya — Schwarzkopf | 1.250 TL |
| Komple Boya | 1.000–7.500 TL |
| Dip Açma & Boyama (koruyucu iksirsiz) | 3.000 TL |
| Dip Açma & Boyama (koruyucu iksirli) | 4.000 TL |
| Komple Açma & Boyama | 3.000–7.500 TL |
| Ombre | 2.500–5.500 TL |
| Sombre | 2.000–3.500 TL |
| Brushlight / Freelight | 2.000–3.500 TL |
| Röfle | 2.000–5.500 TL |

**Cila İşlemi:** Saça doğallaştırma adına yapılan hızlı boyama işlemi. Ombre/Sombre işlemlerinde saça renk verme, canlandırma ve doğallık katma amacıyla uygulanır.

### 2.3 Saç Tasarımı (4 hizmet)

| Hizmet | Ücret |
|--------|-------|
| Günlük Maşa | 300 TL |
| Profesyonel Maşa | 500 TL |
| Yarım Topuz | 500 TL |
| Topuz | 750 TL |

### 2.4 Kirpik & Kaş (4 hizmet)

| Hizmet | Ücret |
|--------|-------|
| İpek Kirpik — Klasik | 750 TL |
| İpek Kirpik — Volume | 900 TL |
| İpek Kirpik — Mega Volume | 1.100 TL |
| Kirpik Lifting | 650 TL |
| Kaş Laminasyon | 650 TL |
| Kaş - Bıyık | — |

### 2.5 Tırnak Bakımı (5 hizmet)

| Hizmet | Ücret | Not |
|--------|-------|-----|
| Protez Tırnak | 1.000 TL | Kalıcı oje ve nail art **hediye** |
| Protez Tırnak Çıkarma | 300 TL | — |
| Kalıcı Oje | 650 TL | — |
| Manikür | 450 TL | — |
| Pedikür | 650 TL | — |

### 2.6 Makyaj (2 hizmet)

| Hizmet | Ücret |
|--------|-------|
| Günlük Makyaj | 1.000 TL |
| Günlük Makyaj (Kirpikli) | 1.500 TL |
| Profesyonel Makyaj | 2.500 TL |

### 2.7 Özel Günler (1 hizmet)

| Hizmet | Ücret | Kapsam |
|--------|-------|--------|
| Özel Gün Paketi | 3.500–7.500 TL | Nişan, söz, isteme gibi özel günler |

### 2.8 Gelin Paketleri (4 paket)

| Paket | Ücret | İçerik |
|-------|-------|--------|
| Tek Günlük (Standart) | 10.000 TL | Profesyonel saç + makyaj |
| İki Günlük (Standart) | 17.500 TL | Kına + düğün için saç + makyaj |
| Tek Günlük (Premium) | 12.000 TL | Saç, makyaj, kaş & bıyık, manikür, kalıcı oje, pedikür |
| İki Günlük (Premium) | 19.000 TL | Premium içerik + tüm vücut lazer epilasyon |

---

## 3. Usta Seçimi

Hizmet seçildikten sonra müsait personel listelenir:

- **Ayşe Yılmaz** — 45 dk
- **Mehmet Demir** — 45 dk
- **Zeynep Kaya** — 45 dk

Seçilen ustanın müsait günleri tablo halinde gösterilir; gün seçimi sonrası o günün boş saatleri veritabanından çekilir.

---

## 4. Randevu Onay Ekranı

```
Randevu Özetiniz
─────────────────
Personel             : Ayşe Yılmaz
Hizmet               : Lazer Saç Kesimi
Başlangıç            : Pazartesi, 11.05.2026 — 14:30
Tahmini Bitiş        : Pazartesi, 11.05.2026 — 15:15
Randevu Notu         : (isteğe bağlı)

[ RANDEVUYU ONAYLA ]
```

### Onay Sonrası Bildirim

> **Randevunuz Oluşturuldu!**
> Bir dahaki sefere çok daha hızlı! Uygulamayı ana ekranınıza ekleyerek bir sonraki randevunuzu **SMS kodu girmeden** saniyeler içinde oluşturabilirsiniz.

**Avantajlar:**
- SMS doğrulamasına gerek yok, anında giriş
- Randevu hatırlatmaları anlık bildirimle
- Uygulama gibi hızlı deneyim

---

## 5. Müşteri Ekranları

### 5.1 Mevcut Randevularım

| # | Randevu Tarihi | Hizmetler | Personel / Oda | İşlem |
|:-:|----------------|-----------|----------------|:-----:|
| 1 | 11.05.2026 14:30 | Lazer Saç Kesimi | Ayşe Yılmaz | İptal Et |

### 5.2 Geçmiş Randevularım

| # | Tarih | Hizmet | Personel / Oda | Durum |
|:-:|-------|--------|----------------|:-----:|
| 2 | 20.04.2026 15:00 | Lazer Saç Kesimi | Taha Yunus Demir | Tamamlandı |
| 1 | 07.04.2026 17:30 | Keratin Saç Bakımı | Taha Yunus Demir | Tamamlandı |

### 5.3 Kişisel Bilgilerim

| Alan | Açıklama |
|------|----------|
| **Ad Soyad** | Müşteri tam adı |
| **Doğum Günü** | Kutlama mesajı için kullanılır. KVKK uyumlu saklanır. |
| **Yıldönümü** | Evlilik yıldönümü kutlaması için kullanılır. KVKK uyumlu saklanır. |

---

## 6. Randevu Ayarları (İşletme)

### 6.1 Genel Ayarlar

| Ayar | Değer | Varsayılan |
|------|-------|:----------:|
| İşletme Saat Dilimi | İstanbul (UTC+3) | — |
| Takvim Renklendirme | Aktif / Pasif | — |
| Onay Sonrası Takvime Ekleme | Kapalı | Kapalı |
| Hatırlatma Mesaj Süresi (dk) | 60 | 60 |
| Online Randevu Alabilenler | Sadece Kayıtlı / Herkes / Hiç kimse | Hiç kimse |
| Online Randevu Modu | Standart / Vitrin | Standart |
| İptal Limiti (engelleme) | 3 | 5 |
| Gelmeme Limiti (engelleme) | 2 | 2 |
| Müşteri İptal Süresi (dk) | 60 | 60 |
| Maks. İleri Tarih (gün) | 45 | 30 |
| Online Takvim Periyodu (dk) | 30 | 15 |
| Yönetim Takvim Periyodu (dk) | 15 | 15 |

> **Online Randevu Modu:**
> - **Standart:** Önce doğrulama → hizmet ve personel seçimi
> - **Vitrin:** Önce menü/vitrin → tarih → en sonda doğrulama

> **Takvimde Kullanılacak Süre:**
> - **Seçtiğim slotlar:** Takvimde seçilen alan aynen korunur
> - **Ayarlarda belirlenen hizmet süresi:** Personel bazlı süre toplamı kadar bitiş hesaplanır

### 6.2 Çalışma Saatleri

| Gün | Açılış | Kapanış |
|-----|:------:|:-------:|
| Pazartesi | 00:00 | 23:59 |
| Salı | 09:00 | 21:30 |
| Çarşamba | 09:00 | 22:00 |
| Perşembe | 08:00 | 19:00 |
| Cuma | 08:00 | 22:00 |
| Cumartesi | 10:00 | 23:00 |
| Pazar | Kapalı | Kapalı |

### 6.3 Özel Gün & Tatil Yönetimi

- **Özel Gün Çalışma Saatleri:** Bayram veya özel günlerde farklı saat aralıkları tanımlanabilir.
- **Kapalı Günler:** İzin, tatil, hastalık, resmi tatil gibi tüm gün kapalı olunacak günler buradan yönetilir. Online randevu sayfasında kapatma nedeni görüntülenir.
- **Seanslı İşlemler:** İsteğe bağlı olarak etkinleştirilebilir.

---

## 7. Mesajlaşma Kanalları ve AI Asistanı

Yukarıdaki bölümler **web randevu ürününü** anlatır. Sistem ayrıca **Instagram** ve **WhatsApp** üzerinden, DB'deki canlı veriyle çalışan bir **AI Müşteri Temsilcisi** sunar. Bu kanalın davranışı web'den farklıdır.

### 7.1 Kanal Matrisi — Ne nerede yapılır?

| İşlem | Web Sitesi | Instagram / WhatsApp (AI) |
|-------|:----------:|:-------------------------:|
| Hizmet / fiyat / çalışma saati / adres bilgisi | ✓ | ✓ (DB'den) |
| Uygun (boş) randevu saatlerini öğrenme | ✓ | ✓ (bilgi amaçlı) |
| **Randevu oluşturma** | ✓ (SMS doğrulamalı) | ✗ → siteye yönlendirir |
| **Randevu listeleme** (mevcut/geçmiş/yaklaşan) | ✓ | ✗ → siteye yönlendirir |
| **Randevu iptal / değişiklik** | ✓ | ✗ → siteye yönlendirir |
| Yetkiliye/personele aktarma | — | ✓ (escalation + telefon) |

> **Temel kural:** Instagram/WhatsApp kanalı **bilgilendirme + yönlendirme** içindir. Randevu **oluşturma, listeleme ve iptal işlemleri web'de** (`booking_url`) yapılır. DM'de müşterinin kimliği doğrulanamadığından randevu listelemek hem güvensiz hem yanıltıcı olur; bu nedenle bilinçli olarak kapatılmıştır.

### 7.2 AI Müşteri Temsilcisi Akışı

Konuşma durumları (`conversations.state`):

- **`greeting`** — Varsayılan menü akışı. Hızlı yanıt butonları: **Randevu Al · Hizmetler · Bilgi Al · Müşteri Temsilcisi**.
- **`ai_active`** — "Müşteri Temsilcisi"ne basınca açılan AI sohbeti. Serbest metinler Groq tabanlı asistana gider.
- **`human_handoff`** — Gerçek personele aktarıldı; bot sessize geçer.

Asistan sohbetin başında **otomatik olduğunu ifşa eder** (Meta politikası) ve personele ulaşmak için işletme telefonunu ayrı bir mesaj olarak paylaşır.

### 7.3 AI'nın Kullandığı Veri (salt-okunur tool'lar)

Asistan **hiçbir bilgiyi uydurmaz**; her somut veri DB'den, şu tool'larla gelir:

| Soru | Tool | Kaynak |
|------|------|--------|
| Hizmet / fiyat | `list_services` | `services` |
| Adres, saat, telefon, WhatsApp, e-posta, `booking_url` | `get_business_info` | `businesses` |
| Personel | `list_staff` | `staff` |
| Uygun saatler | `list_available_slots`, `list_staff_available_at` | hesaplanan müsaitlik |
| Yetkiliye aktarma | `escalate_to_human` | — |

> `create_appointment`, `cancel_appointment` ve `get_customer_appointments` bu kanalda **bilinçli olarak yer almaz** (bkz. 7.1).

### 7.4 Randevu / İptal Talepleri

Müşteri "randevum ne zaman", "randevumu iptal et", "yaklaşan randevum" gibi bir şey sorduğunda asistan **liste/tarih vermez**; randevularını **online sayfadan görüntüleyip iptal/değişiklik** yapabileceğini söyler ve `booking_url`'i paylaşır. Gerekirse `escalate_to_human` ile yetkiliye aktarır.

### 7.5 AI Ayarları (`businesses.ai_settings`)

6.1'deki işletme ayarlarına ek olarak, AI davranışını yöneten alanlar:

| Alan | Açıklama |
|------|----------|
| `persona` | Asistanın ses tonu / karakteri |
| `welcome_message` | "Müşteri Temsilcisi" karşılaması (randevu sorusu sormaz, genel karşılar) |
| `ai_disclosure` | Otomatik asistan ifşa cümlesi (`""` ile kapatılabilir) |
| `fallback_message` | Asistan yanıt veremezse gösterilecek metin |
| `quiet_hours` + `quiet_hours_message` | Sessiz saatler; bu aralıkta otomatik yanıt verilmez |
| `max_advance_days` | Müsaitlik için en fazla kaç gün ileri konuşulacağı |
| `booking_buffer_minutes`, `online_slot_step_minutes` | Müsaitlik hesabını etkiler |

### 7.6 Kanal Notları

- **Düz metin:** Instagram/WhatsApp DM markdown render etmez. Asistan **kalın/italik/`[metin](link)`** kullanmaz; bağlantı ve numaraları açık yazar.
- **Veri kaynağı:** Bu dokümandaki hizmet/fiyat/saat tabloları örnektir. Canlı değerler **her zaman DB'den** gelir; doc ile DB çelişirse **DB esastır**.
