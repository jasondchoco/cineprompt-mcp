import type { NextRequest } from "next/server";
import { mockSearchPeople, mockSearchTitles } from "@/lib/providers/mock";
import { searchPeople, searchTitles } from "@/lib/providers/tmdb";
import type { MediaType } from "@/lib/schemas";

const useMock = () =>
  process.env.CINEPROMPT_PROVIDER === "mock" || !process.env.TMDB_API_KEY;

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const q = searchParams.get("q")?.trim();
  const type = searchParams.get("type") as "title" | "person" | null;
  const mediaType = searchParams.get("media_type") as MediaType | null;
  const year = searchParams.get("year") ? Number(searchParams.get("year")) : null;
  const limit = Math.min(Number(searchParams.get("limit") ?? "10"), 20);

  if (!q) return Response.json({ error: "q is required" }, { status: 400 });

  try {
    if (type === "person") {
      const results = useMock()
        ? mockSearchPeople(q, limit)
        : await searchPeople(q, limit);
      return Response.json(results);
    }

    const results = useMock()
      ? mockSearchTitles(q, limit)
      : await searchTitles(q, mediaType, year, limit);
    return Response.json(results);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    if (msg.includes("TMDB_AUTH_ERROR")) return Response.json({ error: "Invalid TMDb API key." }, { status: 401 });
    if (msg.includes("TMDB_NOT_FOUND")) return Response.json({ error: "Not found." }, { status: 404 });
    return Response.json({ error: msg }, { status: 500 });
  }
}
