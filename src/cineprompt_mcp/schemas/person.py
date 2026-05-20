"""Person-related public schemas."""

from __future__ import annotations

from pydantic import Field

from cineprompt_mcp.schemas.common import CinePromptModel, NonEmptyStr, ProviderAttribution


class PersonSearchResult(CinePromptModel):
    """Normalized person search result returned by public tools."""

    provider: NonEmptyStr
    provider_id: NonEmptyStr
    name: NonEmptyStr
    known_for_department: str | None = None
    known_for_titles: list[NonEmptyStr] = Field(default_factory=list, max_length=10)
    attribution: ProviderAttribution
