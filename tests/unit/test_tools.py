from __future__ import annotations

import pytest
from pydantic import ValidationError

from cineprompt_mcp.providers.mock import MockProvider
from cineprompt_mcp.tools import (
    build_reference_pack_tool,
    check_derivative_risk_tool,
    generate_video_prompt_tool,
    get_person_filmography_tool,
    get_title_detail_tool,
    search_people_tool,
    search_titles_tool,
)


@pytest.mark.asyncio
async def test_search_titles_tool_happy_path() -> None:
    results = await search_titles_tool(MockProvider(), "Glass", media_type="movie")

    assert results[0].title == "Glass City"


@pytest.mark.asyncio
async def test_search_titles_tool_rejects_bad_limit() -> None:
    with pytest.raises(ValidationError):
        await search_titles_tool(MockProvider(), "Glass", limit=100)


@pytest.mark.asyncio
async def test_search_people_tool_happy_path() -> None:
    results = await search_people_tool(MockProvider(), "Mira")

    assert results[0].provider_id == "mock-person-1"


@pytest.mark.asyncio
async def test_get_title_detail_tool_happy_path() -> None:
    detail = await get_title_detail_tool(MockProvider(), "mock", "mock-title-1", "movie")

    assert detail.title == "Glass City"


@pytest.mark.asyncio
async def test_get_person_filmography_tool_happy_path() -> None:
    results = await get_person_filmography_tool(MockProvider(), "mock", "mock-person-1")

    assert results[0].title == "Glass City"


@pytest.mark.asyncio
async def test_build_reference_pack_tool_happy_path() -> None:
    reference_pack = await build_reference_pack_tool(
        MockProvider(),
        "mock",
        "mock-title-1",
        "movie",
        "visual pressure",
    )

    assert reference_pack.reference.provider_id == "mock-title-1"
    assert "visual pressure" in reference_pack.story_engine


def test_check_derivative_risk_tool_happy_path() -> None:
    report = check_derivative_risk_tool("A tense workplace thriller.")

    assert report.level == "low"


@pytest.mark.asyncio
async def test_generate_video_prompt_tool_happy_path() -> None:
    prompt_pack = await generate_video_prompt_tool(MockProvider(), "mock", "mock-title-1", "movie")

    assert prompt_pack.short_prompt
    assert prompt_pack.long_prompt
    assert len(prompt_pack.shot_list) >= 1
    assert "no actor likeness" in prompt_pack.negative_prompt


@pytest.mark.asyncio
async def test_generate_video_prompt_tool_omits_reference_names() -> None:
    prompt_pack = await generate_video_prompt_tool(MockProvider(), "mock", "mock-title-1", "movie")

    combined = " ".join([prompt_pack.short_prompt, prompt_pack.long_prompt, *prompt_pack.shot_list])
    assert "Glass City" not in combined
    assert "Mira Han" not in combined
