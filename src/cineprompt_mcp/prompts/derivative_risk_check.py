"""Derivative-risk review prompt template."""

from __future__ import annotations


def derivative_risk_check(text: str) -> str:
    """Prompt that asks a model to review derivative-risk issues."""

    return f"""Review this AI video request for derivative-risk issues:

{text}

Classify the risk as low, medium, high, or block.
Identify any risky use of exact scenes, copied dialogue, actor likeness, named characters,
franchise identifiers, or title-as-style instructions.
Then rewrite the request into safer neutral cinematic language while preserving the broad goal."""
