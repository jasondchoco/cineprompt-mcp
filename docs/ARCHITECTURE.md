# Architecture

## Core design

CinePrompt MCP separates provider data retrieval from creative transformation.

```text
MCP Client
  → MCP Server
    → Tools
      → Provider adapters
      → Normalizer
      → Reference pack builder
      → Risk checker
    → Prompts
      → reference pack template
      → video prompt template
      → short-form scene template
```

## Packages

```text
src/cineprompt_mcp/
  server.py
  config.py
  tools.py
  schemas/
    title.py
    person.py
    reference_pack.py
    prompt_pack.py
    risk.py
    tools.py
  providers/
    base.py
    tmdb.py
    mock.py
  services/
    reference_pack_builder.py
    prompt_builder.py
    prompt_safety.py
    provider_registry.py
  prompts/
    cinematic_reference_pack.py
    video_prompt_from_reference.py
    shortform_scene_idea.py
    derivative_risk_check.py
```

## Boundary rules

Provider adapters may return raw provider fields internally, but MCP tools should return normalized schemas.

No permanent cache of full synopsis text in v0.1.

KMDb and KOBIS are v0.2 candidates after the provider abstraction and TMDb integration are stable.

## MCP surface

### Tools

- `search_titles`
- `search_people`
- `get_title_detail`
- `get_person_filmography`
- `build_reference_pack`
- `check_derivative_risk`

### Prompts

- `cinematic_reference_pack`
- `video_prompt_from_reference`
- `shortform_scene_idea`
- `derivative_risk_check`

## Dependency direction

```text
server -> tools
tools -> services
tools -> providers
server -> prompts
services -> schemas
providers -> schemas
```

Schemas must not import providers.
