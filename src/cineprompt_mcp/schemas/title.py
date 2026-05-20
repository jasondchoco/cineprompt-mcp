"""Title-related public schemas."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from pydantic import Field

from cineprompt_mcp.schemas.common import (
    CinePromptModel,
    MediaType,
    NonEmptyStr,
    ProviderAttribution,
)

Year = Annotated[int, Field(ge=1878, le=2100)]


class TitleSearchResult(CinePromptModel):
    """Normalized title search result returned by public tools."""

    provider: NonEmptyStr
    provider_id: NonEmptyStr
    media_type: MediaType
    title: NonEmptyStr
    original_title: str | None = None
    year: Year | None = None
    release_date: date | None = None
    overview_hint: str | None = Field(default=None, max_length=600)
    genres: list[NonEmptyStr] = Field(default_factory=list)
    attribution: ProviderAttribution


class TitleDetail(CinePromptModel):
    """Normalized detail for a movie or TV title."""

    provider: NonEmptyStr
    provider_id: NonEmptyStr
    media_type: MediaType
    title: NonEmptyStr
    original_title: str | None = None
    year: Year | None = None
    release_date: date | None = None
    runtime_minutes: Annotated[int, Field(ge=1, le=1000)] | None = None
    genres: list[NonEmptyStr] = Field(default_factory=list)
    overview_summary: str | None = Field(default=None, max_length=1200)
    directors: list[NonEmptyStr] = Field(default_factory=list)
    creators: list[NonEmptyStr] = Field(default_factory=list)
    cast: list[NonEmptyStr] = Field(default_factory=list, max_length=20)
    keywords: list[NonEmptyStr] = Field(default_factory=list, max_length=30)
    production_countries: list[NonEmptyStr] = Field(default_factory=list)
    attribution: ProviderAttribution
