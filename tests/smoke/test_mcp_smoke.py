from __future__ import annotations

import pytest

from cineprompt_mcp.smoke import run_smoke


@pytest.mark.asyncio
async def test_mcp_stdio_smoke() -> None:
    await run_smoke()
