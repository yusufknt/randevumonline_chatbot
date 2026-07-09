from __future__ import annotations

import getpass
import os
import re
import secrets
import shutil
import sys
from pathlib import Path

from scripts.wa_ops import generate_keypair

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
EXAMPLE_PATH = ROOT / ".env.example"
SECRETS_DIR = ROOT / "secrets"


USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None


class C:
    R = "\033[0m" if USE_COLOR else ""
    B = "\033[1m" if USE_COLOR else ""
    DIM = "\033[2m" if USE_COLOR else ""
    CYAN = "\033[36m" if USE_COLOR else ""
    GREEN = "\033[32m" if USE_COLOR else ""
    YELLOW = "\033[33m" if USE_COLOR else ""
    RED = "\033[31m" if USE_COLOR else ""
    MAG = "\033[35m" if USE_COLOR else ""


def banner(title: str) -> None:
    print(f"\n{C.B}{C.CYAN}━━ {title} ━━{C.R}")


def hint(text: str) -> None:
    print(f"  {C.DIM}{text}{C.R}")


def link(url: str) -> None:
    print(f"  {C.CYAN}→ {url}{C.R}")


def ok(text: str) -> None:
    print(f"  {C.GREEN}✓{C.R} {text}")


def warn(text: str) -> None:
    print(f"  {C.YELLOW}!{C.R} {text}")


def _mask(val: str) -> str:
    if not val:
        return ""
    if len(val) <= 10:
        return "•" * len(val)
    return val[:4] + "…" + val[-3:]


def ask(prompt: str, default: str = "", *, secret: bool = False) -> str:
    suffix = ""
    if default:
        suffix = f" {C.DIM}[mevcut: {_mask(default) if secret else default}]{C.R}"
    try:
        if secret and not default:
            val = getpass.getpass(f"  {C.GREEN}?{C.R} {prompt}{suffix} (gizli): ").strip()
        else:
            val = input(f"  {C.GREEN}?{C.R} {prompt}{suffix}: ").strip()
    except EOFError:
        print()
        return default
    return val if val else default


def yesno(prompt: str, default: bool = True) -> bool:
    s = "Y/n" if default else "y/N"
    try:
        val = input(f"  {C.GREEN}?{C.R} {prompt} [{s}]: ").strip().lower()
    except EOFError:
        return default
    if not val:
        return default
    return val[0] == "y"


def parse_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"([A-Z_][A-Z0-9_]*)=(.*)", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def write_env(values: dict[str, str]) -> None:
    if not EXAMPLE_PATH.exists():
        raise FileNotFoundError(f".env.example bulunamadı: {EXAMPLE_PATH}")
    template = EXAMPLE_PATH.read_text(encoding="utf-8")
    template_keys = set(re.findall(r"^([A-Z_][A-Z0-9_]*)=", template, re.M))

    out_lines: list[str] = []
    for line in template.splitlines():
        m = re.match(r"([A-Z_][A-Z0-9_]*)=", line)
        if m:
            key = m.group(1)
            val = values.get(key, "")
            out_lines.append(f"{key}={val}")
        else:
            out_lines.append(line)

    extras = sorted(set(values) - template_keys)
    if extras:
        out_lines.append("")
        out_lines.append("# Per-tenant değişkenler")
        for k in extras:
            out_lines.append(f"{k}={values[k]}")

    if ENV_PATH.exists():
        backup = ENV_PATH.with_name(".env.bak")
        shutil.copy(ENV_PATH, backup)
        hint(f".env yedeği: {backup.name}")
    ENV_PATH.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")


def step_mongo(env: dict[str, str]) -> None:
    banner("1/7 — MongoDB")
    hint("Yerel kurulum için varsayılan uygundur. Atlas kullanıyorsanız bağlantı string'ini girin.")
    link("docs/01-yerel-kurulum.md §1.2")
    env["MONGODB_URL"] = ask("MONGODB_URL", env.get("MONGODB_URL", "mongodb://localhost:27017"))
    env["MONGODB_DB"] = ask("MONGODB_DB", env.get("MONGODB_DB", "randevum_chatbot"))


def step_verify_tokens(env: dict[str, str]) -> None:
    banner("2/7 — Meta Webhook Verify Token'ları")
    hint("Meta webhook subscription GET'inde hub.verify_token ile eşleşir.")
    hint("Terminal: openssl rand -hex 16")
    link("docs/02-meta-app.md §2.4")

    placeholders = {"change-me-wa", "change-me-ig", ""}
    for key, label in [("WA_VERIFY_TOKEN", "WhatsApp"), ("IG_VERIFY_TOKEN", "Instagram")]:
        cur = env.get(key, "")
        is_placeholder = cur in placeholders
        if cur and not is_placeholder:
            if not yesno(f"{label} verify token zaten dolu — yeniden üreteyim mi?", False):
                continue
        if yesno(f"{label} verify token otomatik üreteyim mi?", True):
            env[key] = secrets.token_hex(16)
            ok(f"{key} = {env[key]}")
        else:
            env[key] = ask(key, cur)


def step_app_secret(env: dict[str, str]) -> None:
    banner("3/7 — Meta App Secret'leri")

    hint("WhatsApp webhook imzası için Facebook App Secret:")
    link("developers.facebook.com/apps → App settings → Basic → App secret → Show")
    link("docs/02-meta-app.md §2.2")
    wa_val = ask("WA_APP_SECRET (Facebook App Secret)", env.get("WA_APP_SECRET", ""), secret=True)
    env["WA_APP_SECRET"] = wa_val

    hint("Instagram webhook imzası için Instagram App Secret (Facebook secret'tan FARKLI):")
    link("developers.facebook.com/apps → Instagram → API setup with Instagram Business Login → Instagram app secret → Show")
    ig_val = ask("IG_APP_SECRET (Instagram App Secret)", env.get("IG_APP_SECRET", ""), secret=True)
    env["IG_APP_SECRET"] = ig_val

    if wa_val:
        ok("WA_APP_SECRET set edildi.")
    if ig_val:
        ok("IG_APP_SECRET set edildi.")


def step_flow_keys(env: dict[str, str]) -> None:
    banner("4/7 — WhatsApp Flow RSA Anahtarları")
    hint("2048-bit RSA çifti üretilir. Public key Meta'ya yüklenir; private key endpoint şifre çözümü için.")
    link("docs/04-whatsapp-flow.md §4.2")

    priv = SECRETS_DIR / "flow_private.pem"
    pub = SECRETS_DIR / "flow_public.pem"

    if priv.exists() and pub.exists():
        ok(f"Anahtar çifti mevcut: {priv.relative_to(ROOT)} + {pub.relative_to(ROOT)}")
        if yesno("Yeniden üreteyim mi? (mevcut Flow'lar kırılır)", False):
            _gen_keys(force=True)
    else:
        if yesno("RSA anahtar çifti üreteyim mi?", True):
            _gen_keys()
        else:
            warn("Atlandı — Flow endpoint çalışmayacak.")

    if priv.exists():
        env["WA_FLOW_PRIVATE_KEY_PATH"] = "secrets/flow_private.pem"
    env["WA_FLOW_PRIVATE_KEY"] = env.get("WA_FLOW_PRIVATE_KEY", "")
    env["WA_FLOW_PRIVATE_KEY_PASSPHRASE"] = ask(
        "Private key passphrase (varsa)",
        env.get("WA_FLOW_PRIVATE_KEY_PASSPHRASE", ""),
        secret=True,
    )

    if pub.exists():
        hint("Public key'i Meta'ya yüklemek için (her phone_number_id için bir kez):")
        print(f"  {C.CYAN}python -m scripts upload-key{C.R}")
        hint("veya 3'lü zincir tek komutla:")
        print(f"  {C.CYAN}python -m scripts onboard{C.R}")


def _gen_keys(force: bool = False) -> None:
    try:
        priv, pub = generate_keypair(SECRETS_DIR, overwrite=force)
        ok(f"RSA anahtar çifti üretildi: {priv.relative_to(ROOT)} + {pub.relative_to(ROOT)}")
    except FileExistsError as e:
        warn(str(e))
    except Exception as e:
        warn(f"Anahtar üretimi başarısız: {e}")


def step_ai(env: dict[str, str]) -> None:
    banner("5/7 — AI Müşteri Temsilcisi (Instagram · Groq)")
    hint("Instagram ana menüsündeki \"Müşteri Temsilcisi\" butonu Groq tabanlı bir")
    hint("AI sohbeti açar; AI yalnız işletmenin DB bilgilerine göre yanıtlar ve")
    hint("randevu için web sitesine (booking_url) yönlendirir.")
    hint("Kapalıyken buton AI'sız klasik davranışa (telefon) düşer.")
    link("Groq ücretsiz API key: console.groq.com/keys")
    link("docs/05-instagram-test.md §5.8")

    cur_on = env.get("AI_ENABLED", "false").strip().lower() == "true"
    enable = yesno("AI Müşteri Temsilcisi açık olsun mu? (AI_ENABLED)", cur_on)
    env["AI_ENABLED"] = "true" if enable else "false"

    # Model varsayılanı korunur; gelişmiş ayarlar (base_url/timeout) .env.example'dan gelir.
    env["GROQ_MODEL"] = env.get("GROQ_MODEL") or "llama-3.3-70b-versatile"

    if enable:
        env["GROQ_API_KEY"] = ask("GROQ_API_KEY (gsk_…)", env.get("GROQ_API_KEY", ""), secret=True)
        env["GROQ_MODEL"] = ask("GROQ_MODEL", env["GROQ_MODEL"])
        if env.get("GROQ_API_KEY"):
            ok("AI açık — Instagram \"Müşteri Temsilcisi\" Groq ile yanıtlayacak.")
        else:
            warn("GROQ_API_KEY boş — key girilene kadar buton telefona düşer.")
    else:
        ok("AI kapalı — Instagram klasik (deterministik) menü modunda.")


def step_tenant_tokens(env: dict[str, str]) -> None:
    banner("7/7 — Tenant Bilgileri (EN SON)")
    hint("Bu adım sona bırakıldı: temp token 24 sa expire olur, sayfa yenilenince kaybolur.")
    hint("Token'ı alır almaz aşağıya yapıştır; .env yazılınca hemen `onboard` koş.")
    link("WA: developers.facebook.com/apps → WhatsApp → Step 1 → Generate token")
    link("IG: developers.facebook.com/apps → Instagram → API setup with Instagram business login")

    tenants = [
        ("BERBER_MEHMET_KUTAHYA", "Berber Mehmet — Kütahya"),
        ("AYSE_GUZELLIK_KADIKOY", "Ayşe Güzellik — Kadıköy"),
        ("PATI_DOSTU_CANKAYA", "Pati Dostu Veteriner — Çankaya"),
    ]

    for slug, label in tenants:
        wa_key = f"WA_{slug}_ACCESS_TOKEN"
        ig_key = f"IG_{slug}_ACCESS_TOKEN"
        pnid_key = f"WA_{slug}_PHONE_NUMBER_ID"
        waba_key = f"WA_{slug}_WABA_ID"
        wa_cur = env.get(wa_key, "")
        ig_cur = env.get(ig_key, "")
        status = []
        if wa_cur:
            status.append("WA ✓")
        if ig_cur:
            status.append("IG ✓")
        status_s = f" ({', '.join(status)})" if status else ""
        print()
        if not yesno(f"{C.MAG}{label}{C.R}{status_s} — bilgileri gir/güncelle?", False):
            continue

        hint("Phone Number ID + WABA ID: developers.facebook.com/apps → WhatsApp → Step 1. Try it out")
        env[pnid_key] = ask("Phone Number ID", env.get(pnid_key, ""))
        env[waba_key] = ask("WABA ID (WhatsApp Business Account ID)", env.get(waba_key, ""))

        link("WA (24 sa): developers.facebook.com/apps → WhatsApp → Step 1 → Generate token")
        link("WA kalıcı: business.facebook.com → Business Settings → System Users → Generate Token")
        env[wa_key] = ask(wa_key, wa_cur, secret=True)

        link("IG: developers.facebook.com/apps → Instagram → API setup with Instagram business login")
        env[ig_key] = ask(ig_key, ig_cur, secret=True)


def step_fastapi(env: dict[str, str]) -> None:
    banner("6/7 — FastAPI + Public URL")
    env["LOG_LEVEL"] = env.get("LOG_LEVEL", "INFO")

    hint("ÖNCE başka terminalde `ngrok http 8000` çalıştır, Forwarding satırındaki")
    hint("HTTPS URL'i buraya yapıştır. ngrok'u henüz başlatmadıysan boş bırak (Enter) —")
    hint("ngrok'u açtıktan sonra tek bölümü tekrar koş: `python -m scripts setup --section fastapi`")
    link("dashboard.ngrok.com/get-started/setup")
    link("docs/01-yerel-kurulum.md §1.6")
    env["PUBLIC_BASE_URL"] = ask(
        "PUBLIC_BASE_URL",
        env.get("PUBLIC_BASE_URL") or "https://YOUR-NGROK-URL.ngrok-free.app",
    )

    base = env["PUBLIC_BASE_URL"].rstrip("/")
    print()
    hint("Bu URL'lerden Meta Dashboard'a yapıştıracaklarınız:")
    print(f"  WA  callback : {C.CYAN}{base}/webhooks/whatsapp{C.R}")
    print(f"  IG  callback : {C.CYAN}{base}/webhooks/instagram{C.R}")
    print(f"  Flow endpoint: {C.CYAN}{base}/webhooks/whatsapp/flow{C.R}  "
          f"{C.DIM}(`onboard` Meta'ya otomatik yazar){C.R}")


def summary(env: dict[str, str]) -> None:
    banner("ÖZET")
    placeholders = {"change-me-wa", "change-me-ig", "", "https://YOUR-NGROK-URL.ngrok-free.app"}

    def mark(key: str) -> str:
        v = env.get(key, "")
        return f"{C.GREEN}✓{C.R}" if v and v not in placeholders else f"{C.YELLOW}—{C.R}"

    ai_on = env.get("AI_ENABLED", "").strip().lower() == "true"
    if not ai_on:
        ai_status = f"{C.YELLOW}kapalı{C.R}"
    elif env.get("GROQ_API_KEY"):
        ai_status = f"{C.GREEN}açık ✓ (Groq key ✓){C.R}"
    else:
        ai_status = f"{C.YELLOW}açık ! (Groq key yok){C.R}"

    rows = [
        ("MongoDB URL", env.get("MONGODB_URL", "")),
        ("WA verify token", mark("WA_VERIFY_TOKEN")),
        ("IG verify token", mark("IG_VERIFY_TOKEN")),
        ("App secret", mark("WA_APP_SECRET")),
        ("AI (IG müşteri temsilcisi)", ai_status),
        ("Flow private key path", env.get("WA_FLOW_PRIVATE_KEY_PATH") or f"{C.YELLOW}—{C.R}"),
        ("PUBLIC_BASE_URL", env.get("PUBLIC_BASE_URL", "")),
    ]

    tenant_count = sum(
        1 for k, v in env.items()
        if k.endswith("_ACCESS_TOKEN") and v
    )
    rows.append(("Tenant token'ları", f"{tenant_count} adet dolu"))

    for label, val in rows:
        print(f"  {label:25} {val}")


SECTIONS = {
    "mongo": step_mongo,
    "verify": step_verify_tokens,
    "app_secret": step_app_secret,
    "flow_keys": step_flow_keys,
    "ai": step_ai,
    "tenants": step_tenant_tokens,
    "fastapi": step_fastapi,
}


def show_current() -> None:
    if not ENV_PATH.exists():
        warn(".env yok — `python -m scripts setup` ile oluşturun.")
        return
    env = parse_env(ENV_PATH)
    summary(env)


def run_full(env: dict[str, str]) -> None:
    step_mongo(env)
    step_verify_tokens(env)
    step_app_secret(env)
    step_flow_keys(env)
    step_ai(env)
    step_fastapi(env)
    step_tenant_tokens(env)


def run_wizard(*, section: str | None = None) -> None:
    print()
    print(f"{C.B}{C.CYAN}╭──────────────────────────────────────────╮{C.R}")
    print(f"{C.B}{C.CYAN}│  RandevumOnline Chatbot — .env sihirbazı │{C.R}")
    print(f"{C.B}{C.CYAN}╰──────────────────────────────────────────╯{C.R}")
    print()
    print(f"Adım adım {C.B}.env{C.R} dosyanız doldurulur. Boş enter → mevcut değer korunur.")
    print(f"Detaylı belgeler: {C.CYAN}docs/00-index.md{C.R}")

    if not EXAMPLE_PATH.exists():
        warn(f".env.example bulunamadı: {EXAMPLE_PATH}")
        sys.exit(1)

    env = parse_env(ENV_PATH if ENV_PATH.exists() else EXAMPLE_PATH)

    if ENV_PATH.exists() and not section:
        print()
        if not yesno(".env zaten var — sihirbazı çalıştırayım mı? (yedeklenecek)", True):
            print("İptal edildi.")
            return

    try:
        if section:
            SECTIONS[section](env)
        else:
            run_full(env)
    except KeyboardInterrupt:
        print()
        warn("İptal edildi — .env yazılmadı.")
        sys.exit(1)

    print()
    if not yesno("Bu değerlerle .env yazılsın mı?", True):
        print("İptal edildi.")
        return

    write_env(env)
    summary(env)
    print()
    ok(".env yazıldı.")
    print()
    base = env.get("PUBLIC_BASE_URL", "").rstrip("/")
    ngrok_ready = bool(base) and base != "https://YOUR-NGROK-URL.ngrok-free.app"

    hint("Sıradaki adımlar (sıralı):")
    if not ngrok_ready:
        print(f"  1. ngrok başlat:   {C.CYAN}ngrok http 8000{C.R}  → Forwarding URL'ini al, sonra:")
        print(f"                     {C.CYAN}.venv/bin/python -m scripts setup --section fastapi{C.R}")
    else:
        print(f"  1. ngrok'un {C.CYAN}{base}{C.R} adresinde açık olduğundan emin ol")
        print(f"     {C.DIM}(free tier'da URL her restartta değişir → --section fastapi ile güncelle){C.R}")
    print(f"  2. DB seed:        {C.CYAN}.venv/bin/python -m db.seed{C.R}")
    print(f"  3. Backend başlat: {C.CYAN}.venv/bin/uvicorn app.main:app --reload --port 8000{C.R}")
    print()
    base_show = base if ngrok_ready else "<PUBLIC_BASE_URL>"
    hint("Instagram testi:")
    print(f"  4. Kalıcı menü:    {C.CYAN}.venv/bin/python -m scripts ig-menu set <slug>{C.R}")
    print(f"  5. Meta Dashboard → Instagram → webhooks (yalnız UI'da yapılır):")
    print(f"       Callback   : {C.CYAN}{base_show}/webhooks/instagram{C.R}")
    print(f"       Verify     : .env'deki IG_VERIFY_TOKEN")
    print(f"       Alanlar    : messages + messaging_postbacks")
    print(f"       App Mode   : {C.YELLOW}Live{C.R} (Development'ta IG DM webhook'u gelmez)")
    print()
    hint("WhatsApp Flow (opsiyonel — IG için GEREKMEZ, Business Verification ister):")
    print(f"  {C.CYAN}.venv/bin/python -m scripts onboard{C.R}  {C.DIM}(RSA + Flow create/publish + Mongo){C.R}")
    hint("Detay: docs/TEMP-sifirdan-kurulum.md")
