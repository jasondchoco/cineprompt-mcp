import { Search } from "lucide-react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import type { TitleSearchResult } from "@/lib/schemas";

async function fetchResults(q: string): Promise<TitleSearchResult[]> {
  const base = process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000";
  const res = await fetch(`${base}/api/search?q=${encodeURIComponent(q)}&limit=12`, {
    cache: "no-store",
  });
  if (!res.ok) return [];
  return res.json();
}

export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  const { q } = await searchParams;
  const query = q?.trim() ?? "";

  if (!query) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-3 text-zinc-500">
        <Search className="h-8 w-8" />
        <p>Enter a search term to find titles.</p>
      </div>
    );
  }

  const results = await fetchResults(query);

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-semibold text-zinc-100">
          Results for <span className="text-amber-400">&ldquo;{query}&rdquo;</span>
        </h1>
        <span className="text-sm text-zinc-500">{results.length} titles</span>
      </div>

      {results.length === 0 ? (
        <div className="flex flex-col items-center gap-3 py-16 text-zinc-500">
          <Search className="h-8 w-8" />
          <p>No titles found. Try a different search.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {results.map((r) => (
            <Link key={r.provider_id} href={`/title/${r.provider_id}?media_type=${r.media_type}`}>
              <Card className="h-full hover:border-amber-500/50 transition-colors cursor-pointer">
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between gap-2">
                    <CardTitle className="text-base leading-snug">{r.title}</CardTitle>
                    <Badge variant="secondary" className="shrink-0 text-xs">
                      {r.media_type === "tv" ? "TV" : "Film"}
                    </Badge>
                  </div>
                  {r.year && (
                    <p className="text-xs text-zinc-500">{r.year}</p>
                  )}
                </CardHeader>
                <CardContent className="space-y-3">
                  {r.genres.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {r.genres.slice(0, 3).map((g) => (
                        <Badge key={g} variant="outline" className="text-xs">
                          {g}
                        </Badge>
                      ))}
                    </div>
                  )}
                  {r.overview_hint && (
                    <p className="text-xs text-zinc-400 line-clamp-3">{r.overview_hint}</p>
                  )}
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export function SearchPageSkeleton() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-5 w-3/4" />
              <Skeleton className="h-3 w-1/4 mt-1" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-12 w-full" />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
