import type { NextRequest } from "next/server";
import { mockGetTitleDetail } from "@/lib/providers/mock";
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

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const mediaType = request.nextUrl.searchParams.get("media_type") as MediaType | null;
  const provider = getProvider();

  try {
    const detail =
      provider === "mock"
        ? mockGetTitleDetail(id)
        : provider === "omdb"
          ? await omdb.getTitleDetail(id, mediaType)
          : await tmdb.getTitleDetail(id, mediaType);
    return Response.json(detail);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    if (msg.includes("NOT_FOUND")) return Response.json({ error: "Not found." }, { status: 404 });
    return Response.json({ error: msg }, { status: 500 });
  }
}
