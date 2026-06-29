"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, Sparkles } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";

const navLinks = [
  { href: "/#features", label: "Features" },
  { href: "/#how-it-works", label: "How it Works" },
  { href: "/pricing", label: "Pricing" },
  { href: "/#faq", label: "FAQ" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { user } = useAuth();

  return (
    <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-[#030712]/80 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 shadow-lg shadow-brand-500/30 transition-transform group-hover:scale-105">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <span className="font-display text-xl font-bold tracking-tight">
            Refer<span className="gradient-text">a</span>
          </span>
        </Link>

        <div className="hidden items-center gap-8 md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-slate-400 transition-colors hover:text-white"
            >
              {link.label}
            </Link>
          ))}
        </div>

        <div className="hidden items-center gap-3 md:flex">
          {user ? (
            <Link href="/dashboard" className="btn-primary text-sm py-2.5 px-5">
              Dashboard
            </Link>
          ) : (
            <>
              <Link href="/login" className="text-sm text-slate-300 hover:text-white transition-colors">
                Log in
              </Link>
              <Link href="/signup" className="btn-primary text-sm py-2.5 px-5">
                Get Started
              </Link>
            </>
          )}
        </div>

        <button
          className="md:hidden text-slate-300"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </nav>

      <div className={cn("md:hidden border-t border-white/5 bg-[#030712]/95", open ? "block" : "hidden")}>
        <div className="flex flex-col gap-4 px-4 py-6">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} className="text-slate-300" onClick={() => setOpen(false)}>
              {link.label}
            </Link>
          ))}
          <div className="flex flex-col gap-3 pt-2">
            {user ? (
              <Link href="/dashboard" className="btn-primary text-center" onClick={() => setOpen(false)}>
                Dashboard
              </Link>
            ) : (
              <>
                <Link href="/login" className="btn-secondary text-center" onClick={() => setOpen(false)}>
                  Log in
                </Link>
                <Link href="/signup" className="btn-primary text-center" onClick={() => setOpen(false)}>
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
