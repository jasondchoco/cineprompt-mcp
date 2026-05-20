"""Typed tool input models."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from cineprompt_mcp.schemas.common import CinePromptModel, MediaType, NonEmptyStr
from cineprompt_mcp.schemas.title import Year

Limit = Annotated[int, Field(ge=1, le=20)]


class SearchTitlesInput(CinePromptModel):
    query: NonEmptyStr
    media_type: MediaType | None = None
    year: Year | None = None
    limit: Limit = 5


class SearchPeopleInput(CinePromptModel):
    query: NonEmptyStr
    limit: Limit = 5


class ProviderTitleInput(CinePromptModel):
    provider: NonEmptyStr
    provider_id: NonEmptyStr
    media_type: MediaType | None = None


class PersonFilmographyInput(CinePromptModel):
    provider: NonEmptyStr
    provider_id: NonEmptyStr
    limit: Limit = 10


class BuildReferencePackInput(CinePromptModel):
    provider: NonEmptyStr
    provider_id: NonEmptyStr
    media_type: MediaType | None = None
    focus: str | None = None


class CheckDerivativeRiskInput(CinePromptModel):
    text: NonEmptyStr
    reference_terms: list[NonEmptyStr] = Field(default_factory=list, max_length=20)
