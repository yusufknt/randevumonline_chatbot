#!/usr/bin/env bash
set -euo pipefail

cd /home/randevumonline_chatbot
./.venv/bin/python scripts/voice_preflight.py
curl --fail --silent --show-error http://127.0.0.1:8000/healthz >/dev/null
curl --fail --silent --show-error http://127.0.0.1:9020/ready >/dev/null
! systemctl is-active --quiet asterisk
ss -lunp | grep -q ':8010 .*python'
! ss -ltn | grep -q ':4573 '
! ss -ltn | grep -q ':9019 '
echo "voice_stack=ok"
