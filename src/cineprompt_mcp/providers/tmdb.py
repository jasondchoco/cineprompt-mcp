"""TMDb provider implementation."""

from __future__ import annotations

from datetime import date
from typing import Any, TypeAlias

import httpx

from cineprompt_mcp.providers.base import (
    ProviderAuthError,
    ProviderNotFoundError,
    ProviderUnavailableError,
)
from cineprompt_mcp.schemas.common import MediaType, ProviderAttribution
from cineprompt_mcp.schemas.person import PersonSearchResult
from cineprompt_mcp.schemas.title import TitleDetail, TitleSearchResult

TMDB_ATTRIBUTION = "This product uses the TMDB API but is not endorsed or certified by TMDB."
QueryParam: TypeAlias = str | int | float | bool | None


class TMDbProvider:
    """TMDb API provider using a user-supplied API key."""

    name = "tmdb"

    def __init__(
        self,
        api_key: str | None,
        base_url: str = "https://api.themoviedb.org/3",
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._transport = transport

    async def search_titles(
        self,
        query: str,
        media_type: MediaType | None = None,
        year: int | None = None,
        limit: int = 5,
    ) -> list[TitleSearchResult]:
        endpoint = "/search/multi" if media_type is None else f"/search/{media_type}"
        params: dict[str, QueryParam] = {"query": query, "include_adult": "false", "page": 1}
        if year is not None:
            if media_type == "tv":
                params["first_air_date_year"] = year
            elif media_type == "movie":
                params["year"] = year
        data = await self._get(endpoint, params=params)
        items = data.get("results", [])
        results: list[TitleSearchResult] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            mapped = self._map_search_title(item, media_type)
            if mapped is not None:
                results.append(mapped)
            if len(results) >= limit:
                break
        return results

    async def search_people(self, query: str, limit: int = 5) -> list[PersonSearchResult]:
        data = await self._get(
            "/search/person",
            params={"query": query, "include_adult": "false", "page": 1},
        )
        people: list[PersonSearchResult] = []
        for item in data.get("results", []):
            if not isinstance(item, dict):
                continue
            provider_id = str(item.get("id", "")).strip()
            name = str(item.get("name", "")).strip()
            if not provider_id or not name:
                continue
            known_for_titles = [
                self._display_title(known_for)
                for known_for in item.get("known_for", [])
                if isinstance(known_for, dict) and self._display_title(known_for)
            ]
            people.append(
                PersonSearchResult(
                    provider=self.name,
                    provider_id=provider_id,
                    name=name,
                    known_for_department=item.get("known_for_department"),
                    known_for_titles=known_for_titles[:10],
                    attribution=self._attribution(provider_id, "person"),
                )
            )
            if len(people) >= limit:
                break
        return people

    async def get_title_detail(
        self,
        provider_id: str,
        media_type: MediaType | None = None,
    ) -> TitleDetail:
        resolved_media_type = media_type or "movie"
        data = await self._get(
            f"/{resolved_media_type}/{provider_id}",
            params={"append_to_response": "credits,keywords"},
        )
        return self._map_title_detail(data, resolved_media_type)

    async def get_person_filmography(
        self,
        provider_id: str,
        limit: int = 10,
    ) -> list[TitleSearchResult]:
        data = await self._get(f"/person/{provider_id}/combined_credits")
        items = [
            item for item in data.get("cast", []) + data.get("crew", []) if isinstance(item, dict)
        ]
        items.sort(key=lambda item: float(item.get("popularity") or 0), reverse=True)
        results: list[TitleSearchResult] = []
        seen: set[tuple[str, str]] = set()
        for item in items:
            mapped = self._map_search_title(item, None)
            if mapped is None:
                continue
            key = (mapped.media_type, mapped.provider_id)
            if key in seen:
                continue
            seen.add(key)
            results.append(mapped)
            if len(results) >= limit:
                break
        return results

    async def _get(self, path: str, params: dict[str, QueryParam] | None = None) -> dict[str, Any]:
        if not self._api_key:
            raise ProviderAuthError("TMDB_API_KEY is required for the TMDb provider.")
        request_params: dict[str, QueryParam] = {"api_key": self._api_key}
        request_params.update(params or {})
        async with httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            transport=self._transport,
        ) as client:
            try:
                response = await client.get(path, params=request_params)
            except httpx.HTTPError as exc:
                raise ProviderUnavailableError(f"TMDb request failed: {exc}") from exc
        if response.status_code in {401, 403}:
            raise ProviderAuthError("TMDb rejected the configured API key.")
        if response.status_code == 404:
            raise ProviderNotFoundError(f"TMDb resource not found: {path}")
        if response.status_code >= 400:
            raise ProviderUnavailableError(f"TMDb request failed with HTTP {response.status_code}.")
        payload = response.json()
        if not isinstance(payload, dict):
            raise ProviderUnavailableError("TMDb returned an unexpected payload.")
        return payload

    def _map_search_title(
        self,
        item: dict[str, Any],
        requested_media_type: MediaType | None,
    ) -> TitleSearchResult | None:
        media_type = item.get("media_type") or requested_media_type
        if media_type not in {"movie", "tv"}:
            return None
        provider_id = str(item.get("id", "")).strip()
        title = self._display_title(item)
        if not provider_id or not title:
            return None
        release_date = _parse_date(item.get("release_date") or item.get("first_air_date"))
        return TitleSearchResult(
            provider=self.name,
            provider_id=provider_id,
            media_type=media_type,
            title=title,
            original_title=item.get("original_title") or item.get("original_name"),
            year=release_date.year if release_date else None,
            release_date=release_date,
            overview_hint=item.get("overview") or None,
            genres=[],
            attribution=self._attribution(provider_id, media_type),
        )

    def _map_title_detail(self, data: dict[str, Any], media_type: MediaType) -> TitleDetail:
        provider_id = str(data.get("id", "")).strip()
        title = self._display_title(data)
        if not provider_id or not title:
            raise ProviderUnavailableError("TMDb title detail was missing required fields.")
        release_date = _parse_date(data.get("release_date") or data.get("first_air_date"))
        credits = data.get("credits") if isinstance(data.get("credits"), dict) else {}
        crew = credits.get("crew", []) if isinstance(credits, dict) else []
        cast = credits.get("cast", []) if isinstance(credits, dict) else []
        directors = [
            str(member.get("name")).strip()
            for member in crew
            if isinstance(member, dict) and member.get("job") == "Director" and member.get("name")
        ]
        creators = [
            str(member.get("name")).strip()
            for member in data.get("created_by", [])
            if isinstance(member, dict) and member.get("name")
        ]
        keywords_data = data.get("keywords")
        keyword_items: list[Any] = []
        if isinstance(keywords_data, dict):
            raw_keywords = keywords_data.get("keywords") or keywords_data.get("results") or []
            if isinstance(raw_keywords, list):
                keyword_items = raw_keywords
        return TitleDetail(
            provider=self.name,
            provider_id=provider_id,
            media_type=media_type,
            title=title,
            original_title=data.get("original_title") or data.get("original_name"),
            year=release_date.year if release_date else None,
            release_date=release_date,
            runtime_minutes=data.get("runtime") or _first_int(data.get("episode_run_time")),
            genres=[
                str(genre.get("name")).strip()
                for genre in data.get("genres", [])
                if isinstance(genre, dict) and genre.get("name")
            ],
            overview_summary=data.get("overview") or None,
            directors=directors[:10],
            creators=creators[:10],
            cast=[
                str(member.get("name")).strip()
                for member in cast
                if isinstance(member, dict) and member.get("name")
            ][:20],
            keywords=[
                str(keyword.get("name")).strip()
                for keyword in keyword_items
                if isinstance(keyword, dict) and keyword.get("name")
            ][:30],
            production_countries=[
                str(country.get("iso_3166_1")).strip()
                for country in data.get("production_countries", [])
                if isinstance(country, dict) and country.get("iso_3166_1")
            ],
            attribution=self._attribution(provider_id, media_type),
        )

    def _attribution(self, provider_id: str, kind: str) -> ProviderAttribution:
        url_kind = "movie" if kind == "movie" else "tv" if kind == "tv" else "person"
        return ProviderAttribution(
            provider=self.name,
            provider_id=provider_id,
            source_url=f"https://www.themoviedb.org/{url_kind}/{provider_id}",
            license_note=TMDB_ATTRIBUTION,
        )

    @staticmethod
    def _display_title(item: dict[str, Any]) -> str:
        return str(item.get("title") or item.get("name") or "").strip()


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _first_int(value: object) -> int | None:
    if isinstance(value, list) and value and isinstance(value[0], int):
        return value[0]
    return None
