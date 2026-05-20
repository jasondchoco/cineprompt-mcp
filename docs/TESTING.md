# Testing Strategy

## Test layers

1. Unit tests
   - schema validation
   - normalizer logic
   - prompt-safety transformations
   - reference-pack builder

2. Provider contract tests
   - mocked HTTP response fixtures
   - error handling
   - missing field handling
   - attribution handling

3. Prompt snapshot tests
   - stable structure
   - required sections present
   - prohibited terms removed

4. MCP smoke tests
   - server starts
   - tools list
   - prompts list
   - one mock search call
   - one prompt generation call

5. CLI check

```bash
bash scripts/check.sh
```

MCP smoke:

```bash
bash scripts/smoke_mcp.sh
```

## Network policy

CI tests should not require live provider access.

Live API tests must be opt-in:

```bash
RUN_LIVE_PROVIDER_TESTS=1 pytest tests/live
```

## Minimum quality gate

- formatting passes
- lint passes
- type check passes
- unit tests pass
- smoke test passes
