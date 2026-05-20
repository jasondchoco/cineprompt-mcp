"""Video prompt generation template."""

from __future__ import annotations


def video_prompt_from_reference(reference_pack_json: str, duration_seconds: int = 20) -> str:
    """Prompt that turns a reference pack into a safe AI video prompt pack."""

    return f"""Create an original AI video prompt pack from this reference pack:

{reference_pack_json}

Target duration: {duration_seconds} seconds.

Output:
1. short creative prompt
2. long creative prompt
3. shot list
4. negative prompt
5. derivative-risk notes

Safety rules:
- Do not include movie/TV titles as style instructions.
- Do not include actor likeness, named characters, franchise terms, exact scenes,
  or copied dialogue.
- Preserve only abstract story mechanics and neutral cinematic language."""
