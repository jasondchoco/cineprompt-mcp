#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UV_BIN="$(command -v uv || true)"

if [[ -z "${UV_BIN}" ]]; then
  echo "uv was not found. Install it first:"
  echo "  python -m pip install uv"
  exit 1
fi

cat <<EOF
== Codex ~/.codex/config.toml ==

[mcp_servers.cineprompt]
command = "${UV_BIN}"
args = ["--directory", "${ROOT_DIR}", "run", "cineprompt-mcp"]

== Claude Desktop / Cursor JSON ==

{
  "mcpServers": {
    "cineprompt": {
      "command": "${UV_BIN}",
      "args": [
        "--directory",
        "${ROOT_DIR}",
        "run",
        "cineprompt-mcp"
      ]
    }
  }
}

== MCP Inspector ==

Transport Type: STDIO
Command: ${UV_BIN}
Arguments: --directory ${ROOT_DIR} run cineprompt-mcp

== Quick mock test ==

Tool: search_titles
Arguments:
{
  "query": "Glass"
}
EOF
