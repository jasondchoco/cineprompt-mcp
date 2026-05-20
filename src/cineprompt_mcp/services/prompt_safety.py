"""Rule-based derivative-risk checks and prompt sanitization."""

from __future__ import annotations

import re

from cineprompt_mcp.schemas.common import RiskLevel
from cineprompt_mcp.schemas.risk import DerivativeRiskReport

DIRECT_CLONE_PATTERNS = [
    r"\bshot[- ]for[- ]shot\b",
    r"\bexact(?:ly)?\b",
    r"\brecreate\b",
    r"\bcopy\b",
    r"\bclone\b",
    r"\bsame scene\b",
    r"\bfamous scene\b",
]

ACTOR_LIKENESS_PATTERNS = [
    r"\bactor likeness\b",
    r"\blook(?:s)? like\b",
    r"\bplayed by\b",
    r"\bdeepfake\b",
    r"\bimpersonat(?:e|ing|ion)\b",
]

FRANCHISE_PATTERNS = [
    r"\bfranchise\b",
    r"\bsequel\b",
    r"\bprequel\b",
    r"\bspin[- ]off\b",
    r"\bcharacter from\b",
]

QUOTE_PATTERN = r"[\"'“”‘’][^\"'“”‘’]{20,}[\"'“”‘’]"


def check_derivative_risk(
    text: str,
    reference_terms: list[str] | None = None,
) -> DerivativeRiskReport:
    """Return a deterministic derivative-risk report for user text."""

    reference_terms = reference_terms or []
    matched: list[str] = []
    warnings: list[str] = []
    lowered = text.lower()

    direct_matches = _matches(text, DIRECT_CLONE_PATTERNS)
    actor_matches = _matches(text, ACTOR_LIKENESS_PATTERNS)
    franchise_matches = _matches(text, FRANCHISE_PATTERNS)
    quote_matches = _matches(text, [QUOTE_PATTERN])
    reference_matches = [term for term in reference_terms if term and term.lower() in lowered]

    if direct_matches:
        matched.extend(direct_matches)
        warnings.append("Request appears to ask for direct scene, plot, or expression copying.")
    if actor_matches:
        matched.extend(actor_matches)
        warnings.append("Request includes actor likeness or performance imitation risk.")
    if franchise_matches:
        matched.extend(franchise_matches)
        warnings.append("Request may rely on franchise, sequel, or named-character identifiers.")
    if quote_matches:
        matched.extend(["quoted dialogue"])
        warnings.append("Request may include copied dialogue or long quoted expression.")
    if reference_matches:
        matched.extend(reference_matches)
        warnings.append("Reference terms should be translated into neutral cinematic language.")

    if direct_matches and (reference_matches or "scene" in lowered or "shot" in lowered):
        level: RiskLevel = "block"
    elif direct_matches or actor_matches or franchise_matches:
        level = "high"
    elif reference_matches or quote_matches:
        level = "medium"
    else:
        level = "low"

    safer_rewrite = _safer_rewrite(level)
    if not warnings:
        warnings.append(
            "No direct copying pattern detected; keep final prompts original and specific."
        )

    return DerivativeRiskReport(
        level=level,
        matched_terms=_unique(matched),
        warnings=warnings,
        safer_rewrite=safer_rewrite,
    )


def sanitize_prompt_text(text: str, prohibited_terms: list[str]) -> str:
    """Remove title/person/franchise terms from final AI video prompt text."""

    sanitized = text
    for term in prohibited_terms:
        if not term:
            continue
        sanitized = re.sub(
            re.escape(term),
            "a neutral cinematic reference",
            sanitized,
            flags=re.IGNORECASE,
        )
    sanitized = re.sub(
        r"\b(?:played by|looks like|look like)\b",
        "with an original presence",
        sanitized,
        flags=re.IGNORECASE,
    )
    return sanitized


def _matches(text: str, patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            found.append(match.group(0))
    return found


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def _safer_rewrite(level: str) -> str:
    if level == "block":
        return (
            "Convert the request into an original premise using abstract pressure, new rules, "
            "new characters, and a distinct setting."
        )
    if level == "high":
        return (
            "Replace named or likeness-based references with physical, emotional, and cinematic "
            "traits that do not identify a protected character or performer."
        )
    if level == "medium":
        return (
            "Use the reference only as general genre, mood, camera, lighting, and story-mechanic "
            "language."
        )
    return "Proceed with original characters, settings, dialogue, and scene construction."
