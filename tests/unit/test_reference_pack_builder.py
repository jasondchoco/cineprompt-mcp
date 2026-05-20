from __future__ import annotations

import pytest

from cineprompt_mcp.providers.mock import MockProvider
from cineprompt_mcp.services.prompt_builder import build_video_prompt_pack
from cineprompt_mcp.services.reference_pack_builder import build_reference_pack_from_detail


@pytest.mark.asyncio
async def test_build_reference_pack_from_mock_detail() -> None:
    provider = MockProvider()
    detail = await provider.get_title_detail("mock-title-1", "movie")

    reference_pack = build_reference_pack_from_detail(detail, focus="class pressure")

    assert reference_pack.reference.title == "Glass City"
    assert "escalating pressure" in reference_pack.story_engine
    assert reference_pack.visual_language.camera
    assert reference_pack.risk_notes


@pytest.mark.asyncio
async def test_build_video_prompt_pack_omits_reference_title_and_names() -> None:
    provider = MockProvider()
    detail = await provider.get_title_detail("mock-title-1", "movie")
    reference_pack = build_reference_pack_from_detail(detail)

    prompt_pack = build_video_prompt_pack(reference_pack)

    combined = " ".join([prompt_pack.short_prompt, prompt_pack.long_prompt, *prompt_pack.shot_list])
    assert "Glass City" not in combined
    assert "Mira Han" not in combined
    assert "no actor likeness" in prompt_pack.negative_prompt
