"""Reference pack builder."""

from __future__ import annotations

from cineprompt_mcp.schemas.common import VisualLanguage
from cineprompt_mcp.schemas.reference_pack import ReferencePack
from cineprompt_mcp.schemas.title import TitleDetail


def build_reference_pack_from_detail(
    detail: TitleDetail,
    focus: str | None = None,
) -> ReferencePack:
    """Build an originality-focused reference pack from normalized title detail."""

    genre_text = ", ".join(detail.genres) if detail.genres else "character-driven drama"
    keyword_text = (
        ", ".join(detail.keywords[:5]) if detail.keywords else "pressure, choice, consequence"
    )
    focus_note = f" with emphasis on {focus.strip()}" if focus and focus.strip() else ""
    visual_language = _infer_visual_language(detail)
    return ReferencePack(
        reference=detail,
        summary=detail.overview_summary
        or "A normalized title reference with limited public summary metadata.",
        story_engine=(
            f"A {genre_text} engine built around escalating pressure, visible choices, "
            f"and consequences shaped by {keyword_text}{focus_note}."
        ),
        character_dynamics=[
            "A protagonist wants security but must trade comfort for agency.",
            "A gatekeeping institution turns ordinary ambition into moral pressure.",
            "Secondary characters reveal different survival strategies under the same rules.",
        ],
        genre_mechanics=_genre_mechanics(detail.genres),
        visual_language=visual_language,
        prompt_hooks=[
            "Use social pressure as the source of tension.",
            "Translate the reference into new locations, new stakes, and unnamed characters.",
            "Keep the camera language specific while avoiding recognizable scenes.",
        ],
        risk_notes=[
            "Do not recreate named characters, exact scenes, dialogue, or franchise identifiers.",
            "Use abstract story mechanics and visual language rather than title-as-style prompts.",
            "Avoid actor likeness requests in final video prompts.",
        ],
        attribution=[detail.attribution],
    )


def _genre_mechanics(genres: list[str]) -> list[str]:
    genre_text = " ".join(genres).lower()
    mechanics = ["rising constraints", "status reversals", "compressed decision windows"]
    if "thriller" in genre_text or "mystery" in genre_text:
        mechanics.append("information asymmetry")
    if "drama" in genre_text:
        mechanics.append("private desire colliding with public obligation")
    if "workplace" in genre_text:
        mechanics.append("institutional rules that turn colleagues into competitors")
    return mechanics


def _infer_visual_language(detail: TitleDetail) -> VisualLanguage:
    genre_text = " ".join(detail.genres + detail.keywords).lower()
    camera = ["measured push-ins", "controlled two-shots", "threshold framing"]
    lighting = ["motivated practical light", "cool ambient spill"]
    color = ["muted neutrals", "selective warm accents"]
    space = ["layered interiors", "visible boundaries", "pressure corridors"]
    editing = ["patient escalation", "reaction-led cuts"]
    if "thriller" in genre_text or "pressure" in genre_text:
        camera.extend(["compressed framing", "slow lateral reveals"])
        lighting.append("hard contrast in decision moments")
    if "city" in genre_text or "vertical" in genre_text:
        space.extend(["vertical architecture", "glass partitions"])
    if "workplace" in genre_text or "institution" in genre_text:
        space.extend(["repetitive desks", "surveillance-like sightlines"])
        color.append("desaturated office tones")
    return VisualLanguage(
        camera=camera,
        lighting=lighting,
        color=color,
        space=space,
        editing=editing,
    )
