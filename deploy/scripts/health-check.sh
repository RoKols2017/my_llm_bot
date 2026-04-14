#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.yml -f compose.production.yml ps
docker compose -f compose.yml -f compose.production.yml exec app python -c "import bot.main"
