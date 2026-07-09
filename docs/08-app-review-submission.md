# 08. App Review Submission — Adım Adım Form Rehberi

Bu döküman Meta App Dashboard → **Submit for App Review** ekranındaki
formun her bir bölümünün **RandevumOnline TP başvurusu** (App: `<APP_NAME>`,
App ID `<APP_ID>`) için nasıl doldurulacağını anlatır. Üst
düzey strateji [§6.4](./06-tech-provider-onboarding.md#64-app-review-tech-provider-için)
de; bu döküman alan-alan ne yazılacağını + hangi video'nun nereye
yükleneceğini gösterir.

> **Kapsam:** Burada yalnız **WhatsApp** izinleri (`whatsapp_business_messaging`,
> `whatsapp_business_management`) detaylandırılır — fotoğraflardaki ekranların
> birebir karşılığı. **Instagram** izinleri (`instagram_business_basic`,
> `instagram_business_manage_messages` ve legacy seti) için aynı form pattern'i
> geçerlidir; izin listesi ve use case açıklaması için
> [§6.4](./06-tech-provider-onboarding.md#zorunlu-izinler) tablosuna bakın.

> **Önkoşul:**
> - App **Live** mode, App type: **Business** ([§2.3](./02-meta-app.md#23-app-mode))
> - Business Verification ✅ ([§6.3](./06-tech-provider-onboarding.md#63-business-verification))
> - Privacy Policy + Terms of Service + Data Deletion callback URL'leri
>   yayında ([§2.6](./02-meta-app.md#26-app-dashboard--settings--basic--diğer-alanlar))
>
> **Meta:** [App Review — Tech Providers](./Developers%20Facebook%20Documentation/output/fb-whatsapp-business-platform/documentation__business-messaging__whatsapp__solution-providers__app-review.md)

## 8.1 Submit for App Review — ana ekran

Sol sütundaki üç checklist sırayla **yeşil** olmadan **Submit for
review** butonu aktifleşmez:

| # | Bölüm | İçerik | Detay |
|---|---|---|---|
| 1 | **Verification** | Business Verification ✅ (önceden tamamlanır) | [§6.3](./06-tech-provider-onboarding.md#63-business-verification) |
| 2 | **App settings** | App name, contact email, icon, category, Privacy Policy URL, Data Deletion URL | [§2.6](./02-meta-app.md#26-app-dashboard--settings--basic--diğer-alanlar) |
| 3 | **Allowed usage** | İki izin için ayrı ayrı — aşağıda [§8.2](#82-allowed-usage) | — |
| 4 | **Data handling** | Processor/responsible/government-request soruları — [§8.3](#83-data-handling) | — |

> Üstteki **"Some things to remember"** (Unutulmaması gerekenler)
> kutusunda Meta'nın hatırlattığı: *"Providing incomplete or vague
> answers may result in loss of platform access."*
> → **TR:** *"Eksik veya muğlak yanıt vermek platform erişiminin
> kaybedilmesine yol açabilir."* Alanları boş bırakma, jenerik şablon
> yapıştırma.

## 8.2 Allowed usage

Her iki izin için **dört alt adım** var; ikisi de aynı şablon:

1. **Describe how your app uses this permission or feature**
   → *"Uygulamanızın bu izni veya özelliği nasıl kullandığını
   açıklayın."* — düz metin alanı.
2. **Upload screencast showing the end-to-end user experience**
   → *"Uçtan uca kullanıcı deneyimini gösteren ekran kaydını
   yükleyin."* — video.
3. **Zorunlu API testi isteklerini gerçekleştirdiğinizden emin olun**
   (zaten TR) — Graph API call log'u 24 saat içinde otomatik dolar.
4. **Agree that you will comply with allowed usage**
   → *"İzin verilen kullanıma uyacağınızı kabul edin."* — checkbox.

### 8.2.1 `whatsapp_business_messaging`

Meta'nın resmi tanımı (Usage guidelines pop-up'ından):

> The whatsapp_business_messaging permission allows an app to send
> WhatsApp messages to a specific phone number, upload and retrieve
> media from messages, manage and get WhatsApp business profile
> information, and to register those phone numbers with Meta.

**TR çeviri:** *"whatsapp_business_messaging izni; bir uygulamanın
belirli bir telefon numarasına WhatsApp mesajı göndermesine, mesajlardan
medya yüklemesine/almasına, WhatsApp Business profil bilgilerini
yönetmesine ve almasına, ve bu telefon numaralarını Meta'ya kaydetmesine
olanak tanır."*

**"Describe how your app uses this permission" alanına yaz**
*(Uygulamanızın bu izni nasıl kullandığını açıklayın)***:**

```
RandevumOnline is a SaaS platform that lets local service businesses
(barbershops, beauty salons, dental clinics, auto-service shops) take
appointments through WhatsApp. Each tenant business connects its own
WhatsApp Business phone number via Embedded Signup. Our app uses
whatsapp_business_messaging to:

1. Send appointment-confirmation, reminder and reschedule messages
   from the tenant's WABA to the end customer's WhatsApp number,
2. Receive customer replies through webhooks and respond with a
   guided WhatsApp Flow (service selection → staff → slot → confirm),
3. Upload media (e.g. clinic location image, price-list PDF) returned
   to the customer on request,
4. Register tenant phone numbers with the Cloud API after Embedded
   Signup completes.

All messages are initiated by either the customer (24h service
window) or the business (using pre-approved utility templates for
reminders).
```

**Business Description** *(İşletme Açıklaması — tek satır)***:**

```
We are a SaaS appointment platform that enables local service
businesses to receive bookings via WhatsApp.
```

**TR karşılığı (sadece anlamak için, forma İngilizce gir):**
*"Yerel hizmet işletmelerinin WhatsApp üzerinden randevu almasını
sağlayan bir SaaS randevu platformuyuz."*

**Video gereksinimi** — fotoğraf 1'deki *"Record a video of sending
a message through the WhatsApp Cloud API"* (→ *"WhatsApp Cloud API
üzerinden mesaj gönderdiğinizi gösteren bir video kaydedin"*) pop-up:

- Kendi telefonunuza **Try it out** aracından test mesajı gönderin.
- Veya `curl` komutunu randevumonline.com paneline embed edip
  "Mesaj gönder" butonuna basın.
- Kayıt **iki tarafı** birden göstermeli: app'in mesajı gönderdiği
  ekran + WhatsApp client'ın (web ya da mobil) aynı mesajı aldığı
  ekran.
- Screen recording veya kamera kaydı kabul.

### 8.2.2 `whatsapp_business_management`

Meta'nın resmi tanımı:

> The whatsapp_business_management permission allows your app to
> read and/or manage WhatsApp business assets you own or have been
> granted access to by other businesses through this permission.
> These business assets include WhatsApp business accounts, phone
> numbers, message templates, QR codes and their associated messages,
> and webhook subscriptions.

**TR çeviri:** *"whatsapp_business_management izni; uygulamanızın,
sahip olduğunuz ya da bu izin yoluyla diğer işletmelerin size erişim
verdiği WhatsApp Business varlıklarını okumasına ve/veya yönetmesine
olanak tanır. Bu varlıklar; WhatsApp Business hesaplarını, telefon
numaralarını, mesaj şablonlarını, QR kodlarını ve bunlara bağlı
mesajları, ve webhook aboneliklerini içerir."*

**"Describe how your app uses this permission" alanına yaz**
*(Bu izni nasıl kullandığınızı açıklayın)***:**

```
RandevumOnline uses whatsapp_business_management to onboard tenant
businesses and manage the WhatsApp assets they grant us through
Embedded Signup. Specifically:

1. After Embedded Signup, we call /<WABA_ID>/subscribed_apps to
   subscribe the tenant's WABA to our webhook,
2. We create and update message templates (appointment_reminder_v1,
   appointment_confirmation_v1, reschedule_request_v1) for the
   tenant's reminder/confirmation flows,
3. We read business profile fields (display name, vertical,
   description) to render the tenant dashboard,
4. We subscribe to account_update, message_template_status_update
   and phone_number_quality_update webhooks for tenant lifecycle
   events.

We do not request analytics insights and do not use this permission
for advertising.
```

**Video gereksinimi** — fotoğraf 2'deki *"Instructions to make API
test calls and record a video of creating a WhatsApp message
template"* (→ *"API test çağrıları yapma ve WhatsApp mesaj şablonu
oluşturduğunuz bir video kaydetme talimatları"*) pop-up:

1. **Postman collection** — Meta'nın yayınladığı koleksiyonu çalıştır.
   Test data başvuru formunda görünmesi **24 saat** sürebilir.
2. **Template oluşturma videosu** — WhatsApp Manager → Templates →
   Create template → kategori seç → form doldur → Submit. Tüm bu
   adımları screen recording'e al.
3. **Her iki video da App Review submission'a ayrı dosya** olarak
   eklenir.

> Tek video'da iki izni birden gösterme — Meta otomatik reject ediyor
> ([§6.4 Submission kuralları](./06-tech-provider-onboarding.md#submission-kuralları)).
> Reviewer için randevumonline.com paneline test user hesabı da aynı
> bölümde.

## 8.3 Data handling

Bu bölümdeki sorular Meta'nın **Platform Data**'sı için sorulan
GDPR + ulusal güvenlik sorularıdır. "Platform Data" = Meta'dan API
ile aldığınız her şey (Meta user ID, e-posta, profil resmi, access
token, app secret). Telefon numarası + DM içeriği de buna dahil.

### 8.3.1 `processor-0` — Data processors / service providers (Veri işleyiciler / hizmet sağlayıcılar)

> Do you have data processors or service providers, including your
> own companies, that will have access to the Platform Data that
> you obtain from Meta?

**TR:** *"Meta'dan edindiğiniz Platform Verilerine erişimi olacak;
kendi şirketleriniz de dahil, veri işleyicileriniz veya hizmet
sağlayıcılarınız var mı?"*

**Yanıt:** Üçüncü taraf işleyici varsa **Yes (Evet)** → liste; yoksa
**No (Hayır)**.

RandevumOnline'da kullanıldığı bilinen sub-processor'lar:

| Sağlayıcı | Rol | Platform Data görür mü? |
|---|---|---|
| MongoDB Atlas | Veritabanı (tenant + appointment) | ✅ — DM içerikleri + tenant token'lar |
| Netgsm | SMS fallback | ❌ — sadece müşterinin kendi numarası, Meta'dan gelmiyor |
| Vault provider (HashiCorp / GCP Secret Manager) | Token storage | ✅ — business_token, app_secret |
| Cloud host (örn. Hetzner / GCP) | Sunucu | ✅ — tüm trafik geçiyor |

**Yes** → her birinin **legal entity adı** + ülkesi + neye eriştiği.

### 8.3.2 `responsible-1` — Data controller (Veri sorumlusu)

> Who is the person or entity that will be responsible for all
> Platform Data Meta shares with you?

**TR:** *"Meta'nın sizinle paylaştığı tüm Platform Verilerinden
sorumlu olacak kişi veya tüzel kişi kimdir?"* (KVKK terminolojisinde
**veri sorumlusu / data controller**.)

**Yanıt (tek satır şirket / kişi):**

```
DemiraySoft Yazılım — Kütahya Tasarım Teknokent, Türkiye.
Authorized representative: Taha Yunus Demir (founder),
contact: tahayunusdemir@gmail.com.
```

### 8.3.3 `responsible-2` — Country (Ülke)

> Select the country where this person or entity is located.

**TR:** *"Bu kişinin veya tüzel kişinin bulunduğu ülkeyi seçin."*

**Yanıt:** **Türkiye / Turkey**.

### 8.3.4 `requests-3` — National security requests / Ulusal güvenlik talepleri (son 12 ay)

> Have you provided the personal data or personal information of
> users to public authorities in response to national security
> requests in the past 12 months? *(criminal investigations / mahkeme
> kararları dahil değil)*

**TR:** *"Son 12 ay içinde, ulusal güvenlik talepleri kapsamında
kamu makamlarına kullanıcıların kişisel verilerini ya da kişisel
bilgilerini sağladınız mı? Bu soru, cezai soruşturmalarla ilgili arama
emri veya mahkeme kararı taleplerini kapsamaz."*

Seçenekler ve Türkçe karşılıkları:

| Seçenek (form) | Türkçe karşılığı |
|---|---|
| **No** | **Hayır** ← yeni başvuran TP için doğru cevap |
| Yes, ~10 or fewer users | Evet, yaklaşık 10 veya daha az kullanıcı |
| Yes, 11–100 users | Evet, 11–100 kullanıcı |
| Yes, 101–1,000 users | Evet, 101–1.000 kullanıcı |
| Yes, more than 1,000 users | Evet, 1.000'den fazla kullanıcı |
| We are prohibited by law or company policy from answering | Yasa veya şirket politikası gereği bu soruyu yanıtlamamız yasak |

Daha önce hiçbir devlet talebine veri paylaşılmadıysa **No**. KVKK /
5237 sayılı TCK çerçevesinde gelen savcılık/mahkeme talepleri ulusal
güvenlik kapsamında değil — onlar criminal investigation, soru kapsam
dışı.

### 8.3.5 `requests-4` — Politika ve süreçler

> Which of the following policies or processes do you have in place
> regarding requests from public authorities for the personal data
> or personal information of users? Check all that apply.

**TR:** *"Kamu makamlarından gelen, kullanıcıların kişisel verisi /
kişisel bilgisi taleplerine ilişkin aşağıdaki politika ya da
süreçlerden hangileri sizde mevcut? Uygun olanların hepsini işaretleyin."*

Seçilmesi önerilen (mümkün olan tümü) — Türkçe karşılıklarıyla:

| Seçenek (form) | Türkçe karşılığı |
|---|---|
| ☑ Required review of the legality of these requests. | Bu taleplerin hukuka uygunluğunun zorunlu olarak incelenmesi. |
| ☑ Provisions for challenging these requests if they are considered unlawful. | Hukuka aykırı bulunan talepleri itiraz/dava yoluyla reddetmeye yönelik hükümler. |
| ☑ Data minimization policy — the ability to disclose the minimum information necessary. | Veri minimizasyonu politikası — yalnız zorunlu olan asgari bilgiyi paylaşma yeteneği. |
| ☑ Documentation of these requests, including your responses to the requests and the legal reasoning and actors involved. | Bu taleplerin; yanıtlarınızın, hukuki gerekçenin ve dahil olan tarafların kayıt altına alınması. |
| ☐ None of the above. | Yukarıdakilerin hiçbiri. |
| ☐ We are prohibited by law or company policy from answering this question. | Yasa veya şirket politikası gereği bu soruyu yanıtlamamız yasak. |

> Boş bırakma veya **None of the above** (Hiçbiri) seçme — review'da
> kırmızı bayrak. En azından "legality review" (hukuka uygunluk
> incelemesi) + "data minimization" (veri minimizasyonu) uygulanıyor
> olmalı; bunlar zaten KVKK gereği zorunlu.

## 8.4 Submission paketi — son kontrol

Submit butonuna basmadan önce:

1. **Written service description** — App Settings → Privacy Policy
   sayfasında yayında ([§2.6](./02-meta-app.md#26-app-dashboard--settings--basic--diğer-alanlar)).
2. **Video — `whatsapp_business_messaging`** (mp4 / mov, < 1GB):
   app→customer mesaj akışı, **iki ekran**.
3. **Video — `whatsapp_business_management`** (ayrı dosya): template
   oluşturma, screen recording.
4. **Postman test çağrıları** — submission'dan 24 saat önce
   yapılmış olmalı.
5. **Test user** — reviewer için randevumonline.com paneline.
6. **Privacy Policy + Terms of Service + Data Deletion URL** — App
   Settings'te 200 dönüyor olmalı.
7. **(Opsiyonel) Access Verification** — başvuruyla birlikte veya
   sonrasında. 200/7gün onboarding limiti için gerekir
   ([§6.5.6](./06-tech-provider-onboarding.md#656-onboarding-limitleri)).

Hepsi tamamsa **Submit for review** mavi aktif olur. Tipik review
süresi 3–7 iş günü; reddedilirse [§8.5](#85-yaygın-ret-nedenleri)
tablosunu kontrol et, sonra ilgili alanı düzeltip yeniden submit et.

## 8.5 Yaygın ret nedenleri

| Neden | Çözüm |
|---|---|
| Tek video'da iki izin | Her izin için **ayrı** video yükle. |
| Video'da sadece app görünüyor, WhatsApp tarafı yok | Her iki tarafı **eş zamanlı** kaydet. |
| "Describe" alanları jenerik / 2 satır | Use case'i somut yaz — hangi mesaj tipi, hangi tetikleyici. |
| API test çağrıları görünmüyor | Submission'dan **24 saat önce** Postman koleksiyonunu çalıştır. |
| Privacy Policy / Data Deletion URL 404 | Submission'dan önce her ikisini de tarayıcıdan aç + 200 dön. |
| Gereksiz izin isteme | Sadece kullandığını iste. Catalog, marketing_messages vb. ekleme. |

---

**Üst:** [00. Döküman haritası](./00-index.md) — **İlgili:**
[06. Tech Provider onboarding](./06-tech-provider-onboarding.md),
[07. Hata kılavuzu](./07-hata-kilavuzu.md).
