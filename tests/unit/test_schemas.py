from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from cineprompt_mcp.schemas import (
    DerivativeRiskReport,
    ProviderAttribution,
    ReferencePack,
    TitleDetail,
    TitleSearchResult,
    VideoPromptPack,
    VisualLanguage,
)


def _attribution() -> ProviderAttribution:
    return ProviderAttribution(
        provider="mock",
        provider_id="title-1",
        source_url="mock://title/title-1",
    )


def test_title_search_result_serializes_to_json() -> None:
    result = TitleSearchResult(
        provider="mock",
        provider_id="title-1",
        media_type="movie",
        title="Glass City",
        year=2024,
        release_date="2024-03-14",
        attribution=_attribution(),
    )

    payload = result.to_public_dict()
    assert payload["release_date"] == "2024-03-14"
    assert json.loads(result.model_dump_json())["title"] == "Glass City"


def test_title_search_result_rejects_invalid_media_type() -> None:
    with pytest.raises(ValidationError):
        TitleSearchResult(
            provider="mock",
            provider_id="title-1",
            media_type="game",
            title="Glass City",
            attribution=_attribution(),
        )


def test_title_detail_allows_missing_optional_fields() -> None:
    detail = TitleDetail(
        provider="mock",
        provider_id="title-1",
        media_type="movie",
        title="Glass City",
        attribution=_attribution(),
    )

    assert detail.directors == []
    assert "overview_summary" not in detail.to_public_dict()


def test_reference_pack_requires_story_engine() -> None:
    detail = TitleDetail(
        provider="mock",
        provider_id="title-1",
        media_type="movie",
        title="Glass City",
        attribution=_attribution(),
    )

    with pytest.raises(ValidationError):
        ReferencePack(
            reference=detail,
            summary="summary",
            story_engine="",
            visual_language=VisualLanguage(),
            attribution=[_attribution()],
        )


def test_video_prompt_pack_requires_shot_list() -> None:
    with pytest.raises(ValidationError):
        VideoPromptPack(
            short_prompt="short",
            long_prompt="long",
            shot_list=[],
        )


def test_derivative_risk_report_sets_blocked_from_level() -> None:
    report = DerivativeRiskReport(level="block")
    assert report.blocked is True


def test_derivative_risk_report_rejects_invalid_level() -> None:
    with pytest.raises(ValidationError):
        DerivativeRiskReport(level="critical")
