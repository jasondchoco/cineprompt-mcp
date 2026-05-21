from __future__ import annotations

import httpx
import pytest

from cineprompt_mcp.providers.base import ProviderAuthError, ProviderNotFoundError
from cineprompt_mcp.providers.omdb import OMDbProvider


def _search_handler(request: httpx.Request) -> httpx.Response:
    assert request.url.params["s"] == "Guardians"
    return httpx.Response(
        200,
        json={
            "Search": [
                {
                    "Title": "Guardians of the Galaxy Vol. 2",
                    "Year": "2017",
                    "imdbID": "tt3896198",
                    "Type": "movie",
                }
            ],
            "totalResults": "1",
            "Response": "True",
        },
    )


def _detail_handler(request: httpx.Request) -> httpx.Response:
    assert request.url.params["i"] == "tt3896198"
    return httpx.Response(
        200,
        json={
            "Title": "Guardians of the Galaxy Vol. 2",
            "Year": "2017",
            "Released": "05 May 2017",
            "Runtime": "136 min",
            "Genre": "Action, Adventure, Comedy",
            "Director": "James Gunn",
            "Writer": "James Gunn, Dan Abnett",
            "Actors": "Chris Pratt, Zoe Saldana, Dave Bautista",
            "Plot": "The Guardians struggle to keep together as a team.",
            "Country": "United States",
            "imdbID": "tt3896198",
            "Type": "movie",
            "Response": "True",
        },
    )


@pytest.mark.asyncio
async def test_omdb_provider_requires_api_key() -> None:
    provider = OMDbProvider(api_key=None)

    with pytest.raises(ProviderAuthError):
        await provider.search_titles("query")


@pytest.mark.asyncio
async def test_omdb_provider_search_titles_with_mocked_http() -> None:
    provider = OMDbProvider(
        api_key="test-key",
        transport=httpx.MockTransport(_search_handler),
    )

    results = await provider.search_titles("Guardians", media_type="movie")

    assert len(results) == 1
    assert results[0].provider == "omdb"
    assert results[0].provider_id == "tt3896198"
    assert results[0].title == "Guardians of the Galaxy Vol. 2"
    assert results[0].year == 2017
    assert results[0].media_type == "movie"
    assert results[0].attribution.license_note


@pytest.mark.asyncio
async def test_omdb_provider_search_titles_returns_empty_on_no_results() -> None:
    provider = OMDbProvider(
        api_key="test-key",
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json={"Response": "False", "Error": "Movie not found!"})
        ),
    )

    results = await provider.search_titles("xyznotafilm")

    assert results == []


@pytest.mark.asyncio
async def test_omdb_provider_get_title_detail_with_mocked_http() -> None:
    provider = OMDbProvider(
        api_key="test-key",
        transport=httpx.MockTransport(_detail_handler),
    )

    detail = await provider.get_title_detail("tt3896198", "movie")

    assert detail.provider == "omdb"
    assert detail.provider_id == "tt3896198"
    assert detail.title == "Guardians of the Galaxy Vol. 2"
    assert detail.year == 2017
    assert detail.runtime_minutes == 136
    assert "Action" in detail.genres
    assert detail.directors == ["James Gunn"]
    assert "Chris Pratt" in detail.cast
    assert detail.attribution.source_url == "https://www.imdb.com/title/tt3896198/"


@pytest.mark.asyncio
async def test_omdb_provider_get_title_detail_raises_not_found() -> None:
    provider = OMDbProvider(
        api_key="test-key",
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json={"Response": "False", "Error": "Incorrect IMDb ID."})
        ),
    )

    with pytest.raises(ProviderNotFoundError):
        await provider.get_title_detail("tt0000000")


@pytest.mark.asyncio
async def test_omdb_provider_search_people_returns_empty() -> None:
    provider = OMDbProvider(api_key="test-key")

    results = await provider.search_people("James Gunn")

    assert results == []


@pytest.mark.asyncio
async def test_omdb_provider_get_person_filmography_returns_empty() -> None:
    provider = OMDbProvider(api_key="test-key")

    results = await provider.get_person_filmography("nm0348231")

    assert results == []
