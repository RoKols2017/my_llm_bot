#!/usr/bin/env bash
set -euo pipefail

PREVIOUS_IMAGE="${1:-}"

if [[ -z "$PREVIOUS_IMAGE" ]]; then
  printf 'Usage: %s <previous-image>\n' "$0" >&2
  exit 1
fi

APP_IMAGE="$PREVIOUS_IMAGE" docker compose -f compose.yml -f compose.production.yml up -d
