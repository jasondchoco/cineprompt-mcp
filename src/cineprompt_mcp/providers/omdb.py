"""OMDb provider implementation."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

import httpx

from cineprompt_mcp.providers.base import (
    ProviderAuthError,
    ProviderNotFoundError,
    ProviderUnavailableError,
)
from cineprompt_mcp.schemas.common import MediaType, ProviderAttribution
from cineprompt_mcp.schemas.person import PersonSearchResult
from cineprompt_mcp.schemas.title import TitleDetail, TitleSearchResult

OMDB_ATTRIBUTION = "Movie and TV data provided by OMDb API (omdbapi.com)."
OMDB_BASE_URL = "http://www.omdbapi.com/"

# OMDb type values to internal MediaType
_TYPE_MAP: dict[str, MediaType] = {
    "movie": "movie",
    "series": "tv",
}


class OMDbProvider:
    """OMDb API provider using a user-supplied API key."""

    name = "omdb"

    def __init__(
        self,
        api_key: str | None,
        base_url: str = OMDB_BASE_URL,
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout
        self._transport = transport

    async def search_titles(
        self,
        query: str,
        media_type: MediaType | None = None,
        year: int | None = None,
        limit: int = 5,
    ) -> list[TitleSearchResult]:
        omdb_type = "movie" if media_type == "movie" else "series" if media_type == "tv" else None
        params: dict[str, str | int] = {"s": query}
        if omdb_type is not None:
            params["type"] = omdb_type
        if year is not None:
            params["y"] = year
        data = await self._get(params)
        if data.get("Response") == "False":
            return []
        results: list[TitleSearchResult] = []
        for item in data.get("Search", []):
            if not isinstance(item, dict):
                continue
            mapped = self._map_search_item(item, media_type)
            if mapped is not None:
                results.append(mapped)
            if len(results) >= limit:
                break
        return results

    async def search_people(self, query: str, limit: int = 5) -> list[PersonSearchResult]:
        # OMDb does not provide a person search endpoint.
        return []

    async def get_title_detail(
        self,
        provider_id: str,
        media_type: MediaType | None = None,
    ) -> TitleDetail:
        params: dict[str, str] = {"i": provider_id, "plot": "full"}
        data = await self._get(params)
        if data.get("Response") == "False":
            raise ProviderNotFoundError(f"OMDb title not found: {provider_id}")
        return self._map_title_detail(data)

    async def get_person_filmography(
        self,
        provider_id: str,
        limit: int = 10,
    ) -> list[TitleSearchResult]:
        # OMDb does not provide a person filmography endpoint.
        return []

    async def _get(self, params: dict[str, str | int]) -> dict[str, Any]:
        if not self._api_key:
            raise ProviderAuthError("OMDB_API_KEY is required for the OMDb provider.")
        request_params: dict[str, str | int] = {"apikey": self._api_key}
        request_params.update(params)
        async with httpx.AsyncClient(
            timeout=self._timeout,
            transport=self._transport,
        ) as client:
            try:
                response = await client.get(self._base_url, params=request_params)
            except httpx.HTTPError as exc:
                raise ProviderUnavailableError(f"OMDb request failed: {exc}") from exc
        if response.status_code == 401:
            raise ProviderAuthError("OMDb rejected the configured API key.")
        if response.status_code >= 400:
            raise ProviderUnavailableError(f"OMDb request failed with HTTP {response.status_code}.")
        payload = response.json()
        if not isinstance(payload, dict):
            raise ProviderUnavailableError("OMDb returned an unexpected payload.")
        if payload.get("Error") in {"Invalid API key!", "Request limit reached!"}:
            raise ProviderAuthError(f"OMDb auth error: {payload['Error']}")
        return payload

    def _map_search_item(
        self,
        item: dict[str, Any],
        requested_media_type: MediaType | None,
    ) -> TitleSearchResult | None:
        omdb_type = str(item.get("Type", "")).lower()
        media_type: MediaType | None = _TYPE_MAP.get(omdb_type)
        if media_type is None:
            media_type = requested_media_type
        if media_type not in {"movie", "tv"}:
            return None
        provider_id = str(item.get("imdbID", "")).strip()
        title = str(item.get("Title", "")).strip()
        if not provider_id or not title:
            return None
        year = _parse_year(item.get("Year"))
        return TitleSearchResult(
            provider=self.name,
            provider_id=provider_id,
            media_type=media_type,
            title=title,
            year=year,
            genres=[],
            attribution=self._attribution(provider_id),
        )

    def _map_title_detail(self, data: dict[str, Any]) -> TitleDetail:
        provider_id = str(data.get("imdbID", "")).strip()
        title = str(data.get("Title", "")).strip()
        if not provider_id or not title:
            raise ProviderUnavailableError("OMDb title detail was missing required fields.")
        omdb_type = str(data.get("Type", "")).lower()
        media_type: MediaType = _TYPE_MAP.get(omdb_type, "movie")
        year = _parse_year(data.get("Year"))
        release_date = _parse_release_date(data.get("Released"))
        runtime_minutes = _parse_runtime(data.get("Runtime"))
        genres = _split_csv(data.get("Genre"))
        directors = _split_csv(data.get("Director"))
        writers = _split_csv(data.get("Writer"))
        cast = _split_csv(data.get("Actors"))
        country_raw = _split_csv(data.get("Country"))
        production_countries = [c.strip()[:2].upper() for c in country_raw if c.strip()]
        overview = str(data.get("Plot", "")).strip() or None
        if overview == "N/A":
            overview = None
        return TitleDetail(
            provider=self.name,
            provider_id=provider_id,
            media_type=media_type,
            title=title,
            year=year,
            release_date=release_date,
            runtime_minutes=runtime_minutes,
            genres=genres,
            overview_summary=overview,
            directors=directors,
            creators=writers,
            cast=cast[:20],
            keywords=[],
            production_countries=production_countries,
            attribution=self._attribution(provider_id),
        )

    def _attribution(self, provider_id: str) -> ProviderAttribution:
        return ProviderAttribution(
            provider=self.name,
            provider_id=provider_id,
            source_url=f"https://www.imdb.com/title/{provider_id}/",
            license_note=OMDB_ATTRIBUTION,
        )


def _parse_year(value: object) -> int | None:
    if not isinstance(value, str):
        return None
    match = re.search(r"\b(\d{4})\b", value)
    if match:
        year = int(match.group(1))
        if 1878 <= year <= 2100:
            return year
    return None


def _parse_release_date(value: object) -> date | None:
    if not isinstance(value, str) or not value or value == "N/A":
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        pass
    import time
    for fmt in ("%d %b %Y", "%b %Y", "%Y"):
        try:
            t = time.strptime(value, fmt)
            if fmt == "%Y":
                return date(t.tm_year, 1, 1)
            return date(t.tm_year, t.tm_mon, t.tm_mday)
        except ValueError:
            continue
    return None


def _parse_runtime(value: object) -> int | None:
    if not isinstance(value, str) or value == "N/A":
        return None
    match = re.search(r"(\d+)", value)
    return int(match.group(1)) if match else None


def _split_csv(value: object) -> list[str]:
    if not isinstance(value, str) or not value or value == "N/A":
        return []
    return [part.strip() for part in value.split(",") if part.strip()]
