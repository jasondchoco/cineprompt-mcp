import type { NextRequest } from "next/server";
import { mockGetTitleDetail } from "@/lib/providers/mock";
import { getTitleDetail } from "@/lib/providers/tmdb";
import type { MediaType } from "@/lib/schemas";
import { buildReferencePackFromDetail } from "@/lib/services/reference-pack-builder";

const useMock = () =>
  process.env.CINEPROMPT_PROVIDER === "mock" || !process.env.TMDB_API_KEY;

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const { id, media_type, focus } = body as {
    id?: string;
    media_type?: MediaType;
    focus?: string;
  };

  if (!id) return Response.json({ error: "id is required" }, { status: 400 });

  try {
    const detail = useMock()
      ? mockGetTitleDetail(id)
      : await getTitleDetail(id, media_type);
    const pack = buildReferencePackFromDetail(detail, focus);
    return Response.json(pack);
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    if (msg.includes("NOT_FOUND")) return Response.json({ error: "Not found." }, { status: 404 });
    return Response.json({ error: msg }, { status: 500 });
  }
}
