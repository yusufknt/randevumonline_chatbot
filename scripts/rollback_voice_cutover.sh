#!/usr/bin/env bash
set -euo pipefail

cd /home/randevumonline_chatbot
pm2 startOrReload ecosystem.large-test.config.cjs --only randevumonline-voice-large-test --update-env
systemctl stop asterisk
systemctl disable asterisk
pm2 save

curl --fail --silent --show-error http://127.0.0.1:8000/healthz >/dev/null
curl --fail --silent --show-error http://127.0.0.1:9020/ready >/dev/null
ss -lunp | grep -q ':8010 .*python'
echo "voice_recovery=ok"
