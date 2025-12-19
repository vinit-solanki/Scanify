import { useState } from "react";
import { analyzeProduct } from "../lib/api";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { SparklesCore } from "./ui/sparkles";

export default function ProductInsight({ mode }) {
  const [labelText, setLabelText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    setLoading(true);
    try {
      const data = await analyzeProduct({ labelText, mode });
      setResult(data);
    } catch (err) {
      alert("Analysis failed");
    }
    setLoading(false);
  }

  const chips = ["AI OCR", "Macro rules", "Additive watch", "Local ingredients"];

  return (
    <section className="relative overflow-hidden bg-black py-16 px-6 text-white">
      <div className="absolute inset-0 opacity-60">
        <SparklesCore
          id="insight-sparkles"
          background="transparent"
          minSize={0.5}
          maxSize={1.2}
          particleDensity={140}
          className="h-full w-full"
          particleColor="#10b981"
        />
      </div>

      <div className="relative z-10 mx-auto max-w-6xl grid gap-8 lg:grid-cols-[1.1fr_0.9fr] items-start">
        <Card className="relative border-white/10 bg-white/5 p-6 backdrop-blur">
          <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-emerald-500/10 via-cyan-400/5 to-transparent" aria-hidden />
          <div className="relative space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-emerald-200">Input</p>
                <h2 className="text-2xl font-bold text-white">Paste ingredients / nutrition</h2>
              </div>
              <span className="rounded-full border border-white/20 bg-white/10 px-3 py-1 text-xs text-neutral-200">
                Mode: {mode.replace("_", " ")}
              </span>
            </div>

            <textarea
              className="w-full h-48 rounded-xl border border-white/15 bg-black/40 p-3 text-sm text-white placeholder:text-neutral-500 focus:border-emerald-400 focus:outline-none"
              placeholder="Ingredients, sugar, fat, sodium, allergens, additives..."
              value={labelText}
              onChange={(e) => setLabelText(e.target.value)}
            />

            <div className="flex flex-wrap gap-2">
              {chips.map((chip) => (
                <span
                  key={chip}
                  className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs text-neutral-200"
                >
                  {chip}
                </span>
              ))}
            </div>

            <Button
              className="w-full bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-500 text-black font-semibold"
              onClick={handleAnalyze}
              disabled={loading || !labelText.trim()}
            >
              {loading ? "Analyzing..." : "Analyze product"}
            </Button>
          </div>
        </Card>

        <Card className="relative border-white/10 bg-white/5 p-6 backdrop-blur">
          <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-emerald-400/10 via-emerald-500/5 to-transparent" aria-hidden />
          <div className="relative space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-emerald-200">Verdict</p>
                <h3 className="text-xl font-bold text-white">{result ? result.classification.health_category : "Awaiting scan"}</h3>
              </div>
              <div className="rounded-full border border-white/15 bg-black/40 px-3 py-1 text-xs text-neutral-200">
                {result ? `${result.classification.health_score}/100` : "—"}
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/50 p-4">
              <p className="text-xs uppercase tracking-[0.2em] text-neutral-300">Key reasons</p>
              <div className="mt-3 space-y-2 text-sm text-neutral-100">
                {result ? (
                  result.classification.reasons.map((r) => (
                    <div key={r} className="flex items-start gap-2">
                      <span className="mt-1 h-1.5 w-1.5 rounded-full bg-emerald-400" aria-hidden />
                      <span>{r.replaceAll("_", " ")}</span>
                    </div>
                  ))
                ) : (
                  <div className="text-neutral-400">Paste a label to see the breakdown.</div>
                )}
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/40 p-4 text-sm text-neutral-200">
              <p className="text-xs uppercase tracking-[0.2em] text-neutral-300">Summary</p>
              <div className="mt-2 text-neutral-100">
                {result ? result.explanation.summary : "We will synthesize the verdict, call out risks (sugar, oils, additives), and give a go / caution / avoid recommendation."}
              </div>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
}
