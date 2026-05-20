from __future__ import annotations

import os

import pytest

from cineprompt_mcp.providers.tmdb import TMDbProvider

pytestmark = pytest.mark.live


@pytest.mark.skipif(
    os.getenv("RUN_LIVE_PROVIDER_TESTS") != "1" or not os.getenv("TMDB_API_KEY"),
    reason="Live provider tests require RUN_LIVE_PROVIDER_TESTS=1 and TMDB_API_KEY.",
)
@pytest.mark.asyncio
async def test_tmdb_live_search_titles() -> None:
    provider = TMDbProvider(api_key=os.getenv("TMDB_API_KEY"))

    results = await provider.search_titles("Heat", media_type="movie", limit=1)

    assert results
    assert results[0].provider == "tmdb"
