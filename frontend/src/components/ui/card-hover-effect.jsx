"use client";
import { cn } from "@/lib/utils";

export const HoverEffect = ({ items, className }) => {
  return (
    <div
      className={cn(
        "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        className
      )}
    >
      {items.map((item, idx) => (
        <div
          key={idx}
          className="group relative block p-6 h-full w-full"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-xl blur opacity-0 group-hover:opacity-100 transition duration-500" />
          <div className="relative z-10 bg-neutral-900 rounded-xl p-6 h-full border border-neutral-800">
            <h3 className="text-white text-lg font-semibold">
              {item.title}
            </h3>
            <p className="mt-4 text-neutral-400 text-sm">
              {item.description}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};
