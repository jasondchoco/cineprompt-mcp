# Codex Task Prompts

## Initial repository setup

```text
You are working in the CinePrompt MCP repository.

Read AGENTS.md and docs/plans/v0.1-execution-plan.md first.

Implement Milestone 0 only. Create the repository scaffold, docs, env example, scripts, and CI. Do not implement provider code yet.

After changes:
1. run bash scripts/check.sh if available
2. self-review for secrets, licensing, and data policy
3. update the execution plan
4. summarize the diff and remaining risks
```

## Core schemas

```text
Read AGENTS.md, docs/ARCHITECTURE.md, and docs/plans/v0.1-execution-plan.md.

Implement Milestone 1 only: typed schemas for normalized title/person/reference/prompt data.

Requirements:
- no provider-specific fields leaking into public schemas
- tests for required fields and missing optional fields
- no network tests

Run bash scripts/check.sh.
```

## Provider abstraction

```text
Read AGENTS.md, docs/DATA_POLICY.md, and docs/ARCHITECTURE.md.

Implement Milestone 2 only.

Add a provider interface, deterministic MockProvider, and TMDb provider skeleton.
Do not include API keys.
All unit tests must use MockProvider or mocked HTTP.

Run bash scripts/check.sh.
```

## MCP server tools

```text
Read AGENTS.md and docs/ARCHITECTURE.md.

Implement Milestone 3 only.

Expose MCP tools:
- search_titles
- search_people
- get_title_detail
- get_person_filmography
- build_reference_pack
- check_derivative_risk

Return typed normalized outputs.
Use MockProvider in tests.
Run bash scripts/check.sh and bash scripts/smoke_mcp.sh.
```

## Prompt layer

```text
Read AGENTS.md and docs/PROMPT_SAFETY.md.

Implement Milestone 4 only.

Add MCP prompts:
- cinematic_reference_pack
- video_prompt_from_reference
- shortform_scene_idea
- derivative_risk_check

Add prompt snapshot tests. Ensure final generated prompt instructions avoid actor likeness, exact scenes, character names, franchise terms, and direct style copying.

Run bash scripts/check.sh.
```

## Risk checker

```text
Read AGENTS.md and docs/PROMPT_SAFETY.md.

Implement Milestone 5 only.

Add rule-based derivative-risk checks and output sanitization tests.
Focus on warnings and safer rewrites, not hard censorship except direct clone requests.

Run bash scripts/check.sh.
```
