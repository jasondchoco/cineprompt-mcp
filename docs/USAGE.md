# Using CinePrompt MCP

This project is an MCP server, not a standalone app. End users should not need MCP
Inspector unless they are testing the server. In normal use, connect it to an MCP
client such as Codex, Claude Desktop, Cursor, or another client that supports stdio
MCP servers.

## 30-second local test

```bash
cd /Users/jason/Documents/CinePrompt
bash scripts/smoke_mcp.sh
```

Expected result:

```text
MCP smoke test passed.
```

## Print copy-paste client config

```bash
cd /Users/jason/Documents/CinePrompt
bash scripts/print_mcp_config.sh
```

The script prints:

- Codex `~/.codex/config.toml` block
- Claude Desktop / Cursor style JSON block
- MCP Inspector command

## Codex CLI

Add this block to `~/.codex/config.toml`. Replace paths only if your checkout lives
somewhere else.

```toml
[mcp_servers.cineprompt]
command = "/opt/anaconda3/bin/uv"
args = ["--directory", "/Users/jason/Documents/CinePrompt", "run", "cineprompt-mcp"]
```

Restart Codex after changing the config.

## Claude Desktop / Cursor style config

Use this shape in the client MCP config file:

```json
{
  "mcpServers": {
    "cineprompt": {
      "command": "/opt/anaconda3/bin/uv",
      "args": [
        "--directory",
        "/Users/jason/Documents/CinePrompt",
        "run",
        "cineprompt-mcp"
      ]
    }
  }
}
```

## MCP Inspector

Inspector is for debugging. It is expected to show a technical UI.

Use:

```text
Transport Type: STDIO
Command: /opt/anaconda3/bin/uv
Arguments: --directory /Users/jason/Documents/CinePrompt run cineprompt-mcp
```

Then click `Connect`.

## Mock-provider examples

The mock provider needs no API key.

Try these tool calls:

```text
search_titles
query: Glass
```

```text
get_title_detail
provider: mock
provider_id: mock-title-1
media_type: movie
```

```text
build_reference_pack
provider: mock
provider_id: mock-title-1
media_type: movie
focus: class pressure
```

```text
check_derivative_risk
text: Make it exactly like a famous survival-game show but in an office.
```

## TMDb provider

TMDb requires a user-supplied key. Do not commit it.

```bash
export CINEPROMPT_PROVIDER=tmdb
export TMDB_API_KEY=your_tmdb_key
uv run cineprompt-mcp
```

In client config, add the env block only for local private use:

```json
{
  "mcpServers": {
    "cineprompt": {
      "command": "/opt/anaconda3/bin/uv",
      "args": [
        "--directory",
        "/Users/jason/Documents/CinePrompt",
        "run",
        "cineprompt-mcp"
      ],
      "env": {
        "CINEPROMPT_PROVIDER": "tmdb",
        "TMDB_API_KEY": "your_tmdb_key"
      }
    }
  }
}
```

## Plain-language prompts to try in a client

After the server is connected, ask the MCP client:

```text
Use CinePrompt to search for Glass and build a cinematic reference pack.
```

```text
Use CinePrompt to check whether this request is too derivative:
"Make the same famous masked survival game scene, but for a corporate training video."
```

```text
Use CinePrompt to turn mock-title-1 into an original 20-second AI video prompt.
```

## Product reality

MCP is an integration layer. For non-technical creators, the right experience is a
small app or hosted workflow that hides all of this configuration. The current v0.1
is ready for MCP-capable tools and developer testing, not public self-serve onboarding.
