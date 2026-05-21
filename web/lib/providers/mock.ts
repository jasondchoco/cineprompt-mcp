import type {
  PersonSearchResult,
  TitleDetail,
  TitleSearchResult,
} from "../schemas";

export const MOCK_TITLES: TitleDetail[] = [
  {
    provider: "mock",
    provider_id: "mock-title-1",
    media_type: "movie",
    title: "Glass City",
    original_title: "Glass City",
    year: 2024,
    release_date: "2024-03-14",
    runtime_minutes: 104,
    genres: ["social thriller", "drama"],
    overview_summary:
      "A junior architect enters a sealed corporate redevelopment project and discovers that every promotion depends on quietly displacing someone else.",
    directors: ["Mira Han"],
    creators: [],
    cast: ["Jin Park", "Sora Lee"],
    keywords: ["class pressure", "sealed institution", "vertical city", "moral compromise"],
    production_countries: ["KR"],
    attribution: {
      provider: "mock",
      provider_id: "mock-title-1",
      source_url: "mock://title/mock-title-1",
      license_note: "Synthetic fixture data for tests and demos.",
    },
  },
  {
    provider: "mock",
    provider_id: "mock-title-2",
    media_type: "tv",
    title: "Signal Room",
    original_title: "Signal Room",
    year: 2023,
    release_date: "2023-09-01",
    runtime_minutes: null,
    genres: ["mystery", "workplace drama"],
    overview_summary:
      "A communications analyst at a government relay station begins receiving transmissions that predict workplace accidents before they happen.",
    directors: [],
    creators: ["Jin Park"],
    cast: ["Sora Lee", "Do Yun Kim"],
    keywords: ["surveillance", "institutional paranoia", "closed loop", "whistleblower"],
    production_countries: ["KR"],
    attribution: {
      provider: "mock",
      provider_id: "mock-title-2",
      source_url: "mock://title/mock-title-2",
      license_note: "Synthetic fixture data for tests and demos.",
    },
  },
];

export const MOCK_PEOPLE: PersonSearchResult[] = [
  {
    provider: "mock",
    provider_id: "mock-person-1",
    name: "Mira Han",
    known_for_department: "Directing",
    known_for_titles: ["Glass City"],
    attribution: {
      provider: "mock",
      provider_id: "mock-person-1",
      source_url: "mock://person/mock-person-1",
      license_note: "Synthetic fixture data for tests and demos.",
    },
  },
];

export function mockSearchTitles(
  query: string,
  limit = 5
): TitleSearchResult[] {
  const q = query.toLowerCase();
  return MOCK_TITLES.filter(
    (t) =>
      t.title.toLowerCase().includes(q) ||
      t.genres.some((g) => g.toLowerCase().includes(q)) ||
      t.keywords.some((k) => k.toLowerCase().includes(q))
  )
    .slice(0, limit)
    .map(detailToSearchResult);
}

export function mockGetTitleDetail(id: string): TitleDetail {
  const found = MOCK_TITLES.find((t) => t.provider_id === id);
  if (!found) throw new Error(`MOCK_NOT_FOUND: ${id}`);
  return found;
}

export function mockSearchPeople(query: string, limit = 5): PersonSearchResult[] {
  const q = query.toLowerCase();
  return MOCK_PEOPLE.filter((p) => p.name.toLowerCase().includes(q)).slice(0, limit);
}

function detailToSearchResult(d: TitleDetail): TitleSearchResult {
  return {
    provider: d.provider,
    provider_id: d.provider_id,
    media_type: d.media_type,
    title: d.title,
    original_title: d.original_title,
    year: d.year,
    release_date: d.release_date,
    overview_hint: d.overview_summary?.slice(0, 600) ?? null,
    genres: d.genres,
    attribution: d.attribution,
  };
}
