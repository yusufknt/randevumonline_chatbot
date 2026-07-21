#!/usr/bin/env bash
set -euo pipefail

cd /home/randevumonline_chatbot
pm2 stop randevumonline >/dev/null 2>&1 || true
pm2 start ecosystem.config.cjs --only randevumonline-api,randevumonline-voice
systemctl start asterisk
pm2 save

curl --fail --silent --show-error http://127.0.0.1:8000/healthz >/dev/null
curl --fail --silent --show-error http://127.0.0.1:9020/ready >/dev/null
ss -lunp | grep -q ':8010 .*asterisk'
echo "voice_recovery=ok"
