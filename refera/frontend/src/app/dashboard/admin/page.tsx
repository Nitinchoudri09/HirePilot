"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Users, Briefcase, Send, Crown, FileText, Clock,
} from "lucide-react";
import { useAuth } from "@/lib/auth";
import { api, AdminStats, User, Job, Referral } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function AdminDashboardPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [referrals, setReferrals] = useState<Referral[]>([]);
  const [tab, setTab] = useState<"overview" | "users" | "jobs" | "referrals">("overview");

  useEffect(() => {
    if (user && user.role !== "admin") {
      router.push("/dashboard");
      return;
    }
    api.getAdminStats().then(setStats).catch(() => {});
    api.getAdminUsers().then(setUsers).catch(() => {});
    api.getAdminJobs().then(setJobs).catch(() => {});
    api.getAdminReferrals().then(setReferrals).catch(() => {});
  }, [user, router]);

  if (user?.role !== "admin") return null;

  const statCards = stats ? [
    { label: "Total Users", value: stats.total_users, icon: Users, color: "text-brand-400" },
    { label: "Active Jobs", value: stats.total_jobs, icon: Briefcase, color: "text-violet-400" },
    { label: "Referrals", value: stats.total_referrals, icon: Send, color: "text-emerald-400" },
    { label: "Pending", value: stats.pending_referrals, icon: Clock, color: "text-amber-400" },
    { label: "Premium Users", value: stats.premium_users, icon: Crown, color: "text-amber-400" },
    { label: "Resumes", value: stats.resumes_uploaded, icon: FileText, color: "text-blue-400" },
  ] : [];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold font-display">Admin Dashboard</h1>
        <p className="text-slate-400 mt-1">Manage users, jobs, and referrals</p>
      </div>

      <div className="flex gap-2 mb-6 flex-wrap">
        {(["overview", "users", "jobs", "referrals"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-xl text-sm font-medium capitalize transition-all ${
              tab === t ? "bg-brand-500/15 text-brand-300 border border-brand-500/30" : "text-slate-400 hover:bg-white/5"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "overview" && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {statCards.map(({ label, value, icon: Icon, color }) => (
            <div key={label} className="glass-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500 uppercase">{label}</p>
                  <p className={`text-3xl font-bold mt-1 ${color}`}>{value}</p>
                </div>
                <Icon className={`h-8 w-8 ${color} opacity-40`} />
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === "users" && (
        <div className="glass-card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 border-b border-white/5">
                <th className="pb-3 pr-4">Name</th>
                <th className="pb-3 pr-4">Email</th>
                <th className="pb-3 pr-4">Role</th>
                <th className="pb-3 pr-4">Plan</th>
                <th className="pb-3">Joined</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b border-white/5">
                  <td className="py-3 pr-4 font-medium">{u.full_name}</td>
                  <td className="py-3 pr-4 text-slate-400">{u.email}</td>
                  <td className="py-3 pr-4 capitalize">{u.role}</td>
                  <td className="py-3 pr-4 capitalize">{u.subscription_plan}</td>
                  <td className="py-3 text-slate-500">{formatDate(u.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "jobs" && (
        <div className="space-y-3">
          {jobs.map((j) => (
            <div key={j.id} className="glass-card flex items-center justify-between flex-wrap gap-3">
              <div>
                <p className="font-medium">{j.title}</p>
                <p className="text-sm text-slate-400">{j.company} · {j.location}</p>
              </div>
              <span className={`text-xs px-2 py-1 rounded-full ${j.is_active ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400"}`}>
                {j.is_active ? "Active" : "Inactive"}
              </span>
            </div>
          ))}
        </div>
      )}

      {tab === "referrals" && (
        <div className="space-y-3">
          {referrals.map((r) => (
            <div key={r.id} className="glass-card">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div>
                  <p className="font-medium">{r.job.title} @ {r.job.company}</p>
                  <p className="text-xs text-slate-500">
                    {r.candidate.full_name} → {r.employee.full_name}
                  </p>
                </div>
                <span className="text-xs capitalize px-2 py-1 rounded-full bg-white/5">{r.status}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
