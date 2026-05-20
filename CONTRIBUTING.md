# Contributing

CinePrompt MCP is built with small, test-backed changes.

## Development setup

```bash
python -m pip install uv
uv sync --extra dev
```

## Local checks

```bash
bash scripts/check.sh
```

When MCP server behavior changes, also run:

```bash
bash scripts/smoke_mcp.sh
```

## Pull requests

- Keep PRs scoped to one execution-plan task when possible.
- Do not commit API keys, tokens, or personal credentials.
- Do not add permanent fixtures containing full provider payloads or copyrighted synopsis text.
- Mock provider integrations in unit and contract tests.
- Update docs for any public MCP tool, schema, or prompt change.
