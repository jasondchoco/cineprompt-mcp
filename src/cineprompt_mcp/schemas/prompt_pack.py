"""AI video prompt pack schemas."""

from __future__ import annotations

from pydantic import Field

from cineprompt_mcp.schemas.common import CinePromptModel, NonEmptyStr


class VideoPromptPack(CinePromptModel):
    """Final prompt material safe for AI video generation."""

    short_prompt: NonEmptyStr
    long_prompt: NonEmptyStr
    shot_list: list[NonEmptyStr] = Field(min_length=1)
    negative_prompt: list[NonEmptyStr] = Field(default_factory=list)
    derivative_risk_notes: list[NonEmptyStr] = Field(default_factory=list)
