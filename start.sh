#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-10000}"
WEB_CONCURRENCY="${WEB_CONCURRENCY:-1}"

exec gunicorn app:app \
  --bind "0.0.0.0:${PORT}" \
  --workers "${WEB_CONCURRENCY}" \
  --timeout 120 \
  --access-logfile -
