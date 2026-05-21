"use client";

import { Check, Copy, Loader2 } from "lucide-react";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import type { VideoPromptPack } from "@/lib/schemas";

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  async function handleCopy() {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  }
  return (
    <Button variant="ghost" size="icon" onClick={handleCopy} className="h-7 w-7">
      {copied ? <Check className="h-3.5 w-3.5 text-green-400" /> : <Copy className="h-3.5 w-3.5" />}
    </Button>
  );
}

export function PromptPanel({ titleId, mediaType }: { titleId: string; mediaType: string }) {
  const [duration, setDuration] = useState(20);
  const [ratio, setRatio] = useState("16:9");
  const [result, setResult] = useState<VideoPromptPack | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function generate() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/video-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: titleId, media_type: mediaType, duration_seconds: duration, aspect_ratio: ratio }),
      });
      if (!res.ok) throw new Error((await res.json()).error ?? "Failed");
      setResult(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-5">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm text-amber-400">Prompt Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-zinc-400">Duration</span>
              <span className="font-medium text-zinc-200">{duration}s</span>
            </div>
            <Slider
              min={5}
              max={120}
              step={5}
              value={[duration]}
              onValueChange={([v]) => setDuration(v)}
            />
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm text-zinc-400 shrink-0">Aspect ratio</span>
            <Select value={ratio} onValueChange={setRatio}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="16:9">16:9 (Wide)</SelectItem>
                <SelectItem value="9:16">9:16 (Vertical)</SelectItem>
                <SelectItem value="1:1">1:1 (Square)</SelectItem>
                <SelectItem value="4:3">4:3 (Classic)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button onClick={generate} disabled={loading} className="w-full">
            {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Generating…</> : "Generate Prompts"}
          </Button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </CardContent>
      </Card>

      {result && (
        <div className="space-y-4">
          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm text-amber-400">Short Prompt</CardTitle>
                <CopyButton text={result.short_prompt} />
              </div>
            </CardHeader>
            <CardContent>
              <Textarea value={result.short_prompt} readOnly rows={3} className="resize-none text-xs" />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm text-amber-400">Long Prompt</CardTitle>
                <CopyButton text={result.long_prompt} />
              </div>
            </CardHeader>
            <CardContent>
              <Textarea value={result.long_prompt} readOnly rows={6} className="resize-none text-xs" />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-amber-400">Shot List</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="space-y-2">
                {result.shot_list.map((shot, i) => (
                  <li key={i} className="flex gap-3 text-xs text-zinc-300">
                    <span className="text-amber-500 font-mono shrink-0">{i + 1}.</span>
                    {shot}
                  </li>
                ))}
              </ol>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-zinc-400">Negative Prompt</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-1.5">
                {result.negative_prompt.map((n) => (
                  <Badge key={n} variant="outline" className="text-xs">{n}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
