import type { ReferencePack, VideoPromptPack } from "../schemas";
import { sanitizePromptText } from "./prompt-safety";

export function buildVideoPromptPack(
  pack: ReferencePack,
  durationSeconds = 20,
  aspectRatio = "16:9"
): VideoPromptPack {
  const visual = pack.visual_language;
  const prohibited = [
    pack.reference.title,
    ...(pack.reference.cast ?? []),
    ...(pack.reference.directors ?? []),
    ...(pack.reference.creators ?? []),
  ].filter(Boolean);

  const short = sanitizePromptText(
    `Original ${durationSeconds}-second cinematic scene, ${aspectRatio}, ` +
      `driven by ${pack.story_engine} ` +
      `Camera: ${visual.camera.slice(0, 3).join(", ")}. ` +
      `Lighting: ${visual.lighting.slice(0, 2).join(", ")}. ` +
      `Unnamed characters face institutional pressure through new stakes and setting.`,
    prohibited
  );

  const long = sanitizePromptText(
    `Create an original cinematic video scene lasting about ${durationSeconds} seconds. ` +
      `The dramatic engine is: ${pack.story_engine} ` +
      `Use character dynamics such as ${pack.character_dynamics.slice(0, 2).join(", ")}. ` +
      `Build tension through ${pack.genre_mechanics.slice(0, 3).join(", ")}. ` +
      `Visual language: camera uses ${visual.camera.slice(0, 4).join(", ")}; ` +
      `lighting uses ${visual.lighting.slice(0, 3).join(", ")}; ` +
      `color uses ${visual.color.slice(0, 3).join(", ")}; ` +
      `space uses ${visual.space.slice(0, 4).join(", ")}. ` +
      `Keep all characters, locations, dialogue, costumes, symbols, and plot turns original.`,
    prohibited
  );

  const shotList = [
    `Wide establishing shot of an original pressure-filled space using ${visual.space[0]}.`,
    "Controlled medium shot where a silent choice changes the social balance.",
    `Slow close reaction shot with ${visual.lighting[0]} and restrained movement.`,
    "Final unresolved image showing consequence without copying any known scene.",
  ].map((s) => sanitizePromptText(s, prohibited));

  return {
    short_prompt: short,
    long_prompt: long,
    shot_list: shotList,
    negative_prompt: [
      "no named characters",
      "no actor likeness",
      "no exact scene recreation",
      "no franchise identifiers",
      "no copied dialogue",
      "no title-as-style instruction",
    ],
    derivative_risk_notes: pack.risk_notes,
  };
}
