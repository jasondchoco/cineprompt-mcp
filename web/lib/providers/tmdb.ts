import type {
  MediaType,
  PersonSearchResult,
  TitleDetail,
  TitleSearchResult,
} from "../schemas";

const BASE_URL = process.env.TMDB_BASE_URL ?? "https://api.themoviedb.org/3";

function getApiKey(): string {
  const key = process.env.TMDB_API_KEY;
  if (!key) throw new Error("TMDB_API_KEY environment variable is not set.");
  return key;
}

async function tmdbFetch<T>(path: string, params: Record<string, string> = {}): Promise<T> {
  const url = new URL(`${BASE_URL}${path}`);
  url.searchParams.set("api_key", getApiKey());
  url.searchParams.set("include_adult", "false");
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);

  const res = await fetch(url.toString(), { next: { revalidate: 300 } });
  if (res.status === 401 || res.status === 403) throw new Error("TMDB_AUTH_ERROR: Invalid API key.");
  if (res.status === 404) throw new Error("TMDB_NOT_FOUND");
  if (!res.ok) throw new Error(`TMDB_UNAVAILABLE: ${res.status}`);
  return res.json() as Promise<T>;
}

function toAttribution(provider_id: string) {
  return {
    provider: "tmdb",
    provider_id,
    source_url: `https://www.themoviedb.org/movie/${provider_id}`,
    license_note: "Data from The Movie Database (TMDb). Not endorsed by TMDb.",
  };
}

function normalizeMediaType(raw: string): MediaType {
  return raw === "tv" ? "tv" : "movie";
}

export async function searchTitles(
  query: string,
  mediaType?: MediaType | null,
  year?: number | null,
  limit = 5
): Promise<TitleSearchResult[]> {
  const path = mediaType ? `/search/${mediaType}` : "/search/multi";
  const params: Record<string, string> = { query, page: "1" };
  if (year) params[mediaType === "tv" ? "first_air_date_year" : "year"] = String(year);

  const data = await tmdbFetch<{ results: Record<string, unknown>[] }>(path, params);

  return data.results
    .filter((r) => {
      const mt = (r.media_type as string) ?? mediaType ?? "movie";
      return mt === "movie" || mt === "tv";
    })
    .slice(0, limit)
    .map((r) => {
      const mt = normalizeMediaType((r.media_type as string) ?? mediaType ?? "movie");
      const id = String(r.id);
      return {
        provider: "tmdb",
        provider_id: id,
        media_type: mt,
        title: (r.title as string) ?? (r.name as string) ?? "",
        original_title: (r.original_title as string) ?? (r.original_name as string) ?? null,
        year: r.release_date
          ? Number((r.release_date as string).slice(0, 4))
          : r.first_air_date
            ? Number((r.first_air_date as string).slice(0, 4))
            : null,
        release_date:
          (r.release_date as string) ?? (r.first_air_date as string) ?? null,
        overview_hint: ((r.overview as string) ?? "").slice(0, 600) || null,
        genres: [],
        attribution: toAttribution(id),
      };
    });
}

export async function searchPeople(query: string, limit = 5): Promise<PersonSearchResult[]> {
  const data = await tmdbFetch<{ results: Record<string, unknown>[] }>("/search/person", {
    query,
    page: "1",
  });

  return data.results.slice(0, limit).map((r) => {
    const knownFor = (r.known_for as Record<string, unknown>[]) ?? [];
    return {
      provider: "tmdb",
      provider_id: String(r.id),
      name: (r.name as string) ?? "",
      known_for_department: (r.known_for_department as string) ?? null,
      known_for_titles: knownFor
        .slice(0, 10)
        .map((k) => ((k.title as string) ?? (k.name as string) ?? ""))
        .filter(Boolean),
      attribution: {
        provider: "tmdb",
        provider_id: String(r.id),
        source_url: `https://www.themoviedb.org/person/${r.id}`,
        license_note: "Data from The Movie Database (TMDb). Not endorsed by TMDb.",
      },
    };
  });
}

export async function getTitleDetail(
  id: string,
  mediaType?: MediaType | null
): Promise<TitleDetail> {
  const mt = mediaType ?? "movie";
  const data = await tmdbFetch<Record<string, unknown>>(`/${mt}/${id}`, {
    append_to_response: "credits,keywords",
  });

  const credits = (data.credits as Record<string, unknown>) ?? {};
  const crew = (credits.crew as Record<string, unknown>[]) ?? [];
  const cast = (credits.cast as Record<string, unknown>[]) ?? [];
  const keywordsWrapper = (data.keywords as Record<string, unknown>) ?? {};
  const keywordsArr =
    ((keywordsWrapper.keywords as Record<string, unknown>[]) ??
      (keywordsWrapper.results as Record<string, unknown>[]) ??
      []);

  return {
    provider: "tmdb",
    provider_id: id,
    media_type: mt,
    title: (data.title as string) ?? (data.name as string) ?? "",
    original_title: (data.original_title as string) ?? (data.original_name as string) ?? null,
    year: data.release_date
      ? Number((data.release_date as string).slice(0, 4))
      : data.first_air_date
        ? Number((data.first_air_date as string).slice(0, 4))
        : null,
    release_date: (data.release_date as string) ?? (data.first_air_date as string) ?? null,
    runtime_minutes: (data.runtime as number) ?? null,
    genres: ((data.genres as { name: string }[]) ?? []).map((g) => g.name),
    overview_summary: ((data.overview as string) ?? "").slice(0, 1200) || null,
    directors: crew
      .filter((c) => c.job === "Director")
      .slice(0, 10)
      .map((c) => c.name as string),
    creators: ((data.created_by as { name: string }[]) ?? [])
      .slice(0, 10)
      .map((c) => c.name),
    cast: cast
      .slice(0, 20)
      .map((c) => c.name as string),
    keywords: keywordsArr
      .slice(0, 30)
      .map((k) => k.name as string),
    production_countries: (
      (data.production_countries as { iso_3166_1: string }[]) ?? []
    ).map((c) => c.iso_3166_1),
    attribution: toAttribution(id),
  };
}

export async function getPersonFilmography(
  id: string,
  limit = 10
): Promise<TitleSearchResult[]> {
  const data = await tmdbFetch<{
    cast: Record<string, unknown>[];
    crew: Record<string, unknown>[];
  }>(`/person/${id}/combined_credits`);

  const all = [...(data.cast ?? []), ...(data.crew ?? [])]
    .filter((r) => {
      const mt = r.media_type as string;
      return mt === "movie" || mt === "tv";
    })
    .sort((a, b) => ((b.popularity as number) ?? 0) - ((a.popularity as number) ?? 0))
    .slice(0, limit);

  return all.map((r) => {
    const mt = normalizeMediaType(r.media_type as string);
    const rid = String(r.id);
    return {
      provider: "tmdb",
      provider_id: rid,
      media_type: mt,
      title: (r.title as string) ?? (r.name as string) ?? "",
      original_title: null,
      year: r.release_date
        ? Number((r.release_date as string).slice(0, 4))
        : r.first_air_date
          ? Number((r.first_air_date as string).slice(0, 4))
          : null,
      release_date:
        (r.release_date as string) ?? (r.first_air_date as string) ?? null,
      overview_hint: null,
      genres: [],
      attribution: toAttribution(rid),
    };
  });
}
