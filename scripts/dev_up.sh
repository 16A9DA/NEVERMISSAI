#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

docker compose up -d postgres redis chromadb

echo "Waiting for postgres..."
until docker compose exec -T postgres pg_isready -U "${POSTGRES_USER:-nevermiss}" >/dev/null 2>&1; do
  sleep 1
done

pushd backend >/dev/null
.venv/bin/alembic upgrade head
.venv/bin/python ../scripts/seed_demo_data.py
popd >/dev/null

docker compose up backend frontend
