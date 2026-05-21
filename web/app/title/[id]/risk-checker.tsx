"use client";

import { AlertTriangle, CheckCircle, Loader2, ShieldOff, ShieldX } from "lucide-react";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import type { DerivativeRiskReport, RiskLevel } from "@/lib/schemas";

const RISK_CONFIG: Record<RiskLevel, { label: string; icon: React.ElementType; color: string }> = {
  low: { label: "Low Risk", icon: CheckCircle, color: "text-green-400" },
  medium: { label: "Medium Risk", icon: AlertTriangle, color: "text-yellow-400" },
  high: { label: "High Risk", icon: ShieldX, color: "text-orange-400" },
  block: { label: "Block", icon: ShieldOff, color: "text-red-400" },
};

export function RiskChecker() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<DerivativeRiskReport | null>(null);
  const [loading, setLoading] = useState(false);

  async function check() {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/risk-check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      setResult(await res.json());
    } finally {
      setLoading(false);
    }
  }

  const config = result ? RISK_CONFIG[result.level] : null;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm text-zinc-400">Derivative Risk Checker</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Textarea
            placeholder="Paste your prompt text here to check for copyright risk…"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={5}
          />
          <Button onClick={check} disabled={loading || !text.trim()} variant="secondary">
            {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Checking…</> : "Check Risk"}
          </Button>
        </CardContent>
      </Card>

      {result && config && (
        <Card>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <config.icon className={`h-5 w-5 ${config.color}`} />
              <CardTitle className={`text-sm ${config.color}`}>{config.label}</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            {result.matched_terms.length > 0 && (
              <div className="space-y-1.5">
                <p className="text-xs text-zinc-500 uppercase tracking-wide">Matched Terms</p>
                <div className="flex flex-wrap gap-1.5">
                  {result.matched_terms.map((t) => (
                    <Badge key={t} variant={result.level as RiskLevel}>{t}</Badge>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-1">
              <p className="text-xs text-zinc-500 uppercase tracking-wide">Warnings</p>
              {result.warnings.map((w, i) => (
                <p key={i} className="text-xs text-zinc-300">{w}</p>
              ))}
            </div>

            {result.safer_rewrite && (
              <div className="space-y-1 border-t border-zinc-800 pt-3">
                <p className="text-xs text-zinc-500 uppercase tracking-wide">Safer Approach</p>
                <p className="text-xs text-zinc-300 leading-relaxed">{result.safer_rewrite}</p>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
