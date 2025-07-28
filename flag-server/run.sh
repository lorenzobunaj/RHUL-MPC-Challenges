#!/bin/bash
set -euo pipefail

echo "[+] Flag server listening on port 5000"

exec gunicorn -w 4 -b 0.0.0.0:5000 server:app \
  --access-logfile /dev/null \
  --error-logfile /dev/null \
  --log-level critical