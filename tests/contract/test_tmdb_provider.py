from __future__ import annotations

import httpx
import pytest

from cineprompt_mcp.providers.base import ProviderAuthError, ProviderNotFoundError
from cineprompt_mcp.providers.tmdb import TMDbProvider


@pytest.mark.asyncio
async def test_tmdb_provider_requires_api_key() -> None:
    provider = TMDbProvider(api_key=None)

    with pytest.raises(ProviderAuthError):
        await provider.search_titles("query")


@pytest.mark.asyncio
async def test_tmdb_provider_search_titles_with_mocked_http() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/3/search/movie"
        return httpx.Response(
            200,
            json={
                "results": [
                    {
                        "id": 101,
                        "title": "Glass City",
                        "release_date": "2024-03-14",
                        "overview": "A compressed summary.",
                    }
                ]
            },
        )

    provider = TMDbProvider(
        api_key="test-key",
        base_url="https://api.themoviedb.org/3",
        transport=httpx.MockTransport(handler),
    )

    results = await provider.search_titles("Glass", media_type="movie")

    assert results[0].provider == "tmdb"
    assert results[0].provider_id == "101"
    assert results[0].attribution.license_note


@pytest.mark.asyncio
async def test_tmdb_provider_get_title_detail_with_mocked_http() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/3/movie/101"
        return httpx.Response(
            200,
            json={
                "id": 101,
                "title": "Glass City",
                "original_title": "Glass City",
                "release_date": "2024-03-14",
                "runtime": 104,
                "genres": [{"name": "Thriller"}],
                "overview": "A compressed summary.",
                "credits": {
                    "crew": [{"job": "Director", "name": "Mira Han"}],
                    "cast": [{"name": "Jin Park"}],
                },
                "keywords": {"keywords": [{"name": "pressure"}]},
                "production_countries": [{"iso_3166_1": "KR"}],
            },
        )

    provider = TMDbProvider(
        api_key="test-key",
        base_url="https://api.themoviedb.org/3",
        transport=httpx.MockTransport(handler),
    )

    detail = await provider.get_title_detail("101", "movie")

    assert detail.title == "Glass City"
    assert detail.directors == ["Mira Han"]
    assert detail.keywords == ["pressure"]


@pytest.mark.asyncio
async def test_tmdb_provider_maps_404_to_not_found() -> None:
    provider = TMDbProvider(
        api_key="test-key",
        transport=httpx.MockTransport(lambda _request: httpx.Response(404, json={})),
    )

    with pytest.raises(ProviderNotFoundError):
        await provider.get_title_detail("missing", "movie")
