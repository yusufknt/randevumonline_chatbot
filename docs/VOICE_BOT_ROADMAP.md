# Sesli Randevu Botu — Roadmap

**Hedef:** Retell.ai / Vapi / Bland.ai benzeri ama **tamamen self-hosted**, Türkçe odaklı bir sesli randevu asistanı. İşletmeler kendi sabit/mobil numaralarını **Netgsm SIP Trunk** üzerinden bizim sunucumuza yönlendirir; arayan müşteriler AI ile konuşarak randevu alır.

Mevcut WhatsApp/Instagram chatbot ile **aynı MongoDB ve aynı `app/core/booking`/`availability` çekirdeği** kullanılır. WA Flow ve IG kanalları LLM **içermez** (Flow ekranı + postback dispatcher); `app/core/ai.py` ve `app/core/tools.py` bu nedenle projeden kaldırılmıştır. Voice kanalı bu modülleri **sıfırdan** `app/voice/` altında uygulayacak — LLM bu projeye ilk defa Voice ile gelir.

---

## 1. Yüksek Seviye Mimari

```
Müşteri telefonu
      │  (PSTN/GSM)
      ▼
Netgsm Switch ──── SIP Trunk (UDP 5060, RTP) ────┐
                                                 ▼
                                        ┌─────────────────┐
                                        │   Asterisk      │  ← bizim VoIP gateway
                                        │   (PBX/SBC)     │
                                        └────────┬────────┘
                                                 │ ARI / AGI / AudioSocket
                                                 ▼
                                        ┌─────────────────┐
                                        │  Voice Agent    │  ← Python servis
                                        │  (FastAPI)      │
                                        └──┬───┬───┬──┬───┘
                                           │   │   │  │
                                  ┌────────┘   │   │  └─────────┐
                                  ▼            ▼   ▼            ▼
                              Whisper      LLM   TTS         Tools
                              (STT)      (Ollama) (Piper)  (mevcut)
                                                              │
                                                              ▼
                                                          MongoDB
```

**Kritik gözlem:** Netgsm bize SIP üzerinden ham çağrı verir. Doğrudan SIP konuşamayız (FastAPI HTTP, SIP UDP+RTP); bu yüzden **Asterisk** (veya FreeSWITCH) bir gateway olarak araya girer ve sesi bizim Python servisimize **ham PCM stream** olarak akıtır.

---

## 2. Bileşenler

| Bileşen | Sorumluluk | Seçim önerisi | Self-host? |
|---|---|---|---|
| SIP operatörü | Numara → IP yönlendirme | **Netgsm SIP Trunk** | Hayır (operatör) |
| VoIP gateway / SBC | SIP/RTP terminate, ses akış yönetimi | **Asterisk 20 LTS** (alternatif: FreeSWITCH) | ✅ |
| Ses akış protokolü | Asterisk → Python | **AudioSocket** (TCP, 16-bit 8kHz PCM) veya **ARI ExternalMedia** (UDP RTP) | ✅ |
| ASR (Speech-to-Text) | Müşteri sesini metne | **faster-whisper** (CTranslate2) — Whisper Large-v3 Turbo | ✅ |
| VAD | Cümle sonu tespiti | **Silero VAD** (ONNX) | ✅ |
| LLM | Diyalog + tool-use | **Ollama** (mevcut) — `qwen2.5:14b-instruct` veya `llama3.1:8b-instruct` | ✅ |
| TTS | Metin → ses | **Coqui XTTS-v2** (ses klonlama, çok dilli) veya **Piper** (hızlı, daha robotik) | ✅ |
| Telephony orchestrator | Çağrı state machine | Python servis (`app/voice/`) | ✅ |
| Gözlemlenebilirlik | Latency, başarı oranı | Prometheus + Grafana, çağrı kayıtları MongoDB | ✅ |

> **Neden tamamen self-host?** Retell.ai gibi SaaS ürünleri çağrı dakikası başına ücret alır (~$0.07–0.15/dk). Türkiye fiyatlarıyla bu pahalı; KVKK için ses kayıtlarının yurtdışına çıkmaması da büyük bir avantaj.

---

## 3. Netgsm SIP Trunk — Sunucu Tarafı Hazırlığı

[`docs/Netgsm.md`](Netgsm.md) bilgilerine göre Netgsm tarafında ihtiyacımız olanlar:

- **IP:** Asterisk sunucumuzun public IPv4'ü (sabit olmalı, NAT arkasındaysa port forward).
- **Port:** UDP 5060 (SIP) + UDP 10000-20000 (RTP medya).
- **Arayan Prefix:** `0` (default) → bize `0532XXXXXXX` formatında gelir.
- **Aranan Prefix:** `+90` → bize `+90312XXXXXXX` formatında gelir.

**Bizim tarafta:**
- Ubuntu 22.04 LTS sunucu (önerilen 4 vCPU / 8 GB RAM / GPU varsa Whisper hızlanır).
- Public IPv4 (Netgsm portalına bunu gireceğiz).
- Firewall:
  ```
  ufw allow 5060/udp
  ufw allow 10000:20000/udp
  ufw allow 22/tcp
  ufw allow 8000/tcp   # FastAPI (sadece dahili / VPN)
  ```
- IP tabanlı kimlik doğrulama: Netgsm'in SIP signaling subnet'inden gelen INVITE'lar accept edilir, diğerleri reddedilir (Asterisk `pjsip` `permit/deny` listesi ile).

---

## 4. Asterisk Tasarımı

### 4.1 Çağrı yönü

- **Inbound (gelen çağrı):** Netgsm → Asterisk → Stasis(`voicebot`) → ExternalMedia → Python servisimiz.
- **Outbound (giden çağrı, ileride hatırlatma araması için):** Python → ARI `originate` → Asterisk → Netgsm → PSTN.

### 4.2 pjsip endpoint (örnek)

```ini
; /etc/asterisk/pjsip.conf
[netgsm-trunk]
type=endpoint
context=from-netgsm
disallow=all
allow=alaw           ; Netgsm G.711 A-law verir genellikle
allow=ulaw
direct_media=no
rtp_symmetric=yes
force_rport=yes
rewrite_contact=yes

[netgsm-aor]
type=aor
contact=sip:<NETGSM_PEER_IP>:5060

[netgsm-identify]
type=identify
endpoint=netgsm-trunk
match=<NETGSM_PEER_IP>/32
```

### 4.3 Dialplan (extensions.conf)

```ini
[from-netgsm]
exten => _+90X.,1,NoOp(Inbound from ${CALLERID(num)} to ${EXTEN})
 same => n,Answer()
 same => n,Stasis(voicebot,${EXTEN},${CALLERID(num)})
 same => n,Hangup()
```

`Stasis(voicebot, ...)` çağrıyı **ARI** üzerinden Python'a teslim eder. Python tarafında WebSocket ile ARI eventlerini dinleriz.

### 4.4 Ses akışı: AudioSocket

ExternalMedia (UDP RTP) yerine **AudioSocket** (TCP, frame-bazlı) kullanmak Python tarafını çok basitleştirir. Asterisk 18+ destekler:

```ini
exten => s,1,Answer()
 same => n,AudioSocket(<UUID>,127.0.0.1:9092)
```

Frame formatı: 16-bit signed PCM @ 8 kHz, mono, 320 byte chunks (20ms). Python TCP server bu chunk'ları okur, Whisper'a yollar; TTS çıktısını aynı formatta geri yazar.

---

## 5. Python Servis Tasarımı

Yeni dizin: `app/voice/`

```
app/voice/
├── __init__.py
├── ari_client.py          # WebSocket ARI client (asyncio)
├── audio_socket.py        # TCP server, 8kHz PCM stream
├── stt.py                 # faster-whisper wrapper + VAD
├── tts.py                 # Piper / XTTS wrapper
├── llm.py                 # Ollama tool-use döngüsü + sistem prompt
├── tools.py               # randevu tool'ları (list_services, create_appointment …)
├── pipeline.py            # streaming STT → LLM → TTS state machine
├── call_session.py        # tek çağrı için context (business + customer + conv)
└── config.py              # voice-spesifik env'ler
```

### 5.1 Çağrı yaşam döngüsü (state machine)

```
StasisStart event
   │
   ▼
identify_business(called_number)      ← businesses.contact.phone üzerinden eşleştir
   │
   ▼
identify_customer(caller_number)      ← customers.phone (E.164) upsert
   │
   ▼
upsert_voice_conversation             ← channel="voice", thread_id=call_id
   │
   ▼
greet (TTS: "Merhaba, X işletmesine hoş geldiniz...")
   │
   ▼ (loop)
   ┌──── listen (VAD ile cümle sonu yakala) ────┐
   │            │                               │
   │            ▼                               │
   │     transcribe (Whisper streaming)         │
   │            │                               │
   │            ▼                               │
   │     LLM tool-use turu (app/voice/llm.py)    │
   │            │                               │
   │            ▼                               │
   │     speak (TTS stream-out)                 │
   │            │                               │
   └────────────┴───────────────────────────────┘
   │
   ▼ (Hangup veya tool=end_call)
StasisEnd → kapat, conversation.closed_at=now
```

### 5.2 Latency hedefleri

Sesli botta **konuşma cevap gecikmesi** UX'in her şeyidir. Hedefler (her bir adım için):

| Aşama | Hedef p95 | Strateji |
|---|---|---|
| VAD endpoint detection | < 300 ms | Silero VAD, 200ms tail silence eşiği |
| STT (Whisper) | < 600 ms | faster-whisper Large-v3 Turbo, GPU varsa CUDA, yoksa int8 CPU |
| LLM ilk token | < 700 ms | Ollama keep_alive, küçük model (8B), warm context |
| LLM tool-use turu | < 1500 ms | Tool sayısı az tutulmalı, paralel tool çağrıları |
| TTS ilk audio | < 400 ms | Piper streaming (cümle bittikçe parça parça yolla) |
| **Toplam (yanıta dek)** | **< 1.5 s** ideal, **< 2.5 s** kabul | Streaming + paralel pipeline |

> **İpucu:** "Tamam... bir bakıyorum..." gibi **filler audio** ekleyin. LLM tool çalıştırırken bu filler oynatılır → algılanan latency yarıya iner. Retell.ai'nin gizli sosu budur.

### 5.3 Barge-in (sözünü kesme)

Müşteri TTS oynarken konuşmaya başlarsa TTS'i hemen kesmeli ve dinlemeye geçmeli. AudioSocket çift yönlü TCP olduğu için zor değil:

```python
async def speak(text):
    async for chunk in tts.stream(text):
        if vad.detected_speech():
            tts.cancel()
            break
        await audio_out.send(chunk)
```

---

## 6. Mevcut Sistemle Entegrasyon

### 6.1 MongoDB değişiklikleri (minimal)

`businesses` koleksiyonuna voice config:
```js
channels.voice = {
  enabled: true,
  inbound_number: "+903123330001",   // Netgsm'in bize yönlendirdiği numara
  language: "tr-TR",
  tts_voice: "tr_TR-fahrettin-medium",  // Piper ses modeli
  greeting: "Merhaba, Pati Dostu Veteriner'e hoş geldiniz...",
  max_call_duration_s: 600,
}
```

`appointments.source` enum'una **`voice`** eklenir.

`conversations.channel` enum'una **`voice`** eklenir; `channel_thread_id` = Asterisk channel UUID.

`conversations` üstüne yeni opsiyonel alanlar:
```js
audio_recording_url: "vault://recordings/<call_id>.mp3",  // KVKK uyumlu, opt-in
call_started_at: ISODate,
call_ended_at: ISODate,
call_duration_s: 124,
call_outcome: "booked" | "abandoned" | "handoff" | "no_intent"
```

### 6.2 Tool seti — sıfırdan yaz

`app/core/tools.py` projeden kaldırıldığı için Voice kanalı için tool'lar **`app/voice/tools.py`** olarak yeniden yazılmalıdır. Randevu mantığı `app/core/booking.py` ve `app/core/availability.py` üzerinden aynı şekilde çalışır.

Temel tool'lar:
- `list_services(business_id)` — mevcut hizmet listesi
- `list_available_slots(business_id, service_id, date, before?)` — müsait saatler
- `list_staff_available_at(business_id, slot_dt)` — müsait personel
- `create_appointment(...)` — randevu oluştur
- `send_sms_with_image_link(service_id, week_offset?)` — sesli kanalda görsel yerine SMS link
- `end_call(reason)` — Asterisk'e Hangup gönderir
- `transfer_to_human(reason)` — Asterisk'e Bridge gönderir, çağrıyı işletme sahibine aktarır

### 6.3 Sistem prompt

`app/voice/llm.py` içinde `build_system_prompt(business)` yazılmalı. WA/IG kanallarında LLM olmadığından kıyaslanacak "text" davranışı yok; yalnızca voice-spesifik prompt yeterli:

> "Sesli konuşuyorsun. Cevapların 1-2 cümle olsun, listeyi tek tek oku, ✓/✕/madde işareti kullanma. Onay için 'evet' bekle. Saatleri 'on dört otuz' gibi yaz."

---

## 7. STT / TTS Detayları

### 7.1 STT: faster-whisper

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
# CPU fallback: device="cpu", compute_type="int8"
```

Streaming için **partial transcription**: VAD ile 200ms sessizlik bekle, sonra son N saniyenin buffer'ını transcribe et. Türkçe için Whisper Large-v3 Turbo kelime hata oranı düşük (~10-12% gerçek dünya).

### 7.2 VAD: Silero

```python
import torch
vad_model = torch.jit.load("silero_vad.jit")
# Her 30ms PCM chunk için speech probability
```

Endpoint detection: **300ms** sürekli sessizlik = cümle bitti.

### 7.3 TTS: Piper (önce) → XTTS (sonra)

**Piper** (~50 MB model, CPU'da gerçek zamanlı): Hızlı, pratik. Türkçe sesleri sınırlı:
- `tr_TR-fahrettin-medium` — erkek
- `tr_TR-dfki-medium` — kadın

**XTTS-v2** (Coqui): Ses klonlama. İşletme sahibi 30 saniye ses kaydı verirse "kendi sesi" ile bot. Daha yavaş (~0.3-0.5 RTF GPU'da). Premium feature olarak konumlandırılabilir.

Streaming TTS: Piper cümle-cümle yayınlar. Cümleyi LLM'den parça parça aldıkça TTS'e yollarsak ilk audio gecikmesi minimum olur.

---

## 8. Çağrı Akışı Örneği

```
[ZIL]
Bot:    Merhaba, Pati Dostu Veteriner'e hoş geldiniz. Ben yapay zekâ randevu
        asistanıyım, size nasıl yardımcı olabilirim?
Müşteri: Köpeğim için aşı randevusu almak istiyorum.
Bot:    [tool: list_services] Tabii, karma aşı dediniz değil mi? Bu hafta
        Salı, Çarşamba ve Perşembe günlerimiz müsait. Hangi gün uygun?
Müşteri: Çarşamba olabilir, sabah saatleri varsa.
Bot:    [tool: list_available_slots(date=çarşamba, before=12:00)]
        Çarşamba sabah dokuz, on ve on bir saatlerimiz müsait. Hangisi?
Müşteri: On birde olur.
Bot:    [tool: list_staff_available_at] Çarşamba on birde Vet. Hekim Can Bey
        ve Selin Hanım müsait. Bir tercihiniz var mı?
Müşteri: Fark etmez.
Bot:    Can Bey ile ayarlayayım o zaman. Adınızı alabilir miyim?
Müşteri: Mehmet Yıldırım.
Bot:    [tool: update_customer_name → create_appointment]
        Mehmet Bey, Çarşamba on bir için Can Bey ile karma aşı randevunuz
        oluşturuldu. SMS ile hatırlatma göndereceğiz, görüşmek üzere.
[KAPAT]
```

---

## 9. Roadmap (faz faz)

### Faz 0 — Temel altyapı (1-2 hafta)
- [ ] Ubuntu sunucu provision + public IP + firewall.
- [ ] Asterisk 20 kurulum, pjsip + ARI aktif.
- [ ] Netgsm SIP Trunk başvurusu, IP whitelist.
- [ ] Sahte test numarasıyla Asterisk → Netgsm trunk doğrulama (basit `Playback("hello-world")`).

**Çıktı:** Telefon eden müşteri Asterisk'ten kayıtlı bir karşılama duyabiliyor.

### Faz 1 — STT/TTS prototipi (1-2 hafta)
- [ ] `faster-whisper` Türkçe transcription benchmark (örnek 50 ses kaydı).
- [ ] Piper Türkçe TTS sample, telefon kalitesinde 8kHz mono ile test.
- [ ] AudioSocket TCP server (Python asyncio).
- [ ] Round-trip echo test: telefonla konuş → transcribe → aynı metni TTS ile geri oku.

**Çıktı:** Bot, müşterinin söylediğini tekrar edebiliyor (papağan modu).

### Faz 2 — LLM entegrasyonu (1 hafta)
- [ ] `app/voice/pipeline.py` — STT → LLM → TTS state machine.
- [ ] `app/voice/llm.py` yaz: Ollama OpenAI-compat endpoint + tool-use döngüsü (`channel="voice"`).
- [ ] `app/voice/tools.py` yaz: `list_services`, `list_available_slots`, `list_staff_available_at`, `create_appointment` (§6.2).
- [ ] Voice-spesifik sistem prompt (§6.3).
- [ ] Filler audio ("bir saniye bakıyorum...") tool çağrılarında.

**Çıktı:** Bot, küçük diyaloglarda doğal cevap veriyor; randevu oluşturmuyor henüz.

### Faz 3 — Tam randevu akışı (1-2 hafta)
- [ ] `list_services` → `list_available_slots` → `list_staff_available_at` → `create_appointment` zinciri.
- [ ] `end_call` ve `transfer_to_human` tool'ları.
- [ ] `conversations.channel="voice"` desteği orchestrator'a eklenmesi.
- [ ] Ses kaydı (KVKK opt-in metniyle başlangıçta uyarı).

**Çıktı:** Tek bir test işletmesi için bot baştan sona randevu alıyor.

### Faz 4 — Latency optimizasyonu (1-2 hafta)
- [ ] Streaming TTS (Piper cümle-cümle).
- [ ] LLM warm-pool (Ollama `keep_alive=-1`).
- [ ] Whisper int8 CPU profili veya GPU consolidation.
- [ ] Filler bank: 5-6 farklı "bekleme" sesi rastgele.
- [ ] Barge-in (müşteri sözünü kestiğinde TTS dur).
- [ ] p95 latency < 2.5 s, p50 < 1.5 s hedefi.

### Faz 5 — Multi-tenant + Production (2 hafta)
- [ ] Numara → business eşleme (`businesses.channels.voice.inbound_number`).
- [ ] Eşzamanlı çağrı limiti (per-business + global).
- [ ] Asterisk failover (2. node, RTPengine veya Kamailio yük dengeleyici).
- [ ] Prometheus metrics: `call_duration_seconds`, `stt_latency_ms`, `tts_latency_ms`, `llm_latency_ms`, `call_outcome_total`.
- [ ] Grafana dashboard.
- [ ] Çağrı kayıtları S3-compatible bucket (MinIO self-host).
- [ ] KVKK aydınlatma metni karşılamada otomatik.

### Faz 6 — Çıkış (outbound) (1 hafta)
- [ ] Randevu hatırlatma araması (T-3 saat): bot arar, "Yarınki randevunuzu onaylıyor musunuz?".
- [ ] No-show takibi otomatik.
- [ ] APScheduler ile cron.

### Faz 7 — Premium (opsiyonel)
- [ ] **XTTS-v2 ile ses klonlama**: işletme sahibinin sesi.
- [ ] Çoklu dil (Arapça, Almanca turistik bölgeler için).
- [ ] **Sentiment analizi**: müşteri sinirlendiyse otomatik handoff.
- [ ] **Konuşma özeti**: WA üzerinden işletmeye "Bugün 14 çağrı, 9 randevu" raporu.

---

## 10. Riskler & Düşünmemiz Gerekenler

| Risk | Etki | Mitigasyon |
|---|---|---|
| STT Türkçeyi yanlış anlarsa | Yanlış randevu | Whisper Large-v3 Turbo + LLM tarafında onay zorunlu. Saat ve isim için harf-harf onay. |
| TTS robotik geliyor | Müşteri ciddiye almaz | Önce Piper ile başla, premium müşterilere XTTS sun. |
| Asterisk DDoS / SIP scan | Servis dışı | `fail2ban` + IP whitelist (sadece Netgsm subnet). |
| Eşzamanlı çağrı patlaması | LLM/STT kuyruğu şişer | Per-business max 2 eşzamanlı; global limit. Aşan çağrılara "Tüm hatlarımız meşgul, 1 dk sonra arayın". |
| GPU yokluğunda yavaşlık | Latency hedefi kaçar | İlk müşterilerde Piper (CPU) + Whisper int8 ile yetin. GPU sunucuya yatırım, müşteri 50+'ı geçince. |
| KVKK / ses kaydı | Yasal | Aydınlatma metni karşılamada zorunlu, opt-in. Ses kayıtları 30 gün sonra otomatik silme. |
| Netgsm bağlantı kesilirse | Hizmet dışı | İkinci bir SIP operatörü (örn. Türk Telekom Hosted PBX) failover. |
| Halüsinasyon (uydurma randevu) | Müşteri mağdur | Mevcut sistemdeki gibi `tools` ile DB'ye bağlı; LLM uydurursa create_appointment hata verir. Sesli onay zorunlu. |

---

## 11. Maliyet Tahmini (aylık, 100 işletme / 5000 dk konuşma)

| Kalem | Tahmin |
|---|---|
| Sunucu (4 vCPU, 16GB, 500GB SSD) | ₺800 - ₺1.500 |
| GPU sunucu (RTX 4090 veya Tesla T4) — ileride | ₺3.000 - ₺6.000 |
| Netgsm SIP Trunk (numara başına ~₺50/ay + dakika) | ₺5.000 - ₺10.000 |
| Yedek SIP operatörü | ₺1.500 |
| MinIO storage (ses kayıtları) | ₺500 |
| **Toplam** | **₺11.000 - ₺20.000** |

> Kıyas: Retell.ai $0.07/dk × 5000 dk = $350 ≈ ₺12.000 **sadece AI tarafı için**, üstüne Twilio numara ücreti eklenir.

---

## 12. İlk MVP İçin Minimum Gerekenler

Sadece "1 işletme + 1 numara + temel akış" için 6 haftalık minimum çıktı:

1. **Asterisk + Netgsm SIP Trunk** — gelen çağrı bizim sunucuya düşüyor.
2. **AudioSocket TCP server** + faster-whisper Türkçe + Piper Türkçe.
3. **`app/voice/llm.py` + `app/voice/tools.py`** — sıfırdan, `channel="voice"` ile.
4. **Hizmet seçimi → saat seçimi → personel → onay → create_appointment** akışı.
5. **end_call** ve **transfer_to_human**.
6. **Tek işletme manuel onboard** (Berber Mehmet).
7. **Çağrı kaydı** + transcript MongoDB'ye.

Bu MVP ile gerçek bir berberin numarasını yönlendirip 1 hafta canlı test → öğrendiklerimizi Faz 4'e besleriz.

---

## 13. Kapanış

WA/IG botu tarafında zaten doğru soyutlamalar var: tools, conversations, multi-tenant. Voice eklemek **paralel bir kanal** olarak yapılır — hiçbir core kod yıkılmaz. Asıl iş telephony stack'inin (Asterisk + STT/TTS + latency tuning) doğru kurulması.

İlerleme: önce **Faz 0-1** (altyapı + papağan), sonra LLM çevir, sonra optimize et. Retell'i geçmek için tek bir şey gerekli: **filler audio + streaming TTS + warm LLM**. Bu üç mühendislik kararı ürünü ya parlatır ya batırır.
