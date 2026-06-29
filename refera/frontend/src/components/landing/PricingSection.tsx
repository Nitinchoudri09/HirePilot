"use client";

import Link from "next/link";
import { Check, Crown, Sparkles } from "lucide-react";

const plans = [
  {
    id: "free",
    name: "Free",
    price: 0,
    period: "forever",
    description: "Perfect for getting started with referrals",
    features: [
      "3 referral requests/month",
      "Basic ATS score",
      "Job matching",
      "AI eligibility chatbot",
      "Resume parsing (PDF/DOCX)",
    ],
    cta: "Get Started",
    href: "/signup",
    highlighted: false,
  },
  {
    id: "premium",
    name: "Premium",
    price: 999,
    period: "month",
    description: "For serious job seekers who want maximum reach",
    features: [
      "25 referral requests/month",
      "Advanced ATS analysis",
      "AI referral message generator",
      "Interview question generator",
      "Priority job matching",
      "Premium support",
    ],
    cta: "Upgrade to Premium",
    href: "/signup?plan=premium",
    highlighted: true,
  },
];

export default function PricingSection({ compact = false }: { compact?: boolean }) {
  return (
    <section id="pricing" className={compact ? "section-padding" : "section-padding bg-[#020617]"}>
      <div className="mx-auto max-w-7xl">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="font-display text-3xl sm:text-4xl font-bold">
            Simple, transparent <span className="gradient-text">pricing</span>
          </h2>
          {!compact && (
            <p className="mt-4 text-slate-400">Start free. Upgrade when you&apos;re ready to scale your job search.</p>
          )}
        </div>
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative rounded-2xl p-8 transition-all ${
                plan.highlighted
                  ? "bg-gradient-to-b from-brand-600/20 to-violet-600/10 border-2 border-brand-500/40 shadow-xl shadow-brand-500/10"
                  : "glass-card"
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 flex items-center gap-1 rounded-full bg-gradient-to-r from-brand-500 to-violet-500 px-3 py-1 text-xs font-semibold">
                  <Crown className="h-3 w-3" /> Most Popular
                </div>
              )}
              <div className="flex items-center gap-2 mb-2">
                {plan.highlighted && <Sparkles className="h-5 w-5 text-brand-400" />}
                <h3 className="text-xl font-bold">{plan.name}</h3>
              </div>
              <p className="text-sm text-slate-400 mb-6">{plan.description}</p>
              <div className="mb-6">
                <span className="text-4xl font-bold">
                  {plan.price === 0 ? "Free" : `₹${plan.price}`}
                </span>
                {plan.price > 0 && <span className="text-slate-500 text-sm">/{plan.period}</span>}
              </div>
              <ul className="space-y-3 mb-8">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-slate-300">
                    <Check className="h-4 w-4 text-emerald-400 mt-0.5 shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link
                href={plan.href}
                className={plan.highlighted ? "btn-primary w-full text-center" : "btn-secondary w-full text-center"}
              >
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
