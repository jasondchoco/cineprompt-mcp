from __future__ import annotations

from cineprompt_mcp.prompts import (
    cinematic_reference_pack,
    derivative_risk_check,
    shortform_scene_idea,
    video_prompt_from_reference,
)


def test_cinematic_reference_pack_prompt_has_required_sections() -> None:
    prompt = cinematic_reference_pack("Glass City", focus="social pressure")

    assert "story engine" in prompt
    assert "derivative-risk notes" in prompt
    assert "actor likeness" in prompt


def test_video_prompt_from_reference_prompt_has_safety_rules() -> None:
    prompt = video_prompt_from_reference("{}", duration_seconds=12)

    assert "short creative prompt" in prompt
    assert "negative prompt" in prompt
    assert "Do not include actor likeness" in prompt


def test_shortform_scene_idea_prompt_avoids_recognizable_references() -> None:
    prompt = shortform_scene_idea("closed-rule institutional pressure")

    assert "4-shot structure" in prompt
    assert "no recognizable scene" in prompt


def test_derivative_risk_check_prompt_requests_classification() -> None:
    prompt = derivative_risk_check("Make a tense office scene.")

    assert "Classify the risk" in prompt
    assert "safer neutral cinematic language" in prompt
