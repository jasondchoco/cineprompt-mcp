"""CinePrompt MCP server entrypoint."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from cineprompt_mcp.prompts import (
    cinematic_reference_pack as cinematic_reference_pack_template,
)
from cineprompt_mcp.prompts import (
    derivative_risk_check as derivative_risk_check_template,
)
from cineprompt_mcp.prompts import (
    shortform_scene_idea as shortform_scene_idea_template,
)
from cineprompt_mcp.prompts import (
    video_prompt_from_reference as video_prompt_from_reference_template,
)
from cineprompt_mcp.schemas.common import MediaType
from cineprompt_mcp.services.provider_registry import ProviderRegistry
from cineprompt_mcp.tools import (
    build_reference_pack_tool,
    check_derivative_risk_tool,
    generate_video_prompt_tool,
    get_person_filmography_tool,
    get_title_detail_tool,
    search_people_tool,
    search_titles_tool,
)


def create_server(registry: ProviderRegistry | None = None) -> FastMCP:
    """Create the FastMCP server and register public tools/prompts."""

    provider_registry = registry or ProviderRegistry()
    mcp = FastMCP("CinePrompt MCP")

    @mcp.tool()
    async def search_titles(
        query: str,
        media_type: MediaType | None = None,
        year: int | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Search movie/TV titles using the configured default provider."""

        provider = provider_registry.get()
        results = await search_titles_tool(provider, query, media_type, year, limit)
        return [result.to_public_dict() for result in results]

    @mcp.tool()
    async def search_people(query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Search people using the configured default provider."""

        provider = provider_registry.get()
        results = await search_people_tool(provider, query, limit)
        return [result.to_public_dict() for result in results]

    @mcp.tool()
    async def get_title_detail(
        provider: str,
        provider_id: str,
        media_type: MediaType | None = None,
    ) -> dict[str, Any]:
        """Fetch normalized title detail by provider id."""

        selected_provider = provider_registry.get(provider)
        detail = await get_title_detail_tool(selected_provider, provider, provider_id, media_type)
        return detail.to_public_dict()

    @mcp.tool()
    async def get_person_filmography(
        provider: str,
        provider_id: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Fetch normalized filmography for a person."""

        selected_provider = provider_registry.get(provider)
        results = await get_person_filmography_tool(selected_provider, provider, provider_id, limit)
        return [result.to_public_dict() for result in results]

    @mcp.tool()
    async def build_reference_pack(
        provider: str,
        provider_id: str,
        media_type: MediaType | None = None,
        focus: str | None = None,
    ) -> dict[str, Any]:
        """Build an originality-focused cinematic reference pack."""

        selected_provider = provider_registry.get(provider)
        reference_pack = await build_reference_pack_tool(
            selected_provider,
            provider,
            provider_id,
            media_type,
            focus,
        )
        return reference_pack.to_public_dict()

    @mcp.tool()
    def check_derivative_risk(
        text: str,
        reference_terms: list[str] | None = None,
    ) -> dict[str, Any]:
        """Check derivative-risk patterns in a request."""

        report = check_derivative_risk_tool(text, reference_terms)
        return report.to_public_dict()

    @mcp.tool()
    async def generate_video_prompt(
        provider: str,
        provider_id: str,
        media_type: MediaType | None = None,
        focus: str | None = None,
        duration_seconds: int = 20,
        aspect_ratio: str = "16:9",
    ) -> dict[str, Any]:
        """Generate a safe AI video prompt pack from a title reference."""

        selected_provider = provider_registry.get(provider)
        prompt_pack = await generate_video_prompt_tool(
            selected_provider,
            provider,
            provider_id,
            media_type,
            focus,
            duration_seconds,
            aspect_ratio,
        )
        return prompt_pack.to_public_dict()

    @mcp.prompt()
    def cinematic_reference_pack(title_or_query: str, focus: str | None = None) -> str:
        """Generate instructions for building a cinematic reference pack."""

        return cinematic_reference_pack_template(title_or_query, focus)

    @mcp.prompt()
    def video_prompt_from_reference(reference_pack_json: str, duration_seconds: int = 20) -> str:
        """Generate instructions for creating a safe AI video prompt pack."""

        return video_prompt_from_reference_template(reference_pack_json, duration_seconds)

    @mcp.prompt()
    def shortform_scene_idea(
        story_engine: str,
        format_hint: str = "vertical short-form video",
    ) -> str:
        """Generate an original short-form scene idea."""

        return shortform_scene_idea_template(story_engine, format_hint)

    @mcp.prompt()
    def derivative_risk_check(text: str) -> str:
        """Generate instructions for a derivative-risk review."""

        return derivative_risk_check_template(text)

    return mcp


def main() -> None:
    """Run the stdio MCP server."""

    create_server().run(transport="stdio")


if __name__ == "__main__":
    main()
