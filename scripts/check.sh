#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

uv lock --check
uv run --locked ruff format --check crew/data_platform crew/yields web tests/data_platform
uv run --locked ruff check --fix --diff crew/data_platform/registry.py
uv run --locked pyrefly check
uv run --locked pytest tests/data_platform -q
node --check web/static/site.js
