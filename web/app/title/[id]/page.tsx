import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { ReferencePack, TitleDetail } from "@/lib/schemas";
import { PromptPanel } from "./prompt-panel";
import { RiskChecker } from "./risk-checker";

async function fetchDetail(id: string, mediaType: string): Promise<TitleDetail | null> {
  const base = process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000";
  const res = await fetch(
    `${base}/api/detail/${id}?media_type=${mediaType}`,
    { cache: "no-store" }
  );
  if (!res.ok) return null;
  return res.json();
}

async function fetchReferencePack(id: string, mediaType: string): Promise<ReferencePack | null> {
  const base = process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000";
  const res = await fetch(`${base}/api/reference-pack`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, media_type: mediaType }),
    cache: "no-store",
  });
  if (!res.ok) return null;
  return res.json();
}

export default async function TitlePage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ media_type?: string }>;
}) {
  const { id } = await params;
  const { media_type = "movie" } = await searchParams;

  const [detail, pack] = await Promise.all([
    fetchDetail(id, media_type),
    fetchReferencePack(id, media_type),
  ]);

  if (!detail || !pack) {
    return (
      <div className="flex flex-col items-center gap-4 py-24 text-zinc-500">
        <p className="text-lg">Title not found.</p>
        <Link href="/" className="text-amber-400 hover:underline text-sm">← Back to search</Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
      <Link
        href="/"
        className="inline-flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-100 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" /> Back to search
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-[320px_1fr] gap-6">
        {/* Left: Metadata panel */}
        <aside className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between gap-2">
                <CardTitle className="text-xl leading-snug">{detail.title}</CardTitle>
                <Badge variant="secondary">{detail.media_type === "tv" ? "TV" : "Film"}</Badge>
              </div>
              {detail.year && (
                <p className="text-sm text-zinc-400">{detail.year}</p>
              )}
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              {detail.overview_summary && (
                <p className="text-zinc-300 leading-relaxed">{detail.overview_summary}</p>
              )}

              {detail.genres.length > 0 && (
                <div className="space-y-1.5">
                  <p className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Genres</p>
                  <div className="flex flex-wrap gap-1">
                    {detail.genres.map((g) => (
                      <Badge key={g} variant="outline">{g}</Badge>
                    ))}
                  </div>
                </div>
              )}

              {detail.directors.length > 0 && (
                <div className="space-y-1">
                  <p className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Director</p>
                  <p className="text-zinc-300">{detail.directors.join(", ")}</p>
                </div>
              )}

              {detail.cast.length > 0 && (
                <div className="space-y-1">
                  <p className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Cast</p>
                  <p className="text-zinc-400">{detail.cast.slice(0, 6).join(", ")}</p>
                </div>
              )}

              {detail.keywords.length > 0 && (
                <div className="space-y-1.5">
                  <p className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Keywords</p>
                  <div className="flex flex-wrap gap-1">
                    {detail.keywords.slice(0, 10).map((k) => (
                      <Badge key={k} variant="secondary" className="text-xs">{k}</Badge>
                    ))}
                  </div>
                </div>
              )}

              {detail.runtime_minutes && (
                <div className="space-y-1">
                  <p className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Runtime</p>
                  <p className="text-zinc-400">{detail.runtime_minutes} min</p>
                </div>
              )}

              {detail.production_countries.length > 0 && (
                <div className="space-y-1">
                  <p className="text-xs font-medium text-zinc-500 uppercase tracking-wide">Country</p>
                  <p className="text-zinc-400">{detail.production_countries.join(", ")}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </aside>

        {/* Right: Tabs */}
        <div className="space-y-4">
          <Tabs defaultValue="reference">
            <TabsList>
              <TabsTrigger value="reference">Reference Pack</TabsTrigger>
              <TabsTrigger value="prompt">Video Prompt</TabsTrigger>
              <TabsTrigger value="risk">Risk Check</TabsTrigger>
            </TabsList>

            <TabsContent value="reference" className="space-y-4 mt-4">
              <ReferencePackView pack={pack} />
            </TabsContent>

            <TabsContent value="prompt" className="mt-4">
              <PromptPanel titleId={id} mediaType={media_type} />
            </TabsContent>

            <TabsContent value="risk" className="mt-4">
              <RiskChecker />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}

function ReferencePackView({ pack }: { pack: ReferencePack }) {
  const vl = pack.visual_language;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-amber-400">Story Engine</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-zinc-300 leading-relaxed">{pack.story_engine}</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-amber-400">Character Dynamics</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {pack.character_dynamics.map((d, i) => (
                <li key={i} className="text-xs text-zinc-300 flex gap-2">
                  <span className="text-amber-500 shrink-0">·</span>
                  {d}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-amber-400">Genre Mechanics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-1.5">
              {pack.genre_mechanics.map((m) => (
                <Badge key={m} variant="secondary">{m}</Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm text-amber-400">Visual Language</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            {Object.entries(vl).map(([key, values]) => (
              <div key={key} className="space-y-1.5">
                <p className="font-medium text-zinc-500 uppercase tracking-wide">{key}</p>
                <div className="flex flex-wrap gap-1">
                  {values.map((v: string) => (
                    <Badge key={v} variant="outline" className="text-xs">{v}</Badge>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-amber-400">Prompt Hooks</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {pack.prompt_hooks.map((h, i) => (
                <li key={i} className="text-xs text-zinc-300 flex gap-2">
                  <span className="text-amber-500 shrink-0">→</span>
                  {h}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-zinc-400">Risk Notes</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {pack.risk_notes.map((n, i) => (
                <li key={i} className="text-xs text-zinc-400 flex gap-2">
                  <span className="text-red-500 shrink-0">!</span>
                  {n}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
