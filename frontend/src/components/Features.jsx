import { HoverEffect } from "./ui/card-hover-effect";
import { SparklesCore } from "./ui/sparkles";


export default function Features() {
  const items = [
    {
      title: "AI Label Scanner",
      description:
        "Understands ingredients, additives, and nutrition from Indian food labels.",
      link: "#",
    },
    {
      title: "Health Score",
      description:
        "Instant 0–100 score so you don’t have to read confusing labels.",
      link: "#",
    },
    {
      title: "Diabetes Mode",
      description:
        "Strict sugar & carb evaluation for blood glucose safety.",
      link: "#",
    },
    {
      title: "Weight Loss Mode",
      description:
        "Flags ultra-processed foods and empty calories.",
      link: "#",
    },
    {
      title: "Explainable AI",
      description:
        "Clear reasons behind every verdict. No black box.",
      link: "#",
    },
    {
      title: "Built for India",
      description:
        "Palm oil, maida, hidden sugars — we understand local food.",
      link: "#",
    },
  ];

  return (
    <section id="features" className="relative py-28 bg-black overflow-hidden">
      
      {/* Sparkle background */}
      <div className="absolute inset-0">
        <SparklesCore
          id="features-sparkles"
          background="transparent"
          minSize={0.4}
          maxSize={1.2}
          particleDensity={100}
          className="w-full h-full"
          particleColor="#10b981"
        />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6">
        <h2 className="text-5xl font-bold text-center text-white">
          Built for Smarter Eating
        </h2>

        <p className="mt-6 text-center text-neutral-400 max-w-2xl mx-auto">
          Scan food labels. Get real health insight. Make better choices.
        </p>

        <div className="mt-20">
          <HoverEffect items={items} />
        </div>
      </div>
    </section>
  );
}
