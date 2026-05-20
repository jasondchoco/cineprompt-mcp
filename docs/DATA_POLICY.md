# Data Policy

## Principles

- Use official APIs where possible.
- Require users to supply their own API keys.
- Do not commit API keys.
- Avoid storing original synopsis text.
- Prefer analysis and transformation over republication.
- Keep provider attribution visible.

## Provider strategy

### v0.1

- TMDb: primary global provider via user-supplied key.
- Mock provider: deterministic tests and demos.
- KMDb: optional Korean film provider, introduced after core provider abstraction is stable.

### v0.2

- KOBIS support for Korean movie metadata.
- Multi-provider merge and source attribution.

## Caching

v0.1 should avoid persistent caching of full provider payloads.

Allowed:

- in-memory cache for current process
- redacted test fixtures
- normalized minimal metadata fixtures

Not allowed:

- permanent database of synopses
- poster/still image re-hosting
- storing provider API keys in files other than `.env`, which is gitignored
