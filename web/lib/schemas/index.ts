import { z } from "zod";

export const MediaType = z.enum(["movie", "tv"]);
export type MediaType = z.infer<typeof MediaType>;

export const RiskLevel = z.enum(["low", "medium", "high", "block"]);
export type RiskLevel = z.infer<typeof RiskLevel>;

export const ProviderAttribution = z.object({
  provider: z.string(),
  provider_id: z.string(),
  source_url: z.string().nullable(),
  license_note: z.string().nullable(),
});
export type ProviderAttribution = z.infer<typeof ProviderAttribution>;

export const TitleSearchResult = z.object({
  provider: z.string(),
  provider_id: z.string(),
  media_type: MediaType,
  title: z.string(),
  original_title: z.string().nullable(),
  year: z.number().nullable(),
  release_date: z.string().nullable(),
  overview_hint: z.string().nullable(),
  genres: z.array(z.string()),
  attribution: ProviderAttribution,
});
export type TitleSearchResult = z.infer<typeof TitleSearchResult>;

export const TitleDetail = z.object({
  provider: z.string(),
  provider_id: z.string(),
  media_type: MediaType,
  title: z.string(),
  original_title: z.string().nullable(),
  year: z.number().nullable(),
  release_date: z.string().nullable(),
  runtime_minutes: z.number().nullable(),
  genres: z.array(z.string()),
  overview_summary: z.string().nullable(),
  directors: z.array(z.string()),
  creators: z.array(z.string()),
  cast: z.array(z.string()),
  keywords: z.array(z.string()),
  production_countries: z.array(z.string()),
  attribution: ProviderAttribution,
});
export type TitleDetail = z.infer<typeof TitleDetail>;

export const PersonSearchResult = z.object({
  provider: z.string(),
  provider_id: z.string(),
  name: z.string(),
  known_for_department: z.string().nullable(),
  known_for_titles: z.array(z.string()),
  attribution: ProviderAttribution,
});
export type PersonSearchResult = z.infer<typeof PersonSearchResult>;

export const VisualLanguage = z.object({
  camera: z.array(z.string()),
  lighting: z.array(z.string()),
  color: z.array(z.string()),
  space: z.array(z.string()),
  editing: z.array(z.string()),
});
export type VisualLanguage = z.infer<typeof VisualLanguage>;

export const ReferencePack = z.object({
  reference: TitleDetail,
  summary: z.string(),
  story_engine: z.string(),
  character_dynamics: z.array(z.string()),
  genre_mechanics: z.array(z.string()),
  visual_language: VisualLanguage,
  prompt_hooks: z.array(z.string()),
  risk_notes: z.array(z.string()),
  attribution: z.array(ProviderAttribution),
});
export type ReferencePack = z.infer<typeof ReferencePack>;

export const VideoPromptPack = z.object({
  short_prompt: z.string(),
  long_prompt: z.string(),
  shot_list: z.array(z.string()),
  negative_prompt: z.array(z.string()),
  derivative_risk_notes: z.array(z.string()),
});
export type VideoPromptPack = z.infer<typeof VideoPromptPack>;

export const DerivativeRiskReport = z.object({
  level: RiskLevel,
  matched_terms: z.array(z.string()),
  warnings: z.array(z.string()),
  safer_rewrite: z.string(),
  blocked: z.boolean(),
});
export type DerivativeRiskReport = z.infer<typeof DerivativeRiskReport>;
