#!/usr/bin/env bash
# Despliegue local o en PaaS con Python 3.10+
set -euo pipefail
cd "$(dirname "$0")"

python3 run.py init
exec python3 run.py
