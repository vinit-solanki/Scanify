import { SparklesCore } from "./ui/sparkles";

export default function Footer() {
  const footerLinks = {
    Product: [
      { name: "Features", href: "#features" },
      { name: "Detection Modes", href: "#modes" },
      { name: "How it Works", href: "#how" },
      { name: "Pricing", href: "#pricing" },
    ],
    Resources: [
      { name: "Documentation", href: "#docs" },
      { name: "API Reference", href: "#api" },
      { name: "Nutrition Database", href: "#database" },
      { name: "Blog", href: "#blog" },
    ],
    Company: [
      { name: "About Us", href: "#about" },
      { name: "Careers", href: "#careers" },
      { name: "Privacy Policy", href: "#privacy" },
      { name: "Terms of Service", href: "#terms" },
    ],
  };

  const socialLinks = [
    { name: "Twitter", icon: "𝕏", href: "#" },
    { name: "GitHub", icon: "⚡", href: "#" },
    { name: "LinkedIn", icon: "in", href: "#" },
    { name: "Instagram", icon: "📷", href: "#" },
  ];

  return (
    <footer id="footer" className="border-t border-white/10 relative overflow-hidden bg-black text-white">
      <div className="absolute inset-0 opacity-40">
        <SparklesCore
          id="footer-sparkles"
          background="transparent"
          minSize={0.4}
          maxSize={1}
          particleDensity={80}
          className="h-full w-full"
          particleColor="#10b981"
        />
      </div>

      <div className="relative z-10">
        
        {/* Main Footer Content */}
        <div className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid gap-12 md:grid-cols-2 lg:grid-cols-5">
            {/* Brand Section */}
            <div className="lg:col-span-2 space-y-6">
              <div>
                <h3 className="text-3xl font-black tracking-tight">
                  Scanify
                </h3>
                <p className="mt-2 text-sm uppercase tracking-[0.3em] text-emerald-400/90">
                  OCR · Intelligence · Health
                </p>
              </div>
              <p className="text-neutral-300 max-w-md leading-relaxed">
                Instant label decoding with AI-powered nutrition analysis. 
                Make informed choices in seconds with precision health guardrails 
                tuned for your lifestyle.
              </p>
              
              {/* Social Links */}
              <div className="flex gap-3">
                {socialLinks.map((social) => (
                  <a
                    key={social.name}
                    href={social.href}
                    aria-label={social.name}
                    className="flex h-10 w-10 items-center justify-center rounded-full border border-white/15 bg-white/5 backdrop-blur transition hover:border-emerald-400/50 hover:bg-emerald-500/10 hover:shadow-[0_0_20px_rgba(16,185,129,0.3)]"
                  >
                    <span className="text-sm">{social.icon}</span>
                  </a>
                ))}
              </div>
            </div>

            {/* Links Sections */}
            {Object.entries(footerLinks).map(([category, links]) => (
              <div key={category}>
                <h4 className="mb-4 text-sm font-bold uppercase tracking-[0.2em] text-emerald-200/80">
                  {category}
                </h4>
                <ul className="space-y-3">
                  {links.map((link) => (
                    <li key={link.name}>
                      <a
                        href={link.href}
                        className="text-neutral-300 transition hover:text-emerald-400 hover:translate-x-1 inline-block"
                      >
                        {link.name}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10 bg-black/40 backdrop-blur">
          <div className="mx-auto max-w-7xl px-6 py-6">
            <div className="flex flex-col gap-4 text-center md:flex-row md:items-center md:justify-between md:text-left">
              <div className="flex flex-wrap justify-center gap-4 text-sm text-neutral-400 md:justify-start">
                <span>© 2025 Scanify. All rights reserved.</span>
                <span className="hidden md:inline">•</span>
                <span className="flex items-center gap-2">
                  Built with
                  <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" aria-hidden />
                  precision AI
                </span>
              </div>
              
              <div className="flex flex-wrap justify-center gap-6 text-sm md:justify-end">
                <a href="#privacy" className="text-neutral-400 transition hover:text-emerald-400">
                  Privacy
                </a>
                <a href="#terms" className="text-neutral-400 transition hover:text-emerald-400">
                  Terms
                </a>
                <a href="#cookies" className="text-neutral-400 transition hover:text-emerald-400">
                  Cookies
                </a>
                <a href="#accessibility" className="text-neutral-400 transition hover:text-emerald-400">
                  Accessibility
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
