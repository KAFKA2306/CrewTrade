#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

python -m compileall -q web
node --check web/static/site.js
uv run --no-project --with markdown --with jinja2 python web/build_static.py
uv run --no-project python web/audit_static.py
uv run --no-project --with markdown --with jinja2 python web/build_data_status.py
uv run --no-project python web/audit_data_status.py
