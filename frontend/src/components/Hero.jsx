import { Button } from "./ui/button";
import { SparklesCore } from "./ui/sparkles";
import { BackgroundBeams } from "./ui/background-beams";
import { HoverBorderGradient } from "./ui/hover-border-gradient";

const chips = [
  "Instant OCR verdicts",
  "Diabetes + weight modes",
  "Ingredient red-flags",
  "Explains every decision",
];

const metrics = [
  { label: "Labels decoded", value: "2.4M" },
  { label: "Avg. save time", value: "68%" },
  { label: "Cities covered", value: "40+" },
];

const scanHighlights = [
  { title: "Sugar", status: "3.2g", tone: "from-emerald-400 to-cyan-400" },
  { title: "Additives", status: "Clean", tone: "from-amber-300 to-orange-400" },
  { title: "Palm Oil", status: "None", tone: "from-pink-400 to-rose-500" },
  { title: "Refined flour", status: "Low", tone: "from-sky-300 to-blue-500" },
];

export default function Hero() {
  return (
    <section id="hero" className="mt-15 relative min-h-screen overflow-hidden bg-black text-white">
      <div className="absolute inset-0">
        <div className="absolute -left-20 top-10 h-72 w-72 rounded-full bg-emerald-500/25 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-cyan-500/20 blur-3xl" />
        <BackgroundBeams className="opacity-40" />
        <SparklesCore
          id="hero-sparkles"
          background="transparent"
          minSize={0.6}
          maxSize={1.4}
          particleDensity={140}
          className="absolute inset-0 h-full w-full"
          particleColor="#10b981"
        />
      </div>

      <div className="relative z-10 mx-auto grid max-w-6xl grid-cols-1 items-start gap-x-15 px-6 py-8 lg:grid-cols-2 lg:py-10">
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/40 bg-emerald-500/10 px-4 py-2 text-sm font-semibold tracking-tight shadow-[0_0_30px_rgba(16,185,129,0.25)]">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden />
            Real-time AI label guard
          </div>

          <h1 className="text-4xl font-black leading-tight sm:text-5xl lg:text-[3.25rem]">
            Scan. Decode. Decide.
            <span className="block bg-gradient-to-r from-emerald-400 via-cyan-300 to-white bg-clip-text text-transparent">
              Grocery labels, unraveled in seconds.
            </span>
          </h1>

          <p className="max-w-xl text-lg text-neutral-300">
            Drop any food label and get an instant verdict for diabetes safety, weight loss goals, and clean ingredients with receipts for every decision.
          </p>

          <div className="flex flex-wrap items-center gap-3">
            <Button className="bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-500 px-6 py-3 text-base font-semibold text-black shadow-[0_10px_50px_-15px_rgba(16,185,129,0.65)] transition hover:scale-[1.02]">
              Launch the scanner
            </Button>

            <HoverBorderGradient
              as="div"
              className="bg-white/10 px-5 py-3 text-sm font-semibold text-white"
              containerClassName="rounded-full"
            >
              Watch 45s demo →
            </HoverBorderGradient>
          </div>

        </div>

        <div className="relative mt-10 lg:mt-0">
          <div className="absolute inset-0 -skew-y-6 rounded-3xl bg-gradient-to-br from-emerald-400/15 via-cyan-400/10 to-transparent blur-3xl" aria-hidden />

          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur-2xl">
            <div className="flex items-center justify-between border-b border-white/10 px-6 py-4">
              <div className="text-xs uppercase tracking-[0.25em] text-emerald-100">Live scan</div>
              <div className="flex items-center gap-2 text-xs text-emerald-200">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" aria-hidden />
                Clean label
              </div>
            </div>

            <div className="space-y-4 px-6 py-6">
              <div className="grid grid-cols-2 gap-3 text-sm">
                {chips.map((item) => (
                  <div
                    key={item}
                    className="rounded-2xl border border-white/10 bg-black/40 px-4 py-3 text-neutral-200"
                  >
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-emerald-400" aria-hidden />
                      {item}
                    </div>
                  </div>
                ))}
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/70 p-5">
                <div className="flex items-center justify-between text-xs text-neutral-300">
                  <span>Ingredient radar</span>
                  <span className="text-emerald-300">Safe • Level 92</span>
                </div>
                <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
                  {scanHighlights.map((item) => (
                    <div
                      key={item.title}
                      className="rounded-xl border border-white/10 bg-white/5 p-3"
                    >
                      <div className="text-xs text-neutral-300">{item.title}</div>
                      <div className="mt-2 flex items-center justify-between">
                        <div className="h-2 w-24 rounded-full bg-white/10">
                          <div className={`h-2 w-3/4 rounded-full bg-gradient-to-r ${item.tone}`} />
                        </div>
                        <span className="text-sm font-semibold text-white">{item.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="mt-10 space-y-4">
            <div className="grid grid-cols-3 gap-3 sm:grid-cols-3">
              {metrics.map((item) => (
                <div
                  key={item.label}
                  className="rounded-2xl border border-white/10 bg-white/5 p-4 text-center backdrop-blur"
                >
                  <div className="text-2xl font-bold text-white">{item.value}</div>
                  <div className="text-xs text-neutral-300">{item.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
