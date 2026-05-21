import type { DerivativeRiskReport, RiskLevel } from "../schemas";

const DIRECT_CLONE_PATTERNS = [
  /\bshot[- ]for[- ]shot\b/gi,
  /\bexact(?:ly)?\b/gi,
  /\brecreate\b/gi,
  /\bcopy\b/gi,
  /\bclone\b/gi,
  /\bsame scene\b/gi,
  /\bfamous scene\b/gi,
];

const ACTOR_LIKENESS_PATTERNS = [
  /\bactor likeness\b/gi,
  /\blook(?:s)? like\b/gi,
  /\bplayed by\b/gi,
  /\bdeepfake\b/gi,
  /\bimpersonat(?:e|ing|ion)\b/gi,
];

const FRANCHISE_PATTERNS = [
  /\bfranchise\b/gi,
  /\bsequel\b/gi,
  /\bprequel\b/gi,
  /\bspin[- ]off\b/gi,
  /\bcharacter from\b/gi,
];

const QUOTE_PATTERN = /["""''''][^"""'''']{20,}["""'''']/gi;

function findMatches(text: string, patterns: RegExp[]): string[] {
  const found: string[] = [];
  for (const pattern of patterns) {
    pattern.lastIndex = 0;
    let match: RegExpExecArray | null;
    while ((match = pattern.exec(text)) !== null) {
      found.push(match[0]);
    }
  }
  return found;
}

function unique(values: string[]): string[] {
  const seen = new Set<string>();
  return values.filter((v) => {
    const key = v.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function saferRewrite(level: RiskLevel): string {
  if (level === "block")
    return "Convert the request into an original premise using abstract pressure, new rules, new characters, and a distinct setting.";
  if (level === "high")
    return "Replace named or likeness-based references with physical, emotional, and cinematic traits that do not identify a protected character or performer.";
  if (level === "medium")
    return "Use the reference only as general genre, mood, camera, lighting, and story-mechanic language.";
  return "Proceed with original characters, settings, dialogue, and scene construction.";
}

export function checkDerivativeRisk(
  text: string,
  referenceTerms: string[] = []
): DerivativeRiskReport {
  const lowered = text.toLowerCase();
  const matched: string[] = [];
  const warnings: string[] = [];

  const directMatches = findMatches(text, DIRECT_CLONE_PATTERNS);
  const actorMatches = findMatches(text, ACTOR_LIKENESS_PATTERNS);
  const franchiseMatches = findMatches(text, FRANCHISE_PATTERNS);
  const quoteMatches = findMatches(text, [QUOTE_PATTERN]);
  const referenceMatches = referenceTerms.filter(
    (t) => t && lowered.includes(t.toLowerCase())
  );

  if (directMatches.length) {
    matched.push(...directMatches);
    warnings.push("Request appears to ask for direct scene, plot, or expression copying.");
  }
  if (actorMatches.length) {
    matched.push(...actorMatches);
    warnings.push("Request includes actor likeness or performance imitation risk.");
  }
  if (franchiseMatches.length) {
    matched.push(...franchiseMatches);
    warnings.push("Request may rely on franchise, sequel, or named-character identifiers.");
  }
  if (quoteMatches.length) {
    matched.push("quoted dialogue");
    warnings.push("Request may include copied dialogue or long quoted expression.");
  }
  if (referenceMatches.length) {
    matched.push(...referenceMatches);
    warnings.push("Reference terms should be translated into neutral cinematic language.");
  }

  let level: RiskLevel;
  if (
    directMatches.length &&
    (referenceMatches.length || lowered.includes("scene") || lowered.includes("shot"))
  ) {
    level = "block";
  } else if (directMatches.length || actorMatches.length || franchiseMatches.length) {
    level = "high";
  } else if (referenceMatches.length || quoteMatches.length) {
    level = "medium";
  } else {
    level = "low";
  }

  if (!warnings.length) {
    warnings.push("No direct copying pattern detected; keep final prompts original and specific.");
  }

  return {
    level,
    matched_terms: unique(matched),
    warnings,
    safer_rewrite: saferRewrite(level),
    blocked: level === "block",
  };
}

export function sanitizePromptText(text: string, prohibitedTerms: string[]): string {
  let sanitized = text;
  for (const term of prohibitedTerms) {
    if (!term) continue;
    sanitized = sanitized.replace(
      new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi"),
      "a neutral cinematic reference"
    );
  }
  sanitized = sanitized.replace(
    /\b(?:played by|looks like|look like)\b/gi,
    "with an original presence"
  );
  return sanitized;
}
