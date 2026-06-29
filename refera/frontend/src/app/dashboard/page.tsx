"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  FileSearch, Briefcase, Send, TrendingUp, Upload, ArrowRight, Crown,
} from "lucide-react";
import { useAuth } from "@/lib/auth";
import { api, Resume, JobMatch, Referral } from "@/lib/api";
import { scoreColor } from "@/lib/utils";

export default function DashboardPage() {
  const { user } = useAuth();
  const [resume, setResume] = useState<Resume | null>(null);
  const [matches, setMatches] = useState<JobMatch[]>([]);
  const [referrals, setReferrals] = useState<Referral[]>([]);

  useEffect(() => {
    api.getResumes().then((r) => setResume(r[0] || null)).catch(() => {});
    api.getMyMatches().then(setMatches).catch(() => {});
    api.getSentReferrals().then(setReferrals).catch(() => {});
  }, []);

  const pending = referrals.filter((r) => r.status === "pending").length;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold font-display">
          Welcome back, {user?.full_name?.split(" ")[0]} 👋
        </h1>
        <p className="text-slate-400 mt-1">Here&apos;s your referral network overview</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: "ATS Score", value: resume ? `${resume.ats_score}%` : "—", icon: TrendingUp, color: "text-emerald-400" },
          { label: "Job Matches", value: matches.length, icon: Briefcase, color: "text-brand-400" },
          { label: "Referrals Sent", value: referrals.length, icon: Send, color: "text-violet-400" },
          { label: "Pending", value: pending, icon: FileSearch, color: "text-amber-400" },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="glass-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider">{label}</p>
                <p className={`text-2xl font-bold mt-1 ${color}`}>{value}</p>
              </div>
              <Icon className={`h-8 w-8 ${color} opacity-50`} />
            </div>
          </div>
        ))}
      </div>

      {!resume && (
        <div className="glass-card border-dashed border-brand-500/30 mb-8 text-center py-10">
          <Upload className="h-10 w-10 text-brand-400 mx-auto mb-3" />
          <h3 className="font-semibold mb-1">Upload your resume to get started</h3>
          <p className="text-sm text-slate-400 mb-4">We&apos;ll parse it and match you with jobs instantly</p>
          <Link href="/dashboard/resume" className="btn-primary">
            Upload Resume <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="glass-card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold">Top Job Matches</h2>
            <Link href="/dashboard/jobs" className="text-xs text-brand-400 hover:text-brand-300">View all</Link>
          </div>
          {matches.length === 0 ? (
            <p className="text-sm text-slate-500">Upload a resume to see matches</p>
          ) : (
            <div className="space-y-3">
              {matches.slice(0, 4).map((m) => (
                <div key={m.id} className="flex items-center justify-between rounded-xl bg-white/5 p-3">
                  <div>
                    <p className="text-sm font-medium">{m.job.title}</p>
                    <p className="text-xs text-slate-500">{m.job.company}</p>
                  </div>
                  <span className={`text-sm font-bold ${scoreColor(m.eligibility_score)}`}>
                    {m.eligibility_score}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="glass-card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold">Recent Referrals</h2>
            <Link href="/dashboard/referrals" className="text-xs text-brand-400 hover:text-brand-300">View all</Link>
          </div>
          {referrals.length === 0 ? (
            <p className="text-sm text-slate-500">No referrals yet. Request one from a matched job!</p>
          ) : (
            <div className="space-y-3">
              {referrals.slice(0, 4).map((r) => (
                <div key={r.id} className="flex items-center justify-between rounded-xl bg-white/5 p-3">
                  <div>
                    <p className="text-sm font-medium">{r.job.title}</p>
                    <p className="text-xs text-slate-500">{r.employee.full_name} @ {r.job.company}</p>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full capitalize ${
                    r.status === "accepted" ? "bg-emerald-500/20 text-emerald-400" :
                    r.status === "rejected" ? "bg-red-500/20 text-red-400" :
                    "bg-amber-500/20 text-amber-400"
                  }`}>
                    {r.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {user?.subscription_plan === "free" && (
        <div className="mt-8 glass-card border-brand-500/20 bg-gradient-to-r from-brand-600/10 to-violet-600/10 flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <Crown className="h-8 w-8 text-amber-400" />
            <div>
              <p className="font-semibold">Upgrade to Premium</p>
              <p className="text-sm text-slate-400">Unlock 25 referrals/month and advanced AI features</p>
            </div>
          </div>
          <Link href="/pricing" className="btn-primary text-sm py-2.5">Upgrade — ₹999/mo</Link>
        </div>
      )}
    </div>
  );
}
