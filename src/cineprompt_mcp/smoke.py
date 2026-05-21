"""MCP stdio smoke test entrypoint."""

from __future__ import annotations

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

EXPECTED_TOOLS = {
    "search_titles",
    "search_people",
    "get_title_detail",
    "get_person_filmography",
    "build_reference_pack",
    "check_derivative_risk",
    "generate_video_prompt",
}

EXPECTED_PROMPTS = {
    "cinematic_reference_pack",
    "video_prompt_from_reference",
    "shortform_scene_idea",
    "derivative_risk_check",
}


async def run_smoke() -> None:
    env = dict(os.environ)
    env["CINEPROMPT_PROVIDER"] = "mock"
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "cineprompt_mcp.server"],
        env=env,
    )
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            prompts = await session.list_prompts()
            tool_names = {tool.name for tool in tools.tools}
            prompt_names = {prompt.name for prompt in prompts.prompts}
            missing_tools = EXPECTED_TOOLS - tool_names
            missing_prompts = EXPECTED_PROMPTS - prompt_names
            if missing_tools:
                raise RuntimeError(f"Missing MCP tools: {sorted(missing_tools)}")
            if missing_prompts:
                raise RuntimeError(f"Missing MCP prompts: {sorted(missing_prompts)}")
            search_result = await session.call_tool("search_titles", {"query": "Glass"})
            if search_result.isError:
                raise RuntimeError("search_titles returned an MCP error.")
            video_result = await session.call_tool(
                "generate_video_prompt",
                {"provider": "mock", "provider_id": "mock-title-1", "duration_seconds": 15},
            )
            if video_result.isError:
                raise RuntimeError("generate_video_prompt returned an MCP error.")
            prompt_result = await session.get_prompt(
                "video_prompt_from_reference",
                arguments={"reference_pack_json": "{}", "duration_seconds": "12"},
            )
            if not prompt_result.messages:
                raise RuntimeError("video_prompt_from_reference returned no messages.")


def main() -> None:
    asyncio.run(run_smoke())
    print("MCP smoke test passed.")


if __name__ == "__main__":
    main()
