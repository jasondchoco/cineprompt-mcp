"""Cinematic reference pack prompt template."""

from __future__ import annotations


def cinematic_reference_pack(title_or_query: str, focus: str | None = None) -> str:
    """Prompt that guides a client/model to build a reference pack."""

    focus_line = f"\nFocus the analysis on: {focus}." if focus else ""
    return f"""Build an original cinematic reference pack for: {title_or_query}.{focus_line}

Use CinePrompt MCP tools to search and fetch normalized metadata first.
Translate the reference into:
- neutral metadata summary
- story engine
- character desire and conflict
- genre mechanics
- camera, lighting, color, space, and editing language
- derivative-risk notes

Do not ask for exact scene recreation, actor likeness, named characters, copied dialogue,
franchise identifiers, or the title as a direct style instruction."""
