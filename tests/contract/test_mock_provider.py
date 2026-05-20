from __future__ import annotations

import pytest

from cineprompt_mcp.providers.base import ProviderNotFoundError
from cineprompt_mcp.providers.mock import MockProvider


@pytest.mark.asyncio
async def test_mock_provider_search_titles() -> None:
    provider = MockProvider()

    results = await provider.search_titles("Glass", media_type="movie")

    assert len(results) == 1
    assert results[0].provider == "mock"
    assert results[0].provider_id == "mock-title-1"


@pytest.mark.asyncio
async def test_mock_provider_search_people() -> None:
    provider = MockProvider()

    results = await provider.search_people("Mira")

    assert results[0].name == "Mira Han"


@pytest.mark.asyncio
async def test_mock_provider_get_person_filmography() -> None:
    provider = MockProvider()

    results = await provider.get_person_filmography("mock-person-1")

    assert results[0].title == "Glass City"


@pytest.mark.asyncio
async def test_mock_provider_missing_title_raises() -> None:
    provider = MockProvider()

    with pytest.raises(ProviderNotFoundError):
        await provider.get_title_detail("missing")
