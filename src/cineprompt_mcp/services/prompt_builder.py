"""Build final AI video prompt packs."""

from __future__ import annotations

from cineprompt_mcp.schemas.prompt_pack import VideoPromptPack
from cineprompt_mcp.schemas.reference_pack import ReferencePack
from cineprompt_mcp.services.prompt_safety import sanitize_prompt_text


def build_video_prompt_pack(
    reference_pack: ReferencePack,
    duration_seconds: int = 20,
    aspect_ratio: str = "16:9",
) -> VideoPromptPack:
    """Create final prompt text from a reference pack without title-as-style copying."""

    visual = reference_pack.visual_language
    prohibited_terms = [
        reference_pack.reference.title,
        *(reference_pack.reference.cast or []),
        *(reference_pack.reference.directors or []),
        *(reference_pack.reference.creators or []),
    ]
    short_prompt = (
        f"Original {duration_seconds}-second cinematic scene, {aspect_ratio}, "
        f"driven by {reference_pack.story_engine} "
        f"Camera: {', '.join(visual.camera[:3])}. "
        f"Lighting: {', '.join(visual.lighting[:2])}. "
        "Unnamed characters face institutional pressure through new stakes and setting."
    )
    long_prompt = (
        f"Create an original cinematic video scene lasting about {duration_seconds} seconds. "
        f"The dramatic engine is: {reference_pack.story_engine} "
        f"Use character dynamics such as {', '.join(reference_pack.character_dynamics[:2])}. "
        f"Build tension through {', '.join(reference_pack.genre_mechanics[:3])}. "
        f"Visual language: camera uses {', '.join(visual.camera[:4])}; lighting uses "
        f"{', '.join(visual.lighting[:3])}; color uses {', '.join(visual.color[:3])}; "
        f"space uses {', '.join(visual.space[:4])}. "
        "Keep all characters, locations, dialogue, costumes, symbols, and plot turns original."
    )
    shot_list = [
        f"Wide establishing shot of an original pressure-filled space using {visual.space[0]}.",
        "Controlled medium shot where a silent choice changes the social balance.",
        f"Slow close reaction shot with {visual.lighting[0]} and restrained movement.",
        "Final unresolved image showing consequence without copying any known scene.",
    ]
    negative_prompt = [
        "no named characters",
        "no actor likeness",
        "no exact scene recreation",
        "no franchise identifiers",
        "no copied dialogue",
        "no title-as-style instruction",
    ]
    return VideoPromptPack(
        short_prompt=sanitize_prompt_text(short_prompt, prohibited_terms),
        long_prompt=sanitize_prompt_text(long_prompt, prohibited_terms),
        shot_list=[sanitize_prompt_text(shot, prohibited_terms) for shot in shot_list],
        negative_prompt=negative_prompt,
        derivative_risk_notes=reference_pack.risk_notes,
    )
