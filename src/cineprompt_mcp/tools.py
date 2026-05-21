"""Tool handlers shared by MCP server and tests."""

from __future__ import annotations

from cineprompt_mcp.providers.base import MetadataProvider
from cineprompt_mcp.schemas.common import MediaType
from cineprompt_mcp.schemas.person import PersonSearchResult
from cineprompt_mcp.schemas.prompt_pack import VideoPromptPack
from cineprompt_mcp.schemas.reference_pack import ReferencePack
from cineprompt_mcp.schemas.risk import DerivativeRiskReport
from cineprompt_mcp.schemas.title import TitleDetail, TitleSearchResult
from cineprompt_mcp.schemas.tools import (
    BuildReferencePackInput,
    CheckDerivativeRiskInput,
    GenerateVideoPromptInput,
    PersonFilmographyInput,
    ProviderTitleInput,
    SearchPeopleInput,
    SearchTitlesInput,
)
from cineprompt_mcp.services.prompt_builder import build_video_prompt_pack
from cineprompt_mcp.services.prompt_safety import check_derivative_risk
from cineprompt_mcp.services.reference_pack_builder import build_reference_pack_from_detail


async def search_titles_tool(
    provider: MetadataProvider,
    query: str,
    media_type: MediaType | None = None,
    year: int | None = None,
    limit: int = 5,
) -> list[TitleSearchResult]:
    params = SearchTitlesInput(query=query, media_type=media_type, year=year, limit=limit)
    return await provider.search_titles(
        query=params.query,
        media_type=params.media_type,
        year=params.year,
        limit=params.limit,
    )


async def search_people_tool(
    provider: MetadataProvider,
    query: str,
    limit: int = 5,
) -> list[PersonSearchResult]:
    params = SearchPeopleInput(query=query, limit=limit)
    return await provider.search_people(query=params.query, limit=params.limit)


async def get_title_detail_tool(
    provider: MetadataProvider,
    provider_name: str,
    provider_id: str,
    media_type: MediaType | None = None,
) -> TitleDetail:
    params = ProviderTitleInput(
        provider=provider_name,
        provider_id=provider_id,
        media_type=media_type,
    )
    return await provider.get_title_detail(
        provider_id=params.provider_id,
        media_type=params.media_type,
    )


async def get_person_filmography_tool(
    provider: MetadataProvider,
    provider_name: str,
    provider_id: str,
    limit: int = 10,
) -> list[TitleSearchResult]:
    params = PersonFilmographyInput(provider=provider_name, provider_id=provider_id, limit=limit)
    return await provider.get_person_filmography(provider_id=params.provider_id, limit=params.limit)


async def build_reference_pack_tool(
    provider: MetadataProvider,
    provider_name: str,
    provider_id: str,
    media_type: MediaType | None = None,
    focus: str | None = None,
) -> ReferencePack:
    params = BuildReferencePackInput(
        provider=provider_name,
        provider_id=provider_id,
        media_type=media_type,
        focus=focus,
    )
    detail = await provider.get_title_detail(
        provider_id=params.provider_id,
        media_type=params.media_type,
    )
    return build_reference_pack_from_detail(detail, focus=params.focus)


def check_derivative_risk_tool(
    text: str,
    reference_terms: list[str] | None = None,
) -> DerivativeRiskReport:
    params = CheckDerivativeRiskInput(text=text, reference_terms=reference_terms or [])
    return check_derivative_risk(text=params.text, reference_terms=params.reference_terms)


async def generate_video_prompt_tool(
    provider: MetadataProvider,
    provider_name: str,
    provider_id: str,
    media_type: MediaType | None = None,
    focus: str | None = None,
    duration_seconds: int = 20,
    aspect_ratio: str = "16:9",
) -> VideoPromptPack:
    params = GenerateVideoPromptInput(
        provider=provider_name,
        provider_id=provider_id,
        media_type=media_type,
        focus=focus,
        duration_seconds=duration_seconds,
        aspect_ratio=aspect_ratio,
    )
    detail = await provider.get_title_detail(
        provider_id=params.provider_id,
        media_type=params.media_type,
    )
    reference_pack = build_reference_pack_from_detail(detail, focus=params.focus)
    return build_video_prompt_pack(
        reference_pack,
        duration_seconds=params.duration_seconds,
        aspect_ratio=params.aspect_ratio,
    )
