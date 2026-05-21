from __future__ import annotations

import os

import pytest

from cineprompt_mcp.providers.omdb import OMDbProvider

pytestmark = pytest.mark.live

OMDB_API_KEY = os.getenv("OMDB_API_KEY")


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_PROVIDER_TESTS") != "1" or not OMDB_API_KEY,
    reason="Live provider tests require RUN_LIVE_PROVIDER_TESTS=1 and OMDB_API_KEY.",
)
@pytest.mark.asyncio
async def test_omdb_live_search_titles() -> None:
    provider = OMDbProvider(api_key=OMDB_API_KEY)

    results = await provider.search_titles("Heat", media_type="movie", limit=1)

    assert results
    assert results[0].provider == "omdb"
    assert results[0].provider_id.startswith("tt")


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_PROVIDER_TESTS") != "1" or not OMDB_API_KEY,
    reason="Live provider tests require RUN_LIVE_PROVIDER_TESTS=1 and OMDB_API_KEY.",
)
@pytest.mark.asyncio
async def test_omdb_live_get_title_detail() -> None:
    provider = OMDbProvider(api_key=OMDB_API_KEY)

    # Guardians of the Galaxy Vol. 2
    detail = await provider.get_title_detail("tt3896198")

    assert detail.provider == "omdb"
    assert detail.provider_id == "tt3896198"
    assert "Guardians" in detail.title
    assert detail.year == 2017
    assert detail.runtime_minutes is not None
    assert detail.genres
    assert detail.directors
