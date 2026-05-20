# AGENTS.md

This repository is optimized for agent-assisted development.

## Project

CinePrompt MCP is an open-source MCP server that turns movie/TV metadata into AI video creation reference packs and prompt templates.

## Read first

Before editing code, read:

1. `docs/PRODUCT_SPEC.md`
2. `docs/ARCHITECTURE.md`
3. `docs/DATA_POLICY.md`
4. `docs/PROMPT_SAFETY.md`
5. `docs/TESTING.md`
6. Current active plan in `docs/plans/`

## Hard rules

- Never commit API keys, tokens, or personal credentials.
- Do not store provider response payloads as permanent fixtures unless redacted and license-safe.
- Unit tests must not require network access.
- Provider integrations must be mocked in unit tests.
- Final video prompts must not include copyrighted character names, actor likeness requests, exact scene recreation, or franchise identifiers.
- Any new tool must have:
  - typed input schema
  - typed output model
  - happy-path test
  - failure-path test
  - documentation update

## Quality gate

Run before proposing completion:

```bash
bash scripts/check.sh
```

If MCP server behavior changed, also run:

```bash
bash scripts/smoke_mcp.sh
```

## Development loop

For each iteration:

1. Pick exactly one unchecked task from the active execution plan.
2. Implement the smallest useful change.
3. Run the quality gate.
4. Self-review the diff for security, data policy, and prompt-safety issues.
5. Update the execution plan and decision log.
6. Stop if the task is ambiguous, blocked by provider credentials, or would require violating data policy.

## Review guidelines

Prioritize P0/P1 comments only:

- broken MCP protocol behavior
- provider key leakage
- unsafe prompt outputs
- permanent storage of copyrighted synopsis text
- tests that depend on live external services
- undocumented public tool/schema changes
