#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.yml -f compose.production.yml logs -f app
