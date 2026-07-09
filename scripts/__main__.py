from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from scripts import setup_env
from scripts.gen_test_token import gen_test_token
from scripts.ig_menu import run as run_ig_menu
from scripts.ig_token import run as run_ig_token
from scripts.local_flow_test import run as run_local_flow_test
from scripts.wa_ops import (
    DEFAULT_PUB_PATH,
    DEFAULT_SECRETS_DIR,
    create_flow,
    generate_keypair,
    read_public_pem,
    subscribe_app_to_waba,
    update_business_wa_channel,
    upload_public_key,
)

ROOT = Path(__file__).resolve().parent.parent


def _env_or_prompt(name: str, *, prompt: str, secret: bool = False) -> str:
    val = os.environ.get(name)
    if val:
        print(f"  {setup_env.C.GREEN}✓{setup_env.C.R} {name} (env'den)")
        return val
    return setup_env.ask(prompt, secret=secret)


def _print_block(title: str) -> None:
    print(f"\n{setup_env.C.B}{setup_env.C.CYAN}━━ {title} ━━{setup_env.C.R}")


def cmd_setup(args: argparse.Namespace) -> int:
    if args.show:
        setup_env.show_current()
        return 0
    setup_env.run_wizard(section=args.section)
    return 0


def cmd_gen_keys(args: argparse.Namespace) -> int:
    try:
        priv, pub = generate_keypair(DEFAULT_SECRETS_DIR, overwrite=args.force)
    except FileExistsError as e:
        print(str(e), file=sys.stderr)
        return 1
    print(f"OK\n  {priv}\n  {pub}\n")
    print("Public key (Meta'ya yükle):\n")
    print(pub.read_text(encoding="utf-8"))
    return 0


def cmd_upload_key(args: argparse.Namespace) -> int:
    _print_block("Public key'i Meta'ya yükle")
    setup_env.hint("Endpoint: POST /<PHONE_NUMBER_ID>/whatsapp_business_encryption")
    setup_env.link("docs/04-whatsapp-flow.md §4.2")

    pnid = args.phone_number_id or _env_or_prompt(
        "PHONE_NUMBER_ID", prompt="PHONE_NUMBER_ID")
    token = args.access_token or _env_or_prompt(
        "ACCESS_TOKEN", prompt="ACCESS_TOKEN", secret=True)
    pub_path = Path(args.public_key_path or DEFAULT_PUB_PATH)

    try:
        pub_pem = read_public_pem(pub_path)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        setup_env.hint("Önce: `python -m scripts gen-keys`")
        return 1

    result = upload_public_key(pnid, token, pub_pem, api_version=args.api_version)
    print(f"\nHTTP {result.status_code}: {result.body}")
    return 0 if result.ok else 1


def cmd_create_flow(args: argparse.Namespace) -> int:
    _print_block("Flow yarat + publish")
    setup_env.link("docs/04-whatsapp-flow.md §4.3")

    waba = args.waba_id or _env_or_prompt("WABA_ID", prompt="WABA_ID")
    token = args.access_token or _env_or_prompt(
        "ACCESS_TOKEN", prompt="ACCESS_TOKEN", secret=True)
    public_base = args.public_base_url or os.environ.get("PUBLIC_BASE_URL") or \
        setup_env.ask("PUBLIC_BASE_URL (ngrok HTTPS)")
    setup_env.hint(
        f"Flow endpoint_uri Meta'ya: {public_base.rstrip('/')}/webhooks/whatsapp/flow")

    try:
        result = create_flow(
            waba_id=waba, access_token=token, public_base_url=public_base,
            flow_name=args.name, api_version=args.api_version,
        )
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1

    if result.validation_errors:
        print("\nValidation hataları:")
        for err in result.validation_errors:
            print(f"  - {err}")
        setup_env.warn("Publish atlandı.")
        return 1

    setup_env.ok(f"Flow ID: {result.flow_id}")
    print(f"Publish: HTTP {result.publish_status}: {result.publish_body}")
    print("\nMongo'ya yazmak için:")
    print(f"  db.businesses.updateOne(")
    print(f'    {{business_id: "<slug>"}},')
    print(f'    {{$set: {{"channels.whatsapp.flow_id": "{result.flow_id}"}}}})')
    return 0


def cmd_onboard(args: argparse.Namespace) -> int:
    _print_block("Tenant Onboarding — Flow uçtan uca")
    setup_env.hint(
        "5 adımı zincirler: RSA üret → public key yükle → WABA→app subscribe "
        "→ Flow yarat+publish → Mongo'ya yaz.")
    print()

    # Inputs (arg > env > interaktif)
    pnid = args.phone_number_id or _env_or_prompt(
        "PHONE_NUMBER_ID", prompt="PHONE_NUMBER_ID")
    waba = args.waba_id or _env_or_prompt("WABA_ID", prompt="WABA_ID")
    token = args.access_token or _env_or_prompt(
        "ACCESS_TOKEN", prompt="ACCESS_TOKEN", secret=True)
    public_base = args.public_base_url or os.environ.get("PUBLIC_BASE_URL") or \
        setup_env.ask("PUBLIC_BASE_URL (ngrok HTTPS)")
    slug = args.business_slug

    # 1) Anahtar çifti
    _print_block("1/5 — RSA anahtar çifti")
    priv = DEFAULT_SECRETS_DIR / "flow_private.pem"
    pub = DEFAULT_SECRETS_DIR / "flow_public.pem"
    if priv.exists() and pub.exists():
        setup_env.ok(f"Mevcut anahtar kullanılacak: {priv.name}, {pub.name}")
    else:
        priv, pub = generate_keypair(DEFAULT_SECRETS_DIR)
        setup_env.ok(f"Üretildi: {priv.name}, {pub.name}")

    # 2) Public key upload
    _print_block("2/5 — Public key Meta'ya yükleniyor")
    pub_pem = read_public_pem(pub)
    up = upload_public_key(pnid, token, pub_pem, api_version=args.api_version)
    if not up.ok:
        print(f"  HTTP {up.status_code}: {up.body}", file=sys.stderr)
        return 1
    setup_env.ok(f"HTTP {up.status_code}")

    # 3) WABA → app subscribe (test number'lar default 'WA DevX' app'ine bağlı)
    _print_block("3/5 — WABA → app webhook subscribe")
    sub = subscribe_app_to_waba(waba, token, api_version=args.api_version)
    if not sub.ok:
        print(f"  HTTP {sub.status_code}: {sub.body}", file=sys.stderr)
        return 1
    setup_env.ok(f"HTTP {sub.status_code}")

    # 4) Flow create + publish
    _print_block("4/5 — Flow yarat + publish")
    try:
        result = create_flow(
            waba_id=waba, access_token=token, public_base_url=public_base,
            flow_name=args.name, api_version=args.api_version,
        )
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1
    if result.validation_errors:
        for err in result.validation_errors:
            print(f"  - {err}")
        setup_env.warn("Validation hataları — publish atlandı.")
        return 1
    publish_note = ""
    if result.publish_status and result.publish_status >= 400:
        publish_note = f" — publish HTTP {result.publish_status} (DRAFT kaldı; test number'da beklenen)"
    setup_env.ok(f"Flow ID: {result.flow_id}{publish_note}")

    # 5) Mongo: PNID + WABA + flow_id business kaydına yazılır
    _print_block(f"5/5 — Mongo update (business_id={slug})")
    try:
        m = update_business_wa_channel(
            slug,
            flow_id=result.flow_id,
            phone_number_id=pnid,
            business_account_id=waba,
        )
    except Exception as e:
        setup_env.warn(f"Mongo update başarısız: {e}")
        return 1
    if m.matched == 0:
        setup_env.warn(f"'{slug}' slug'lı işletme bulunamadı — seed.py'i koş ya da --business-slug ver.")
        return 1
    wa = m.business["channels"]["whatsapp"]
    setup_env.ok(
        f"{m.business['name']} → flow_id={wa.get('flow_id')} "
        f"pnid={wa.get('phone_number_id')} waba={wa.get('business_account_id')}")

    _print_block("Bitti")
    base = public_base.rstrip("/")
    setup_env.hint("Meta Dashboard'a yapıştırılacak URL'ler:")
    print(f"  WA  callback : {setup_env.C.CYAN}{base}/webhooks/whatsapp{setup_env.C.R}")
    print(f"  IG  callback : {setup_env.C.CYAN}{base}/webhooks/instagram{setup_env.C.R}")
    print(f"  Flow endpoint: {setup_env.C.CYAN}{base}/webhooks/whatsapp/flow{setup_env.C.R}  "
          f"{setup_env.C.DIM}(Meta'ya bu komutla zaten yazıldı){setup_env.C.R}")
    print()
    setup_env.hint("Uvicorn açıksa hot-reload picks up; değilse yeniden başlat:")
    print(f"  {setup_env.C.CYAN}.venv/bin/uvicorn app.main:app --reload --port 8000{setup_env.C.R}")
    return 0


def cmd_set_flow_id(args: argparse.Namespace) -> int:
    res = update_business_wa_channel(args.slug, flow_id=args.flow_id)
    if res.matched == 0:
        print(f"UYARI: '{args.slug}' slug'lı işletme bulunamadı.", file=sys.stderr)
        return 1
    wa = res.business["channels"]["whatsapp"]
    print(f"matched={res.matched} modified={res.modified}")
    print(f"  {res.business['name']} → flow_id = {wa.get('flow_id')}")
    return 0


def cmd_gen_test_token(args: argparse.Namespace) -> int:
    token = gen_test_token(args.slug)
    if not token:
        print(f"İşletme bulunamadı: {args.slug}", file=sys.stderr)
        return 1
    print(token)
    return 0


def cmd_test_flow(args: argparse.Namespace) -> int:
    return run_local_flow_test(args.flow_token, args.endpoint)


def cmd_ig_menu(args: argparse.Namespace) -> int:
    import asyncio
    return asyncio.run(run_ig_menu(args.action, args.slug))


def cmd_ig_refresh_token(args: argparse.Namespace) -> int:
    import asyncio
    return asyncio.run(run_ig_token(args.slug))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m scripts",
        description="RandevumOnline Chatbot — yardımcı komutlar",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # setup
    sp = sub.add_parser("setup", help=".env interaktif sihirbazı")
    sp.add_argument("--show", action="store_true", help="Mevcut .env özet")
    sp.add_argument("--section", choices=list(setup_env.SECTIONS),
                    help="Tek bölüm: " + ", ".join(setup_env.SECTIONS))
    sp.set_defaults(func=cmd_setup)

    # gen-keys
    sp = sub.add_parser("gen-keys", help="Flow için RSA çifti üret")
    sp.add_argument("--force", action="store_true",
                    help="Var olan anahtarın üzerine yaz")
    sp.set_defaults(func=cmd_gen_keys)

    # upload-key
    sp = sub.add_parser("upload-key", help="Public key'i Meta'ya yükle")
    sp.add_argument("--phone-number-id", help="env: PHONE_NUMBER_ID")
    sp.add_argument("--access-token", help="env: ACCESS_TOKEN")
    sp.add_argument("--api-version", default="v25.0")
    sp.add_argument("--public-key-path", help="default: secrets/flow_public.pem")
    sp.set_defaults(func=cmd_upload_key)

    # create-flow
    sp = sub.add_parser("create-flow", help="Flow yarat + endpoint bağla + publish")
    sp.add_argument("--waba-id", help="env: WABA_ID")
    sp.add_argument("--access-token", help="env: ACCESS_TOKEN")
    sp.add_argument("--public-base-url", help="env: PUBLIC_BASE_URL")
    sp.add_argument("--name", default="randevu_form_v1", help="Flow adı")
    sp.add_argument("--api-version", default="v25.0")
    sp.set_defaults(func=cmd_create_flow)

    # onboard (chain)
    sp = sub.add_parser(
        "onboard",
        help="Tenant uçtan-uca: keys → upload → subscribe → flow → mongo")
    sp.add_argument("--phone-number-id")
    sp.add_argument("--waba-id")
    sp.add_argument("--access-token")
    sp.add_argument("--public-base-url")
    sp.add_argument("--business-slug", default="berber_mehmet_kutahya",
                    help="Mongo'da güncellenecek business_id (default: berber_mehmet_kutahya)")
    sp.add_argument("--name", default="randevu_form_v1")
    sp.add_argument("--api-version", default="v25.0")
    sp.set_defaults(func=cmd_onboard)

    # set-flow-id
    sp = sub.add_parser("set-flow-id", help="Mongo business.flow_id update")
    sp.add_argument("slug")
    sp.add_argument("flow_id")
    sp.set_defaults(func=cmd_set_flow_id)

    # gen-test-token
    sp = sub.add_parser("gen-test-token",
                        help="Flow Builder Preview için flow_token üret")
    sp.add_argument("slug")
    sp.set_defaults(func=cmd_gen_test_token)

    # test-flow
    sp = sub.add_parser("test-flow",
                        help="Local 6-ekran Flow endpoint simülasyonu")
    sp.add_argument("flow_token")
    sp.add_argument("--endpoint", default=None,
                    help="Flow endpoint URL (default: http://localhost:8000/webhooks/whatsapp/flow)")
    sp.set_defaults(func=cmd_test_flow)

    # ig-menu
    sp = sub.add_parser("ig-menu",
                        help="Instagram persistent menu + ice breakers yönetimi")
    sp.add_argument("action", choices=["set", "get", "delete"],
                    help="set: kur | get: görüntüle | delete: sil")
    sp.add_argument("slug", help="business_id (örn: berber_mehmet_kutahya)")
    sp.set_defaults(func=cmd_ig_menu)

    # ig-refresh-token
    sp = sub.add_parser("ig-refresh-token",
                        help="Instagram uzun ömürlü access token'ı yenile (~60 gün)")
    sp.add_argument("slug", help="business_id (örn: berber_mehmet_kutahya)")
    sp.set_defaults(func=cmd_ig_refresh_token)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
