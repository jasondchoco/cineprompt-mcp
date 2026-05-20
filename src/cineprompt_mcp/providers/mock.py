"""Deterministic mock provider for tests and demos."""

from __future__ import annotations

from datetime import date

from cineprompt_mcp.providers.base import ProviderNotFoundError
from cineprompt_mcp.schemas.common import MediaType, ProviderAttribution
from cineprompt_mcp.schemas.person import PersonSearchResult
from cineprompt_mcp.schemas.title import TitleDetail, TitleSearchResult


def _attribution(provider_id: str, kind: str = "title") -> ProviderAttribution:
    return ProviderAttribution(
        provider="mock",
        provider_id=provider_id,
        source_url=f"mock://{kind}/{provider_id}",
        license_note="Synthetic fixture data for tests and demos.",
    )


MOCK_TITLE_DETAIL = TitleDetail(
    provider="mock",
    provider_id="mock-title-1",
    media_type="movie",
    title="Glass City",
    original_title="Glass City",
    year=2024,
    release_date=date(2024, 3, 14),
    runtime_minutes=104,
    genres=["social thriller", "drama"],
    overview_summary=(
        "A junior architect enters a sealed corporate redevelopment project and discovers "
        "that every promotion depends on quietly displacing someone else."
    ),
    directors=["Mira Han"],
    creators=[],
    cast=["Jin Park", "Sora Lee"],
    keywords=["class pressure", "sealed institution", "vertical city", "moral compromise"],
    production_countries=["KR"],
    attribution=_attribution("mock-title-1"),
)

MOCK_TV_DETAIL = TitleDetail(
    provider="mock",
    provider_id="mock-title-2",
    media_type="tv",
    title="Signal Room",
    original_title="Signal Room",
    year=2023,
    release_date=date(2023, 9, 8),
    runtime_minutes=48,
    genres=["mystery", "workplace drama"],
    overview_summary=(
        "A night-shift team in an emergency operations center tracks conflicting reports "
        "while their own ranking system turns cooperation into suspicion."
    ),
    directors=[],
    creators=["Noah Vale"],
    cast=["Iris Moon", "Tae Kim"],
    keywords=["procedural tension", "communications failure", "institutional pressure"],
    production_countries=["US"],
    attribution=_attribution("mock-title-2"),
)

MOCK_TITLES: dict[str, TitleDetail] = {
    MOCK_TITLE_DETAIL.provider_id: MOCK_TITLE_DETAIL,
    MOCK_TV_DETAIL.provider_id: MOCK_TV_DETAIL,
}

MOCK_PEOPLE: dict[str, PersonSearchResult] = {
    "mock-person-1": PersonSearchResult(
        provider="mock",
        provider_id="mock-person-1",
        name="Mira Han",
        known_for_department="Directing",
        known_for_titles=["Glass City"],
        attribution=_attribution("mock-person-1", "person"),
    ),
    "mock-person-2": PersonSearchResult(
        provider="mock",
        provider_id="mock-person-2",
        name="Noah Vale",
        known_for_department="Writing",
        known_for_titles=["Signal Room"],
        attribution=_attribution("mock-person-2", "person"),
    ),
}

MOCK_FILMOGRAPHY: dict[str, list[str]] = {
    "mock-person-1": ["mock-title-1"],
    "mock-person-2": ["mock-title-2"],
}


class MockProvider:
    """Deterministic provider with normalized synthetic data."""

    name = "mock"

    async def search_titles(
        self,
        query: str,
        media_type: MediaType | None = None,
        year: int | None = None,
        limit: int = 5,
    ) -> list[TitleSearchResult]:
        query_lower = query.lower()
        results: list[TitleSearchResult] = []
        for detail in MOCK_TITLES.values():
            searchable = " ".join(
                [detail.title, detail.original_title or "", *detail.genres, *detail.keywords]
            )
            if query_lower not in searchable.lower():
                continue
            if media_type is not None and detail.media_type != media_type:
                continue
            if year is not None and detail.year != year:
                continue
            results.append(_detail_to_search_result(detail))
        return results[:limit]

    async def search_people(self, query: str, limit: int = 5) -> list[PersonSearchResult]:
        query_lower = query.lower()
        return [
            person
            for person in MOCK_PEOPLE.values()
            if query_lower in person.name.lower()
            or query_lower in " ".join(person.known_for_titles).lower()
        ][:limit]

    async def get_title_detail(
        self,
        provider_id: str,
        media_type: MediaType | None = None,
    ) -> TitleDetail:
        detail = MOCK_TITLES.get(provider_id)
        if detail is None or (media_type is not None and detail.media_type != media_type):
            raise ProviderNotFoundError(f"Mock title not found: {provider_id}")
        return detail

    async def get_person_filmography(
        self,
        provider_id: str,
        limit: int = 10,
    ) -> list[TitleSearchResult]:
        title_ids = MOCK_FILMOGRAPHY.get(provider_id)
        if title_ids is None:
            raise ProviderNotFoundError(f"Mock person not found: {provider_id}")
        return [_detail_to_search_result(MOCK_TITLES[title_id]) for title_id in title_ids[:limit]]


def _detail_to_search_result(detail: TitleDetail) -> TitleSearchResult:
    return TitleSearchResult(
        provider=detail.provider,
        provider_id=detail.provider_id,
        media_type=detail.media_type,
        title=detail.title,
        original_title=detail.original_title,
        year=detail.year,
        release_date=detail.release_date,
        overview_hint=detail.overview_summary,
        genres=detail.genres,
        attribution=detail.attribution,
    )
