from __future__ import annotations

from cineprompt_mcp.services.prompt_safety import check_derivative_risk, sanitize_prompt_text


def test_check_derivative_risk_blocks_exact_scene_with_reference_term() -> None:
    report = check_derivative_risk(
        "Recreate the exact red-light scene with the same shots.",
        reference_terms=["red-light scene"],
    )

    assert report.level == "block"
    assert report.blocked is True
    assert report.safer_rewrite is not None


def test_check_derivative_risk_flags_actor_likeness() -> None:
    report = check_derivative_risk("Make the lead look like a famous actor.")

    assert report.level == "high"
    assert any("actor likeness" in warning.lower() for warning in report.warnings)


def test_check_derivative_risk_allows_general_cinematic_language() -> None:
    report = check_derivative_risk("A tense institutional satire with cold lighting.")

    assert report.level == "low"
    assert report.blocked is False


def test_sanitize_prompt_text_removes_prohibited_terms() -> None:
    sanitized = sanitize_prompt_text(
        "Make this like Glass City and played by Mira Han.",
        ["Glass City", "Mira Han"],
    )

    assert "Glass City" not in sanitized
    assert "Mira Han" not in sanitized
    assert "played by" not in sanitized
