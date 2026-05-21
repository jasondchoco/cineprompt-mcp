import type { NextRequest } from "next/server";
import { mockSearchPeople, mockSearchTitles } from "@/lib/providers/mock";
import * as omdb from "@/lib/providers/omdb";
import * as tmdb from "@/lib/providers/tmdb";
import type { MediaType } from "@/lib/schemas";

function getProvider() {
  const p = process.env.CINEPROMPT_PROVIDER;
  if (p === "omdb" && process.env.OMDB_API_KEY) return "omdb";
  if (p === "mock" || (!process.env.TMDB_API_KEY && !process.env.OMDB_API_KEY)) return "mock";
  if (process.env.OMDB_API_KEY) return "omdb";
  return "tmdb";
}

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const q = searchParams.get("q")?.trim();
  const type = searchParams.get("type") as "title" | "person" | null;
  const mediaType = searchParams.get("media_type") as MediaType | null;
  const year = searchParams.get("year") ? Number(searchParams.get("year")) : null;
  const limit = Math.min(Number(searchParams.get("limit") ?? "10"), 20);

  if (!q) return Response.json({ error: "q is required" }, { status: 400 });

  const provider = getProvider();

  try {
    if (type === "person") {
      const results =
        provider === "mock"
          ? mockSearchPeople(q, limit)
          : provider === "omdb"
            ? omdb.searchPeople(q, limit)
            : await tmdb.searchPeople(q, limit);
      return Response.json(results);
    }

    const results =
      provider === "mock"
        ? mockSearchTitles(q, limit)
        : provider === "omdb"
          ? await omdb.searchTitles(q, mediaType, year, limit)
          : await tmdb.searchTitles(q, mediaType, year, limit);
    return Response.json(results);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    if (msg.includes("AUTH_ERROR")) return Response.json({ error: "Invalid API key." }, { status: 401 });
    if (msg.includes("NOT_FOUND")) return Response.json({ error: "Not found." }, { status: 404 });
    return Response.json({ error: msg }, { status: 500 });
  }
}
