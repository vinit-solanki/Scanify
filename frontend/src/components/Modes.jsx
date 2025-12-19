import { Card } from "./ui/card";
import { SparklesCore } from "./ui/sparkles";

const palette = {
  general: "from-emerald-400/30 via-cyan-400/20 to-transparent",
  diabetes: "from-rose-500/30 via-amber-400/20 to-transparent",
  weight_loss: "from-indigo-400/30 via-blue-400/20 to-transparent",
};

const modeDetails = {
  general: ["Balanced macros", "Additive screening", "Hydration + fiber"],
  diabetes: ["Strict sugar gates", "Net carb scoring", "Glycemic load view"],
  weight_loss: ["Ultra-processed flags", "Calories per serve", "Protein priority"],
};

export default function Modes() {
  const modes = [
    { id: "general", title: "General", desc: "Daily-friendly, balanced insight" },
    { id: "diabetes", title: "Diabetes", desc: "Sugar and carb compliance" },
    { id: "weight_loss", title: "Weight Loss", desc: "Low-kcal, high-protein focus" },
  ];

  return (
    <section id="modes" className="relative overflow-hidden bg-black py-16 px-6 text-white">
      <div className="absolute inset-0 opacity-60">
        <SparklesCore
          id="modes-sparkles"
          background="transparent"
          minSize={0.5}
          maxSize={1.2}
          particleDensity={120}
          className="h-full w-full"
          particleColor="#10b981"
        />
      </div>

      <div className="relative z-10 mx-auto max-w-6xl space-y-10">
        <div className="text-center space-y-3">
          <p className="text-sm uppercase tracking-[0.3em] text-emerald-200/80">
            Precision health rails
          </p>
          <h2 className="text-4xl font-black leading-tight sm:text-5xl">
            Choose your label-detection discipline
          </h2>
          <p className="text-neutral-300 max-w-2xl mx-auto">
            Snap between guardrails tuned for everyday balance, blood-glucose safety, or aggressive cut phases with instant OCR rules baked in.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {modes.map((mode) => (
            <Card
              key={mode.id}
              className="relative overflow-hidden border-white/10 bg-white/5 p-6 backdrop-blur transition duration-300 hover:-translate-y-1 hover:border-emerald-400/40 hover:shadow-[0_10px_40px_-25px_rgba(16,185,129,0.5)]"
            >
              <div
                className={`pointer-events-none absolute inset-0 bg-gradient-to-br ${palette[mode.id]}`}
                aria-hidden
              />
              <div className="relative space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs uppercase tracking-[0.2em] text-neutral-300">Mode</p>
                    <h3 className="text-2xl font-bold text-white">{mode.title}</h3>
                  </div>
                  <span className="rounded-full border border-white/15 bg-black/40 px-3 py-1 text-xs text-neutral-200">
                    OCR tuned
                  </span>
                </div>

                <p className="text-sm text-neutral-300">{mode.desc}</p>

                <div className="space-y-2">
                  {modeDetails[mode.id].map((item) => (
                    <div
                      key={item}
                      className="flex items-center gap-2 text-sm text-neutral-100"
                    >
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" aria-hidden />
                      {item}
                    </div>
                  ))}
                </div>

                <div className="flex items-center justify-end pt-4 text-sm text-neutral-200">
                  <span className="rounded-full border border-white/10 bg-white/10 px-3 py-1 text-xs">
                    {mode.id.replace("_", " ")}
                  </span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
