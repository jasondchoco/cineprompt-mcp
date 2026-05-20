"""Derivative-risk public schema."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from cineprompt_mcp.schemas.common import CinePromptModel, NonEmptyStr, RiskLevel


class DerivativeRiskReport(CinePromptModel):
    """Rule-based report for derivative-risk review."""

    level: RiskLevel
    matched_terms: list[NonEmptyStr] = Field(default_factory=list)
    warnings: list[NonEmptyStr] = Field(default_factory=list)
    safer_rewrite: str | None = None
    blocked: bool = False

    @model_validator(mode="before")
    @classmethod
    def align_blocked_with_level(cls, data: Any) -> Any:
        if isinstance(data, dict):
            next_data = dict(data)
            next_data["blocked"] = next_data.get("level") == "block"
            return next_data
        return data
