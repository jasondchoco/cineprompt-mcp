import type { NextRequest } from "next/server";
import { checkDerivativeRisk } from "@/lib/services/prompt-safety";

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => ({}));
  const { text, reference_terms } = body as {
    text?: string;
    reference_terms?: string[];
  };

  if (!text?.trim()) return Response.json({ error: "text is required" }, { status: 400 });

  const report = checkDerivativeRisk(text, reference_terms ?? []);
  return Response.json(report);
}
