import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { HoverBorderGradient } from "./ui/hover-border-gradient";

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleNavClick = (href, isRoute) => {
    if (!isRoute) {
      // If we're not on the home page, navigate to home first then scroll
      if (location.pathname !== '/') {
        navigate('/');
        // Wait for navigation to complete, then scroll
        setTimeout(() => {
          const element = document.querySelector(href.replace('/#', '#'));
          if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
          }
        }, 100);
      } else {
        // If already on home page, just scroll
        const element = document.querySelector(href.replace('/#', '#'));
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }
    }
  };

  const navLinks = [
    { label: "Scanner", href: "/scan", isRoute: true },
    { label: "Features", href: "/#features", isRoute: false },
    { label: "Modes", href: "/#modes", isRoute: false },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-6">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
              <div className="text-2xl italic font-bold text-white">Scanify</div>

          {/* Desktop Nav */}
          <div className="hidden items-center gap-8 md:flex">
            {navLinks.map((link) => (
              link.isRoute ? (
                <Link
                  key={link.label}
                  to={link.href}
                  className="group flex items-center gap-2 text-sm font-semibold text-neutral-300 transition hover:text-emerald-300"
                >
                  {link.label}
                </Link>
              ) : (
                <button
                  key={link.label}
                  onClick={() => handleNavClick(link.href, link.isRoute)}
                  className="group flex items-center gap-2 text-sm font-semibold text-neutral-300 transition hover:text-emerald-300 cursor-pointer bg-transparent border-none"
                >
                  {link.label}
                </button>
              )
            ))}
          </div>

          {/* CTA */}
          <div className="hidden md:block">
            <button onClick={() => handleNavClick('/#footer', false)}>
              <HoverBorderGradient
                as="button"
                className="bg-white/10 px-5 py-2 text-sm font-semibold text-white"
                containerClassName="rounded-full"
              >
                Contact Us →
              </HoverBorderGradient>
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="rounded-lg border border-white/15 bg-white/5 p-2 text-white md:hidden"
            aria-label="Toggle menu"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {mobileOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileOpen && (
          <div className="border-t border-white/10 py-4 md:hidden">
            <div className="space-y-3">
              {navLinks.map((link) => (
                link.isRoute ? (
                  <Link
                    key={link.label}
                    to={link.href}
                    onClick={() => setMobileOpen(false)}
                    className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-sm font-semibold text-white transition hover:border-emerald-400/40"
                  >
                    {link.label}
                  </Link>
                ) : (
                  <button
                    key={link.label}
                    onClick={() => {
                      handleNavClick(link.href, link.isRoute);
                      setMobileOpen(false);
                    }}
                    className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 px-4 py-3 text-sm font-semibold text-white transition hover:border-emerald-400/40 w-full text-left"
                  >
                    {link.label}
                  </button>
                )
              ))}
              <button 
                onClick={() => {
                  handleNavClick('/#footer', false);
                  setMobileOpen(false);
                }}
                className="w-full rounded-full bg-gradient-to-r from-emerald-400 via-cyan-400 to-blue-500 px-5 py-3 text-sm font-semibold text-black block text-center"
              >
                Contact Us →
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
