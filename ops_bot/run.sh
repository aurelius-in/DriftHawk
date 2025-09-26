#!/usr/bin/env bash
set -euo pipefail
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; fi
exec uvicorn ops_bot.app.main:app --host 0.0.0.0 --port 8080
