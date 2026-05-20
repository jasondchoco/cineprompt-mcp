"""Provider interface and errors."""

from __future__ import annotations

from typing import Protocol

from cineprompt_mcp.schemas.common import MediaType
from cineprompt_mcp.schemas.person import PersonSearchResult
from cineprompt_mcp.schemas.title import TitleDetail, TitleSearchResult


class ProviderError(RuntimeError):
    """Base provider error."""


class ProviderAuthError(ProviderError):
    """Provider credentials are missing or invalid."""


class ProviderNotFoundError(ProviderError):
    """Provider resource was not found."""


class ProviderUnavailableError(ProviderError):
    """Provider request failed or provider is unavailable."""


class MetadataProvider(Protocol):
    """Public provider contract used by services and MCP tools."""

    name: str

    async def search_titles(
        self,
        query: str,
        media_type: MediaType | None = None,
        year: int | None = None,
        limit: int = 5,
    ) -> list[TitleSearchResult]:
        """Search for movie or TV titles."""

    async def search_people(self, query: str, limit: int = 5) -> list[PersonSearchResult]:
        """Search for people."""

    async def get_title_detail(
        self,
        provider_id: str,
        media_type: MediaType | None = None,
    ) -> TitleDetail:
        """Fetch normalized title detail."""

    async def get_person_filmography(
        self,
        provider_id: str,
        limit: int = 10,
    ) -> list[TitleSearchResult]:
        """Fetch a normalized person filmography."""
