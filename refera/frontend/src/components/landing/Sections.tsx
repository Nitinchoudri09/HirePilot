"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  ArrowRight, Zap, Users, Target, Brain, Shield, TrendingUp,
} from "lucide-react";

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center overflow-hidden pt-20">
      <div className="absolute inset-0 bg-hero-gradient" />
      <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-40" />
      <div className="absolute top-1/4 -left-32 h-96 w-96 rounded-full bg-brand-600/20 blur-3xl animate-float" />
      <div className="absolute bottom-1/4 -right-32 h-96 w-96 rounded-full bg-violet-600/20 blur-3xl animate-float" style={{ animationDelay: "3s" }} />

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-500/10 px-4 py-1.5 text-xs font-medium text-brand-300 mb-6">
              <Zap className="h-3.5 w-3.5" />
              AI-Powered Job Referral Network
            </div>
            <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight tracking-tight">
              Get referred to your{" "}
              <span className="gradient-text">dream job</span>{" "}
              with AI
            </h1>
            <p className="mt-6 text-lg text-slate-400 leading-relaxed max-w-xl">
              Refera connects talented candidates with employees at top companies.
              Upload your resume, get matched to jobs, and request warm referrals — all powered by AI.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link href="/signup" className="btn-primary">
                Start Free <ArrowRight className="h-4 w-4" />
              </Link>
              <Link href="/#how-it-works" className="btn-secondary">
                See How It Works
              </Link>
            </div>
            <div className="mt-10 flex flex-wrap gap-8">
              {[
                { value: "2,500+", label: "Referrals sent" },
                { value: "89%", label: "Match accuracy" },
                { value: "150+", label: "Partner companies" },
              ].map((stat) => (
                <div key={stat.label}>
                  <p className="text-2xl font-bold gradient-text">{stat.value}</p>
                  <p className="text-sm text-slate-500">{stat.label}</p>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="relative"
          >
            <div className="glass rounded-3xl p-6 shadow-2xl shadow-brand-500/10">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wider">ATS Score</p>
                  <p className="text-3xl font-bold text-emerald-400">87%</p>
                </div>
                <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 flex items-center justify-center border border-emerald-500/30">
                  <TrendingUp className="h-8 w-8 text-emerald-400" />
                </div>
              </div>
              <div className="space-y-3">
                {[
                  { skill: "React", match: 95 },
                  { skill: "TypeScript", match: 88 },
                  { skill: "System Design", match: 72 },
                ].map((item) => (
                  <div key={item.skill}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-300">{item.skill}</span>
                      <span className="text-brand-400">{item.match}%</span>
                    </div>
                    <div className="h-2 rounded-full bg-white/5 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-brand-500 to-violet-500 transition-all"
                        style={{ width: `${item.match}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 glass rounded-xl p-4 border border-brand-500/20">
                <p className="text-xs text-brand-300 font-medium mb-1">AI Referral Message</p>
                <p className="text-sm text-slate-400 leading-relaxed">
                  &ldquo;I&apos;d like to refer Jordan for the Senior Full Stack role — strong React &amp; TypeScript background...&rdquo;
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}

export function ProblemSection() {
  return (
    <section className="section-padding bg-[#020617]">
      <div className="mx-auto max-w-7xl">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="font-display text-3xl sm:text-4xl font-bold">
            The referral gap is <span className="gradient-text">real</span>
          </h2>
          <p className="mt-4 text-slate-400">
            70% of jobs are filled through referrals, yet most candidates never get a warm introduction.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { icon: Target, title: "Cold applications fail", desc: "ATS systems reject 75% of resumes before a human sees them." },
            { icon: Users, title: "No insider access", desc: "Candidates lack connections at target companies for referrals." },
            { icon: Brain, title: "Generic outreach", desc: "Writing referral requests is awkward and time-consuming." },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="glass-card group">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-red-500/10 border border-red-500/20 mb-4 group-hover:scale-110 transition-transform">
                <Icon className="h-6 w-6 text-red-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function HowItWorks() {
  const steps = [
    { step: "01", title: "Upload Resume", desc: "Parse PDF/DOCX and extract skills, experience, and projects instantly." },
    { step: "02", title: "Get Matched", desc: "AI compares your profile against open roles and scores eligibility." },
    { step: "03", title: "Request Referral", desc: "Connect with employees and send AI-crafted referral messages." },
    { step: "04", title: "Track & Interview", desc: "Monitor referral status and prep with AI-generated interview questions." },
  ];

  return (
    <section id="how-it-works" className="section-padding">
      <div className="mx-auto max-w-7xl">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="font-display text-3xl sm:text-4xl font-bold">
            How <span className="gradient-text">Refera</span> works
          </h2>
          <p className="mt-4 text-slate-400">Four steps from resume upload to referral acceptance.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((item, i) => (
            <motion.div
              key={item.step}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass-card relative"
            >
              <span className="text-4xl font-bold gradient-text opacity-50">{item.step}</span>
              <h3 className="text-lg font-semibold mt-2 mb-2">{item.title}</h3>
              <p className="text-sm text-slate-400">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Features() {
  const features = [
    { icon: Brain, title: "AI Resume Analyzer", desc: "ATS scoring, keyword analysis, and personalized improvement tips." },
    { icon: Target, title: "Smart Job Matching", desc: "Eligibility scores based on skills, experience, and job requirements." },
    { icon: Users, title: "Referral Network", desc: "Connect with employees at Google, Microsoft, Amazon, and more." },
    { icon: Zap, title: "AI Message Generator", desc: "Professional referral messages crafted in seconds." },
    { icon: Shield, title: "Secure Storage", desc: "Resumes stored securely with enterprise-grade encryption." },
    { icon: TrendingUp, title: "Analytics Dashboard", desc: "Track referrals, matches, and application progress in one place." },
  ];

  return (
    <section id="features" className="section-padding bg-[#020617]">
      <div className="mx-auto max-w-7xl">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="font-display text-3xl sm:text-4xl font-bold">
            Everything you need to <span className="gradient-text">get hired</span>
          </h2>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="glass-card group hover:shadow-lg hover:shadow-brand-500/5">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-500/10 border border-brand-500/20 mb-4 group-hover:bg-brand-500/20 transition-colors">
                <Icon className="h-5 w-5 text-brand-400" />
              </div>
              <h3 className="font-semibold mb-2">{title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Testimonials() {
  const items = [
    { name: "Jordan Lee", role: "Software Engineer @ TechCorp", quote: "Got referred to Google through Refera. The AI message generator saved me hours of awkward networking.", avatar: "JL" },
    { name: "Emma Wilson", role: "Full Stack Developer", quote: "The ATS analyzer helped me improve my resume from 62% to 89%. Landed 3 interviews in 2 weeks.", avatar: "EW" },
    { name: "Sarah Chen", role: "Employee @ Google", quote: "As a referrer, I love how Refera pre-screens candidates. Every referral I receive is actually qualified.", avatar: "SC" },
  ];

  return (
    <section className="section-padding">
      <div className="mx-auto max-w-7xl">
        <div className="text-center mb-16">
          <h2 className="font-display text-3xl sm:text-4xl font-bold">
            Loved by <span className="gradient-text">candidates & referrers</span>
          </h2>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {items.map((t) => (
            <div key={t.name} className="glass-card">
              <p className="text-slate-300 text-sm leading-relaxed mb-6">&ldquo;{t.quote}&rdquo;</p>
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-brand-500 to-violet-600 flex items-center justify-center text-xs font-bold">
                  {t.avatar}
                </div>
                <div>
                  <p className="text-sm font-medium">{t.name}</p>
                  <p className="text-xs text-slate-500">{t.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function FAQ() {
  const faqs = [
    { q: "How does the ATS score work?", a: "We parse your resume and compare it against job descriptions, checking keyword density, formatting, section completeness, and skill alignment." },
    { q: "Is my resume data secure?", a: "Yes. Resumes are encrypted at rest and stored on secure cloud infrastructure (AWS S3 or local storage in dev)." },
    { q: "How many referrals can I request?", a: "Free plan includes 3 referrals/month. Premium unlocks 25 referrals plus advanced AI features." },
    { q: "Can employees join as referrers?", a: "Absolutely. Sign up as an employee to receive and manage referral requests from qualified candidates." },
  ];

  return (
    <section id="faq" className="section-padding bg-[#020617]">
      <div className="mx-auto max-w-3xl">
        <div className="text-center mb-12">
          <h2 className="font-display text-3xl sm:text-4xl font-bold">
            Frequently asked <span className="gradient-text">questions</span>
          </h2>
        </div>
        <div className="space-y-4">
          {faqs.map((faq) => (
            <details key={faq.q} className="glass-card group cursor-pointer">
              <summary className="font-medium text-white list-none flex justify-between items-center">
                {faq.q}
                <span className="text-brand-400 group-open:rotate-45 transition-transform text-xl">+</span>
              </summary>
              <p className="mt-3 text-sm text-slate-400 leading-relaxed">{faq.a}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}

export function CTA() {
  return (
    <section className="section-padding">
      <div className="mx-auto max-w-4xl">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-brand-600/20 via-violet-600/20 to-brand-600/20 border border-brand-500/20 p-12 text-center">
          <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-20" />
          <div className="relative">
            <h2 className="font-display text-3xl sm:text-4xl font-bold mb-4">
              Ready to get referred?
            </h2>
            <p className="text-slate-400 mb-8 max-w-lg mx-auto">
              Join thousands of candidates using AI to land jobs at top companies through warm referrals.
            </p>
            <Link href="/signup" className="btn-primary">
              Create Free Account <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
