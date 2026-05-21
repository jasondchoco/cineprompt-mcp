import type { MediaType, PersonSearchResult, TitleDetail, TitleSearchResult } from "../schemas";

const BASE_URL = process.env.OMDB_BASE_URL ?? "http://www.omdbapi.com/";
const ATTRIBUTION_NOTE = "Movie and TV data provided by OMDb API (omdbapi.com).";

const TYPE_MAP: Record<string, MediaType> = {
  movie: "movie",
  series: "tv",
};

function getApiKey(): string {
  const key = process.env.OMDB_API_KEY;
  if (!key) throw new Error("OMDB_API_KEY environment variable is not set.");
  return key;
}

async function omdbFetch<T>(params: Record<string, string>): Promise<T> {
  const url = new URL(BASE_URL);
  url.searchParams.set("apikey", getApiKey());
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  const res = await fetch(url.toString(), { next: { revalidate: 300 } });
  if (res.status === 401 || res.status === 403) throw new Error("OMDB_AUTH_ERROR: Invalid API key.");
  if (!res.ok) throw new Error(`OMDB_UNAVAILABLE: ${res.status}`);
  return res.json() as Promise<T>;
}

function attribution(imdbID: string) {
  return {
    provider: "omdb",
    provider_id: imdbID,
    source_url: `https://www.imdb.com/title/${imdbID}/`,
    license_note: ATTRIBUTION_NOTE,
  };
}

function parseYear(raw: string | undefined): number | null {
  if (!raw) return null;
  const m = raw.match(/\d{4}/);
  return m ? parseInt(m[0], 10) : null;
}

function parseRuntime(raw: string | undefined): number | null {
  if (!raw || raw === "N/A") return null;
  const m = raw.match(/(\d+)/);
  return m ? parseInt(m[0], 10) : null;
}

function splitCsv(raw: string | undefined): string[] {
  if (!raw || raw === "N/A") return [];
  return raw.split(",").map((s) => s.trim()).filter(Boolean);
}

function parseDate(raw: string | undefined): string | null {
  if (!raw || raw === "N/A") return null;
  const formats = [
    { regex: /^\d{4}-\d{2}-\d{2}$/, parse: (s: string) => s },
    {
      regex: /^(\d{2}) (\w{3}) (\d{4})$/,
      parse: (s: string) => {
        const d = new Date(s);
        return isNaN(d.getTime()) ? null : d.toISOString().slice(0, 10);
      },
    },
  ];
  for (const { regex, parse } of formats) {
    if (regex.test(raw)) return parse(raw);
  }
  return null;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mapSearchItem(item: Record<string, any>, requestedType: MediaType | null): TitleSearchResult | null {
  const mediaType: MediaType = TYPE_MAP[item.Type] ?? requestedType ?? "movie";
  if (!["movie", "tv"].includes(mediaType)) return null;
  const id = item.imdbID as string;
  const title = item.Title as string;
  if (!id || !title) return null;
  return {
    provider: "omdb",
    provider_id: id,
    media_type: mediaType,
    title,
    original_title: null,
    year: parseYear(item.Year),
    release_date: null,
    overview_hint: null,
    genres: [],
    attribution: attribution(id),
  };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function mapDetail(data: Record<string, any>): TitleDetail {
  const id = data.imdbID as string;
  const title = data.Title as string;
  if (!id || !title) throw new Error("OMDB_UNAVAILABLE: missing required fields");
  const mediaType: MediaType = TYPE_MAP[data.Type] ?? "movie";
  const countries = splitCsv(data.Country).map((c) => c.slice(0, 2).toUpperCase());
  return {
    provider: "omdb",
    provider_id: id,
    media_type: mediaType,
    title,
    original_title: null,
    year: parseYear(data.Year),
    release_date: parseDate(data.Released),
    runtime_minutes: parseRuntime(data.Runtime),
    genres: splitCsv(data.Genre),
    overview_summary: data.Plot && data.Plot !== "N/A" ? (data.Plot as string) : null,
    directors: splitCsv(data.Director),
    creators: splitCsv(data.Writer),
    cast: splitCsv(data.Actors).slice(0, 20),
    keywords: [],
    production_countries: countries,
    attribution: attribution(id),
  };
}

export async function searchTitles(
  query: string,
  mediaType: MediaType | null,
  year: number | null,
  limit: number,
): Promise<TitleSearchResult[]> {
  const params: Record<string, string> = { s: query };
  if (mediaType === "movie") params.type = "movie";
  else if (mediaType === "tv") params.type = "series";
  if (year) params.y = String(year);

  const data = await omdbFetch<Record<string, unknown>>(params);
  if (data.Response === "False") return [];

  const items = (data.Search as Record<string, unknown>[] | undefined) ?? [];
  const results: TitleSearchResult[] = [];
  for (const item of items) {
    const mapped = mapSearchItem(item as Record<string, string>, mediaType);
    if (mapped) results.push(mapped);
    if (results.length >= limit) break;
  }
  return results;
}

export async function getTitleDetail(
  id: string,
  _mediaType: MediaType | null,
): Promise<TitleDetail> {
  const data = await omdbFetch<Record<string, unknown>>({ i: id, plot: "full" });
  if (data.Response === "False") throw new Error("OMDB_NOT_FOUND");
  return mapDetail(data as Record<string, string>);
}

export function searchPeople(_query: string, _limit: number): PersonSearchResult[] {
  return [];
}
