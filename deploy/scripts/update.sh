#!/usr/bin/env bash
set -euo pipefail

./deploy/scripts/backup.sh
docker compose -f compose.yml -f compose.production.yml pull
docker compose -f compose.yml -f compose.production.yml up -d
./deploy/scripts/health-check.sh
