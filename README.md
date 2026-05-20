# CinePrompt MCP

Open-source MCP server for filmmakers, AI video creators, and storytellers.

CinePrompt MCP retrieves movie/TV metadata from supported providers and turns it into structured creative reference packs, cinematic prompt templates, shot lists, and derivative-risk warnings.

## Product thesis

AI video creators do not only need summaries. They need story structure, visual language, shot-level prompts, and safeguards against copying existing works.

Core flow:

```text
reference title/person
→ metadata + synopsis
→ story engine
→ visual language
→ AI video prompt pack
→ derivative-risk check
```

## Initial scope: v0.1

- TMDb provider, using user-supplied API key
- Mock provider for deterministic tests and demos
- MCP tools for title/person search, title detail lookup, person filmography, reference packs, and derivative-risk checks
- MCP prompts for cinematic reference packs and AI video prompt generation
- Unit tests, provider contract tests, prompt snapshot tests
- MCP Inspector smoke-test script
- Codex/Ralph-compatible development harness

## Non-goals

- Do not store or redistribute a synopsis database.
- Do not scrape pages that prohibit scraping.
- Do not clone copyrighted characters, scenes, dialogue, or franchise elements.
- Do not include provider API keys in the repository.

## Attribution

Add the required attribution for each enabled provider in the final README.

For TMDb, include:

```text
This product uses the TMDB API but is not endorsed or certified by TMDB.
```

## Install

```bash
python -m pip install uv
uv sync --extra dev
```

## Configuration

Copy `.env.example` to `.env` for local development. The default provider is `mock`, which requires no credentials.

```bash
CINEPROMPT_PROVIDER=mock
TMDB_API_KEY=
```

To use TMDb:

```bash
CINEPROMPT_PROVIDER=tmdb
TMDB_API_KEY=your_tmdb_key
```

Do not commit `.env` or provider keys.

## Run the MCP server

```bash
uv run cineprompt-mcp
```

The server runs over stdio for MCP clients.

## Tools

- `search_titles(query, media_type?, year?, limit?)`
- `search_people(query, limit?)`
- `get_title_detail(provider, provider_id, media_type?)`
- `get_person_filmography(provider, provider_id, limit?)`
- `build_reference_pack(provider, provider_id, media_type?, focus?)`
- `check_derivative_risk(text, reference_terms?)`

## Prompts

- `cinematic_reference_pack`
- `video_prompt_from_reference`
- `shortform_scene_idea`
- `derivative_risk_check`

## Checks

```bash
bash scripts/check.sh
bash scripts/smoke_mcp.sh
```

Live provider tests are opt-in and are not part of CI:

```bash
RUN_LIVE_PROVIDER_TESTS=1 pytest tests/live
```
