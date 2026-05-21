import type { ReferencePack, TitleDetail, VisualLanguage } from "../schemas";

export function buildReferencePackFromDetail(
  detail: TitleDetail,
  focus?: string | null
): ReferencePack {
  const genreText = detail.genres.length ? detail.genres.join(", ") : "character-driven drama";
  const keywordText = detail.keywords.length
    ? detail.keywords.slice(0, 5).join(", ")
    : "pressure, choice, consequence";
  const focusNote = focus?.trim() ? ` with emphasis on ${focus.trim()}` : "";

  return {
    reference: detail,
    summary:
      detail.overview_summary ??
      "A normalized title reference with limited public summary metadata.",
    story_engine: `A ${genreText} engine built around escalating pressure, visible choices, and consequences shaped by ${keywordText}${focusNote}.`,
    character_dynamics: buildCharacterDynamics(detail),
    genre_mechanics: buildGenreMechanics(detail.genres),
    visual_language: inferVisualLanguage(detail),
    prompt_hooks: [
      "Use social pressure as the source of tension.",
      "Translate the reference into new locations, new stakes, and unnamed characters.",
      "Keep the camera language specific while avoiding recognizable scenes.",
    ],
    risk_notes: [
      "Do not recreate named characters, exact scenes, dialogue, or franchise identifiers.",
      "Use abstract story mechanics and visual language rather than title-as-style prompts.",
      "Avoid actor likeness requests in final video prompts.",
    ],
    attribution: [detail.attribution],
  };
}

function buildCharacterDynamics(detail: TitleDetail): string[] {
  const genreText = [...detail.genres, ...detail.keywords].join(" ").toLowerCase();
  const castCount = detail.cast.length;
  const dynamics: string[] = [];

  if (castCount >= 2) {
    dynamics.push(
      "A protagonist navigating competing loyalties as someone close reveals a hidden agenda."
    );
    dynamics.push(
      "An outsider figure who exposes the unspoken rules everyone else follows silently."
    );
  } else if (castCount === 1) {
    dynamics.push(
      "A lone actor within a system that rewards compliance and punishes visibility."
    );
  } else {
    dynamics.push("A protagonist wants security but must trade comfort for agency.");
  }

  if (genreText.includes("thriller") || genreText.includes("mystery")) {
    dynamics.push(
      "An information broker whose partial knowledge becomes both survival tool and liability."
    );
  }
  if (genreText.includes("workplace") || genreText.includes("institution")) {
    dynamics.push("A gatekeeper who turns ordinary ambition into a moral test.");
  }
  if (genreText.includes("class") || genreText.includes("social")) {
    dynamics.push(
      "Secondary characters who embody competing survival strategies under the same pressure."
    );
  }
  if (genreText.includes("crime") || genreText.includes("heist")) {
    dynamics.push(
      "A character who built trust under false pretenses now faces the cost of that choice."
    );
  }

  const defaults = [
    "A protagonist wants security but must trade comfort for agency.",
    "A gatekeeping institution turns ordinary ambition into moral pressure.",
    "Secondary characters reveal different survival strategies under the same rules.",
  ];
  for (const fallback of defaults) {
    if (dynamics.length >= 3) break;
    if (!dynamics.includes(fallback)) dynamics.push(fallback);
  }

  return dynamics;
}

function buildGenreMechanics(genres: string[]): string[] {
  const genreText = genres.join(" ").toLowerCase();
  const mechanics = ["rising constraints", "status reversals", "compressed decision windows"];
  if (genreText.includes("thriller") || genreText.includes("mystery"))
    mechanics.push("information asymmetry");
  if (genreText.includes("drama"))
    mechanics.push("private desire colliding with public obligation");
  if (genreText.includes("workplace"))
    mechanics.push("institutional rules that turn colleagues into competitors");
  return mechanics;
}

function inferVisualLanguage(detail: TitleDetail): VisualLanguage {
  const genreText = [...detail.genres, ...detail.keywords].join(" ").toLowerCase();
  const camera = ["measured push-ins", "controlled two-shots", "threshold framing"];
  const lighting = ["motivated practical light", "cool ambient spill"];
  const color = ["muted neutrals", "selective warm accents"];
  const space = ["layered interiors", "visible boundaries", "pressure corridors"];
  const editing = ["patient escalation", "reaction-led cuts"];

  if (genreText.includes("thriller") || genreText.includes("pressure")) {
    camera.push("compressed framing", "slow lateral reveals");
    lighting.push("hard contrast in decision moments");
  }
  if (genreText.includes("city") || genreText.includes("vertical")) {
    space.push("vertical architecture", "glass partitions");
  }
  if (genreText.includes("workplace") || genreText.includes("institution")) {
    space.push("repetitive desks", "surveillance-like sightlines");
    color.push("desaturated office tones");
  }

  return { camera, lighting, color, space, editing };
}
