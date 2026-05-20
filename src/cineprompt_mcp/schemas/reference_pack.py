"""Reference pack schemas."""

from __future__ import annotations

from pydantic import Field

from cineprompt_mcp.schemas.common import (
    CinePromptModel,
    NonEmptyStr,
    ProviderAttribution,
    VisualLanguage,
)
from cineprompt_mcp.schemas.title import TitleDetail


class ReferencePack(CinePromptModel):
    """Originality-focused creative analysis derived from normalized metadata."""

    reference: TitleDetail
    summary: NonEmptyStr
    story_engine: NonEmptyStr
    character_dynamics: list[NonEmptyStr] = Field(default_factory=list)
    genre_mechanics: list[NonEmptyStr] = Field(default_factory=list)
    visual_language: VisualLanguage
    prompt_hooks: list[NonEmptyStr] = Field(default_factory=list)
    risk_notes: list[NonEmptyStr] = Field(default_factory=list)
    attribution: list[ProviderAttribution]
