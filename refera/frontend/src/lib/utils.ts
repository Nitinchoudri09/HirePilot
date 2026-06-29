import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string) {
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function scoreColor(score: number) {
  if (score >= 75) return "text-emerald-400";
  if (score >= 50) return "text-amber-400";
  return "text-red-400";
}

export function scoreBg(score: number) {
  if (score >= 75) return "from-emerald-500/20 to-emerald-600/10 border-emerald-500/30";
  if (score >= 50) return "from-amber-500/20 to-amber-600/10 border-amber-500/30";
  return "from-red-500/20 to-red-600/10 border-red-500/30";
}
