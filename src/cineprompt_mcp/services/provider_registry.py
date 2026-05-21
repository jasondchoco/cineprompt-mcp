"""Provider selection helpers."""

from __future__ import annotations

from cineprompt_mcp.config import Settings, load_settings
from cineprompt_mcp.providers.base import MetadataProvider, ProviderNotFoundError
from cineprompt_mcp.providers.mock import MockProvider
from cineprompt_mcp.providers.omdb import OMDbProvider
from cineprompt_mcp.providers.tmdb import TMDbProvider


class ProviderRegistry:
    """Lazy provider registry for MCP tool calls."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or load_settings()
        self._mock = MockProvider()
        self._tmdb: TMDbProvider | None = None
        self._omdb: OMDbProvider | None = None

    def get(self, name: str | None = None) -> MetadataProvider:
        provider_name = (name or self._settings.default_provider).strip().lower()
        if provider_name == "mock":
            return self._mock
        if provider_name == "tmdb":
            if self._tmdb is None:
                self._tmdb = TMDbProvider(
                    api_key=self._settings.tmdb_api_key,
                    base_url=self._settings.tmdb_base_url,
                )
            return self._tmdb
        if provider_name == "omdb":
            if self._omdb is None:
                self._omdb = OMDbProvider(
                    api_key=self._settings.omdb_api_key,
                    base_url=self._settings.omdb_base_url,
                )
            return self._omdb
        raise ProviderNotFoundError(f"Unsupported provider: {provider_name}")
