"use client";

import { Film, Search, Shield, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const EXAMPLE_QUERIES = [
  "Parasite",
  "David Fincher",
  "Bong Joon-ho",
  "Succession",
  "Oldboy",
];

export default function HomePage() {
  const router = useRouter();
  const [query, setQuery] = useState("");

  function handleSearch(q: string) {
    const trimmed = q.trim();
    if (!trimmed) return;
    router.push(`/search?q=${encodeURIComponent(trimmed)}`);
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-4 py-16">
      <div className="w-full max-w-2xl space-y-8 text-center">
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs text-amber-400">
            <Sparkles className="h-3 w-3" />
            AI Video Prompt Generator
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-zinc-50 sm:text-5xl">
            Turn any film into an<br />
            <span className="text-amber-400">AI video blueprint</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-lg mx-auto">
            Search a movie, TV show, or director. Get a cinematic reference pack,
            shot list, and AI video prompt — without copying protected content.
          </p>
        </div>

        <div className="flex gap-2">
          <Input
            placeholder="Search a title or director…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch(query)}
            className="h-12 text-base"
          />
          <Button size="lg" onClick={() => handleSearch(query)} className="shrink-0 h-12 px-6">
            <Search className="h-4 w-4" />
            Search
          </Button>
        </div>

        <div className="flex flex-wrap gap-2 justify-center">
          {EXAMPLE_QUERIES.map((q) => (
            <button
              key={q}
              onClick={() => handleSearch(q)}
              className="rounded-full border border-zinc-700 px-3 py-1 text-sm text-zinc-400 hover:border-amber-500/50 hover:text-amber-400 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-4 pt-8 border-t border-zinc-800">
          {[
            { icon: Film, title: "12 Output Modules", desc: "Story engine, visual language, shot list" },
            { icon: Sparkles, title: "AI-Ready Prompts", desc: "Short, long, shot-by-shot formats" },
            { icon: Shield, title: "Copyright Safe", desc: "Derivative-risk checker built in" },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="flex flex-col items-center gap-1.5 text-center">
              <div className="rounded-lg bg-zinc-800 p-2">
                <Icon className="h-5 w-5 text-amber-400" />
              </div>
              <div className="text-sm font-medium text-zinc-200">{title}</div>
              <div className="text-xs text-zinc-500">{desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
