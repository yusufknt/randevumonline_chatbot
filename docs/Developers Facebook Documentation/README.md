# html-to-markdown

JavaScript ile render edilen modern web sitelerini (React/Vue/SPA) tam olarak yükleyip **temiz Markdown** dosyalarına dönüştüren bir araç seti. Özellikle Facebook for Developers, MDN, Docusaurus tabanlı dokümantasyon siteleri ve benzeri JS-ağırlıklı sayfalar için tasarlandı.

> **Neden bu araç?** `requests + BeautifulSoup` veya `wget`, JavaScript çalıştırmadığı için React tabanlı sitelerde boş/eksik HTML alırsın. Bu proje **Playwright + headless Chromium** kullanarak sayfayı gerçek bir tarayıcıda render eder, sonra Markdown'a çevirir.

---

## İçerik

- [Özellikler](#özellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum (Adım Adım)](#kurulum-adım-adım)
- [Kullanım](#kullanım)
  - [1. Tek Sayfa İndirme](#1-tek-sayfa-indirme-scrape_pagepy)
  - [2. Recursive Crawler](#2-recursive-crawler-crawl_sitepy-önerilen)
- [Pratik Senaryolar](#pratik-senaryolar)
- [Nasıl Çalışıyor?](#nasıl-çalışıyor)
- [İpuçları & Sorun Giderme](#ipuçları--sorun-giderme)
- [Alternatif Hazır Araçlar](#alternatif-hazır-araçlar)
- [Yasal Uyarı](#yasal-uyarı)

---

## Özellikler

- **JS rendering**: Playwright + headless Chromium ile gerçek tarayıcı ortamı.
- **Temiz Markdown çıktısı**: `<nav>`, `<header>`, `<footer>`, cookie banner gibi gürültüleri otomatik kaldırır; ana içeriği (`<main>`, `<article>`) yakalar.
- **İki farklı mod**:
  - Tek sayfa scraper
  - Recursive crawler (link takibi)
- **Paralel indirme**: `asyncio` + worker pool, ayarlanabilir concurrency.
- **Akıllı link normalizasyonu**: `href`/`src` değerleri absolute URL'e çevrilir.
- **Filtreleme**: include/exclude substring filtreleri.
- **Progress bar**: `tqdm` ile canlı ilerleme.

---

## Gereksinimler

- Python 3.10+ (test edildi: 3.12)
- ~500 MB disk (Chromium binary ~170 MB + paketler)
- Linux/macOS/WSL2/Windows
- Linux'ta sudo (sadece sistem kütüphaneleri için, bir kez)

---

## Kurulum (Adım Adım)

### 1) Repo'yu klonla / dizine geç
```bash
cd /home/taha/projects/html-to-markdown
```

### 2) Sanal ortam oluştur ve aktive et
```bash
python3 -m venv .venv
source .venv/bin/activate     # Linux/macOS
# .venv\Scripts\activate     # Windows
```

### 3) Python paketlerini kur
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Playwright Chromium binary'sini indir
```bash
playwright install chromium
```

### 5) **Linux/WSL için sistem bağımlılıkları (zorunlu)**

Linux/WSL'de Chromium'un çalışabilmesi için bazı paylaşımlı kütüphaneler şart:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libatspi2.0-0t64 \
  libcairo2 libcups2t64 libdbus-1-3 libdrm2 libgbm1 libglib2.0-0t64 \
  libnspr4 libnss3 libpango-1.0-0 libx11-6 libxcb1 libxcomposite1 \
  libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xvfb \
  fonts-noto-color-emoji fonts-unifont libfontconfig1 libfreetype6 \
  fonts-liberation fonts-freefont-ttf
```

Veya tek komutla (Playwright'ın resmi yardımcısı):
```bash
sudo $(which playwright) install-deps chromium
```

> macOS / Windows'ta bu adıma gerek yok — Playwright kendi başına halleder.

### 6) Doğrulama (smoke test)
```bash
python scrape_page.py "https://example.com" -o output/example.md
cat output/example.md
```

Bir başlık + paragraf görürsen kurulum tamam. ✅

---

## Kullanım

### 1. Tek Sayfa İndirme (`scrape_page.py`)

Tek bir URL → tek bir Markdown dosyası.

```bash
python scrape_page.py <URL> [-o output.md] [--wait CSS_SELECTOR] [--timeout MS]
```

**Örnekler:**
```bash
# Basit
python scrape_page.py https://developers.facebook.com/docs/graph-api

# Belirli bir output dosyası
python scrape_page.py https://developers.facebook.com/docs/graph-api -o graph-api.md

# Bir CSS seçici görünene kadar bekle (lazy loaded içerik için)
python scrape_page.py https://developers.facebook.com/docs/graph-api \
    --wait "main article h1" --timeout 90000
```

`-o` verilmezse otomatik olarak URL yolunu `__` ile ayrılmış dosya adına çevirir:
`output/<url-path-with-__>.md`. Örneğin `/docs/graph-api/overview` için
`output/docs__graph-api__overview.md` oluşur.

---

### 2. Recursive Crawler (`crawl_site.py`) ⭐ **Önerilen**

Bir başlangıç URL'inden başlayarak aynı domain altındaki linkleri takip eder.

```bash
python crawl_site.py <START_URL> \
    [--out output/] \
    [--max 100] \
    [--depth 3] \
    [--concurrency 4] \
    [--include substring] \
    [--exclude substring] \
    [--nav-only]
```

**Örnek (Graph API dokümanları):**
```bash
python crawl_site.py https://developers.facebook.com/docs/graph-api \
    --include /docs/graph-api \
    --nav-only \
    --max 200 --depth 4 --concurrency 1 \
    --out output/fb-graph-api
```

**Notlar:**
- `--include` birden çok kez verilebilir (OR mantığı).
- `--depth 0` = sadece başlangıç sayfası.
- `--concurrency 1`, sidebar sırasını ve "tıklayınca açılan alt bölüm" davranışını en tutarlı şekilde korur. Hız öncelikliyse artırabilirsin; daha yüksek değerlerde rate-limit yiyebilirsin.
- `--nav-only`, Facebook docs gibi sayfalarda sadece sidebar/nav linklerini takip eder; sayfa içindeki örnek/reference linkleri kuyruğa almaz. Aktif sayfaya göre açılan alt sidebar bölümleri de ziyaret edilir.
- Crawl sonunda `out_dir/index.md` oluşturulur. Bu dosya gezilen sidebar/nav menüsünü listeler; indirilen sayfalara lokal `.md` linki, henüz indirilmeyenlere kaynak URL verir.
- Sayfa dosyaları URL segmentleri `__` ile birleştirilerek adlandırılır. Bu yapı okunabilir kalır, derin klasör üretmez ve `/changelog` ile `/changelog/version25.0` gibi ilişkili sayfaları yan yana gösterir.

**Çıktı örneği:**
```text
output/fb-graph-api/
├── index.md                           # sidebar/nav özeti
├── docs__graph-api.md                 # /docs/graph-api
├── docs__graph-api__overview.md
├── docs__graph-api__get-started.md
└── docs__graph-api__changelog.md
```

---

## Pratik Senaryolar

### A) Belirli bir docs bölümünü indirmek
```bash
python crawl_site.py https://developers.facebook.com/docs/graph-api/overview \
    --include /docs/graph-api \
    --max 200 --depth 4 --concurrency 3 \
    --out output/fb-graph-api
```

### B) Tek bir sayfayı hızlıca almak
```bash
python scrape_page.py https://developers.facebook.com/docs/graph-api/overview \
    -o overview.md
```

### C) Kendi blogundan / küçük site'tan tüm yazılar
```bash
python crawl_site.py https://example-blog.com \
    --max 50 --depth 2 --out output/blog
```

---

## Nasıl Çalışıyor?

```
┌──────────────┐    ┌────────────────┐    ┌──────────────┐    ┌────────────┐
│ URL keşfi    │ -> │ Playwright     │ -> │ BeautifulSoup│ -> │ markdownify│
│ (recursive   │    │ (Chromium      │    │ (gürültü     │    │ (HTML→MD)  │
│  link takibi)│    │  + JS render)  │    │  temizleme)  │    │            │
└──────────────┘    └────────────────┘    └──────────────┘    └────────────┘
                                                                    │
                                                                    v
                                                            output/<url-path-with-__>.md
```

1. **Render**: Headless Chromium, sayfayı `networkidle` event'ine kadar yükler — yani XHR/fetch çağrıları bittikten sonra.
2. **Temizleme**: `<nav>`, `<header>`, `<footer>`, banner'lar, cookie popup'lar regex/CSS selector ile silinir. `<main>`/`<article>`/`#content` öncelik sırasıyla aranır.
3. **Link normalizasyonu**: Tüm relatif `href` ve `src` değerleri absolute URL'e dönüştürülür — Markdown başka yere taşınınca linkler bozulmaz.
4. **Markdown**: `markdownify` ATX heading + `-` bullet stiliyle dönüştürür; arda arda fazla newline'lar tek pasaja indirilir.

---

## İpuçları & Sorun Giderme

### "TargetClosedError: Browser has been closed"
Chromium çalışmıyor → sistem kütüphaneleri eksik. Yukarıdaki [adım 5](#5-linuxwsl-için-sistem-bağımlılıkları-zorunlu)'i çalıştır.

### "TimeoutError: page.goto"
- `--timeout` değerini artır (`--timeout 120000`).
- Yavaş ağ ya da çok ağır sayfa olabilir; `--concurrency` düşür.

### Sayfa yarım render oluyor
- `--wait "css.selector"` ile içerik konteyneri bekle.
- `scrape_page.py` içinde `wait_until="networkidle"` zaten kullanılıyor.

### Rate limit / 429 / Cloudflare
- `--concurrency 1` yap.
- Worker fonksiyonunda `await asyncio.sleep(1)` ekle.
- Site cloudflare ile koruyorsa `playwright-stealth` paketine geçmen gerekebilir.

### Login gerektiren sayfalar
Bu projede out-of-the-box yok, ama eklemesi kolay: `scrape_page.py` içindeki `browser.new_context()` çağrısına `storage_state="auth.json"` parametresi ekle ve önceden `playwright codegen <url>` ile login state'i kaydet.

### Markdown'da garip karakterler
`markdownify` bazen `&nbsp;` gibi entity'leri olduğu gibi bırakabilir. `html.unescape()` ile temizlenebilir; gerekiyorsa `html_to_markdown` fonksiyonuna ekle.

### Çıktı klasörünü temizle
```bash
rm -rf output/
```

---

## Alternatif Hazır Araçlar

Kendi kodu çalıştırmak istemiyorsan:

| Araç | Açıklama | Ücretsiz? |
|------|----------|-----------|
| **[Jina Reader](https://r.jina.ai)** | `https://r.jina.ai/<URL>` → direkt MD döner. En kolayı. | ✅ Tamamen |
| **[Firecrawl](https://www.firecrawl.dev)** | Crawl + MD API. Playground'u var. | Sınırlı tier |
| **Apify Tech Docs Scrapers** | Docusaurus / GitBook için hazır actor'lar. | Sınırlı tier |
| **`wget --mirror`** | JS render etmez, statik sitelerde işe yarar. | ✅ |
| **HTTrack** | Aynı, statik için. | ✅ |

> Bu projedeki avantaj: tam kontrol (filtre, concurrency, dosya isimlendirme, post-processing).

---

## Proje Yapısı

```
html-to-markdown/
├── .venv/                  # Sanal ortam (gitignore'da)
├── output/                 # MD çıktıları (gitignore'da)
├── scrape_page.py          # Tek sayfa scraper
├── crawl_site.py           # Recursive crawler ⭐
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Yasal Uyarı

- Bu araçları yalnızca **kişisel/araştırma** kullanım için kullan.
- Hedef sitenin **Terms of Service** ve **robots.txt** dosyasını kontrol et.
- Ticari yeniden dağıtım için ilgili kaynağın lisansına bak (Facebook docs için Meta'nın koşulları geçerlidir).
- Rate-limit'lere ve sunucuya yük bindirmemeye dikkat et — `--concurrency` değerini makul tut.

---

## Lisans

Kişisel kullanım için serbest. İçeriğin telif hakları ilgili sitelere aittir.
