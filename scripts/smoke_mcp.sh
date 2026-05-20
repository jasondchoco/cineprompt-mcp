#!/usr/bin/env bash
set -euo pipefail

echo "== MCP smoke test =="

if command -v uv >/dev/null 2>&1; then
  uv run cineprompt-mcp-smoke
else
  python -m cineprompt_mcp.smoke
fi
