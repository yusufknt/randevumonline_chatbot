#!/usr/bin/env bash
# MongoDB 8.0 kurulumu — apt resmi reposu (sudo gerekir).
# `mongodb-org` metapaketi mongod + mongosh'u PATH'e koyar.
# Idempotent: zaten kuruluysa atlar. Sonunda başlat/durdur talimatı verir.
set -euo pipefail

DATA_DIR="${HOME}/data/db"
LOG_FILE="${HOME}/data/mongod.log"

have() { command -v "$1" >/dev/null 2>&1; }

start_hint() {
  echo ""
  echo "Veri dizini: ${DATA_DIR}"
  echo "Başlatmak için:"
  echo "  mongod --dbpath ${DATA_DIR} --port 27017 --fork --logpath ${LOG_FILE}"
  echo "Doğrulamak için:"
  echo "  mongosh --quiet --eval 'db.runCommand({ping:1})'"
  echo "Durdurmak için:"
  echo "  mongod --dbpath ${DATA_DIR} --shutdown"
}

mkdir -p "${DATA_DIR}"

# Zaten kurulu mu?
if have mongod; then
  echo "==> mongod zaten PATH'te: $(command -v mongod) ($(mongod --version | head -1))"
  start_hint
  exit 0
fi

# sudo şart
if ! have sudo; then
  echo "HATA: apt kurulumu için 'sudo' gerekir, bulunamadı." >&2
  exit 1
fi

echo "==> apt ile kurulum (sudo)..."
KEYRING=/usr/share/keyrings/mongodb-server-8.0.gpg
LIST=/etc/apt/sources.list.d/mongodb-org-8.0.list
if [ ! -f "${KEYRING}" ]; then
  echo "==> GPG anahtarı ekleniyor..."
  curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc \
    | sudo gpg -o "${KEYRING}" --dearmor
fi
if [ ! -f "${LIST}" ]; then
  echo "==> Repo ekleniyor (noble paketi)..."
  echo "deb [ arch=amd64,arm64 signed-by=${KEYRING} ] \
https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" \
    | sudo tee "${LIST}" >/dev/null
fi
echo "==> apt update + install..."
sudo apt-get update -qq
sudo apt-get install -y mongodb-org
echo "==> Kurulum tamam (apt)."
start_hint
