"""Runtime configuration for CinePrompt MCP."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    default_provider: str = "mock"
    tmdb_api_key: str | None = None
    tmdb_base_url: str = "https://api.themoviedb.org/3"


def load_settings() -> Settings:
    """Load settings from environment variables."""

    return Settings(
        default_provider=os.getenv("CINEPROMPT_PROVIDER", "mock").strip() or "mock",
        tmdb_api_key=os.getenv("TMDB_API_KEY") or None,
        tmdb_base_url=os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3").rstrip("/"),
    )
