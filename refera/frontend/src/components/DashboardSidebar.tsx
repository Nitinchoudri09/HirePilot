"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, FileSearch, Briefcase, Send, User, Shield,
  LogOut, Sparkles, Crown, X,
} from "lucide-react";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";

const links = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/resume", label: "Resume Analyzer", icon: FileSearch },
  { href: "/dashboard/jobs", label: "Job Matches", icon: Briefcase },
  { href: "/dashboard/referrals", label: "Referrals", icon: Send },
  { href: "/dashboard/profile", label: "Profile", icon: User },
];

export default function DashboardSidebar({ onClose }: { onClose?: () => void }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-white/5 bg-[#030712]/95 backdrop-blur-xl">
      <div className="flex items-center gap-2 border-b border-white/5 px-4 py-5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-violet-600">
          <Sparkles className="h-4 w-4 text-white" />
        </div>
        <span className="flex-1 font-display text-lg font-bold">Refera</span>
        {onClose && (
          <button
            onClick={onClose}
            className="md:hidden rounded-lg p-1.5 text-slate-400 hover:bg-white/5 hover:text-white transition-colors"
            aria-label="Close sidebar"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {links.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            onClick={onClose}
            className={cn(
              "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
              pathname === href
                ? "bg-brand-500/15 text-brand-300 border border-brand-500/20"
                : "text-slate-400 hover:bg-white/5 hover:text-white"
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        ))}
        {user?.role === "admin" && (
          <Link
            href="/dashboard/admin"
            onClick={onClose}
            className={cn(
              "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
              pathname === "/dashboard/admin"
                ? "bg-brand-500/15 text-brand-300 border border-brand-500/20"
                : "text-slate-400 hover:bg-white/5 hover:text-white"
            )}
          >
            <Shield className="h-4 w-4" />
            Admin
          </Link>
        )}
      </nav>

      <div className="border-t border-white/5 p-4">
        <div className="glass rounded-xl p-3 mb-3">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-brand-500 to-violet-600 text-xs font-bold">
              {user?.full_name?.charAt(0) || "U"}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.full_name}</p>
              <p className="text-xs text-slate-500 truncate flex items-center gap-1">
                {user?.subscription_plan === "premium" && <Crown className="h-3 w-3 text-amber-400" />}
                {user?.subscription_plan || "free"} plan
              </p>
            </div>
          </div>
          <p className="mt-2 text-xs text-slate-500">
            Referrals: {user?.referrals_used}/{user?.referral_limit}
          </p>
        </div>
        <button
          onClick={logout}
          className="flex w-full items-center gap-2 rounded-xl px-3 py-2 text-sm text-slate-400 hover:bg-white/5 hover:text-white transition-all"
        >
          <LogOut className="h-4 w-4" />
          Log out
        </button>
      </div>
    </aside>
  );
}
