"""Short-form scene idea prompt template."""

from __future__ import annotations


def shortform_scene_idea(story_engine: str, format_hint: str = "vertical short-form video") -> str:
    """Prompt that creates an original short-form scene idea."""

    return f"""Create one original {format_hint} scene idea using this story engine:

{story_engine}

Return:
- logline
- central pressure
- visual hook
- 4-shot structure
- negative prompt

Use original characters, original setting, and no recognizable scene, character, actor,
or franchise references."""
