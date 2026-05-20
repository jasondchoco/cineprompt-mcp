#!/usr/bin/env bash
set -euo pipefail

echo "== CinePrompt MCP quality gate =="

if command -v uv >/dev/null 2>&1; then
  uv sync --extra dev
  uv run ruff check .
  uv run ruff format --check .
  uv run mypy src
  uv run pytest
else
  echo "uv not found. Install uv or adapt this script to your environment."
  python -m ruff check .
  python -m ruff format --check .
  python -m mypy src
  python -m pytest
fi
