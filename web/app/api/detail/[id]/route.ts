import type { NextRequest } from "next/server";
import { mockGetTitleDetail } from "@/lib/providers/mock";
import { getTitleDetail } from "@/lib/providers/tmdb";
import type { MediaType } from "@/lib/schemas";

const useMock = () =>
  process.env.CINEPROMPT_PROVIDER === "mock" || !process.env.TMDB_API_KEY;

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const mediaType = request.nextUrl.searchParams.get("media_type") as MediaType | null;

  try {
    const detail = useMock()
      ? mockGetTitleDetail(id)
      : await getTitleDetail(id, mediaType);
    return Response.json(detail);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    if (msg.includes("NOT_FOUND")) return Response.json({ error: "Not found." }, { status: 404 });
    return Response.json({ error: msg }, { status: 500 });
  }
}
