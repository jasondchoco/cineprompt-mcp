"""Shared public schema primitives."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
MediaType = Literal["movie", "tv"]
RiskLevel = Literal["low", "medium", "high", "block"]


class CinePromptModel(BaseModel):
    """Base model for public CinePrompt payloads."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, validate_assignment=True)

    def to_public_dict(self) -> dict[str, object]:
        """Return a JSON-safe public representation without null fields."""

        return self.model_dump(mode="json", exclude_none=True)


class ProviderAttribution(CinePromptModel):
    """Visible attribution for normalized provider-derived data."""

    provider: NonEmptyStr
    provider_id: NonEmptyStr
    source_url: str | None = None
    license_note: str | None = None


class VisualLanguage(CinePromptModel):
    """Cinematic language extracted from a reference without copying expression."""

    camera: list[NonEmptyStr] = Field(default_factory=list)
    lighting: list[NonEmptyStr] = Field(default_factory=list)
    color: list[NonEmptyStr] = Field(default_factory=list)
    space: list[NonEmptyStr] = Field(default_factory=list)
    editing: list[NonEmptyStr] = Field(default_factory=list)
