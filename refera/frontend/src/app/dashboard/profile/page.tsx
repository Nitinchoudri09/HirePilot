"use client";

import { useState } from "react";
import { Save, Crown } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { api } from "@/lib/api";
import Link from "next/link";

export default function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const [form, setForm] = useState({
    full_name: user?.full_name || "",
    company: user?.company || "",
    job_title: user?.job_title || "",
    bio: user?.bio || "",
    location: user?.location || "",
    linkedin_url: user?.linkedin_url || "",
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.updateProfile(form);
      await refreshUser();
      setMessage("Profile updated successfully!");
    } catch {
      setMessage("Failed to update profile");
    } finally {
      setSaving(false);
    }
  };

  const handleUpgrade = async () => {
    try {
      const order = await api.createOrder("premium");
      if (order.demo_mode) {
        await api.verifyPayment({
          razorpay_order_id: order.order_id as string,
          razorpay_payment_id: "demo_payment_" + Date.now(),
          razorpay_signature: "demo_sig",
        });
        await refreshUser();
        setMessage("Premium activated! (Demo mode)");
      }
    } catch {
      setMessage("Payment failed");
    }
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold font-display">Profile</h1>
        <p className="text-slate-400 mt-1">Manage your account settings</p>
      </div>

      <div className="glass-card mb-6 flex items-center gap-4">
        <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-brand-500 to-violet-600 flex items-center justify-center text-2xl font-bold">
          {user?.full_name?.charAt(0) || "U"}
        </div>
        <div>
          <p className="font-semibold text-lg">{user?.full_name}</p>
          <p className="text-sm text-slate-400">{user?.email}</p>
          <p className="text-xs text-slate-500 mt-1 capitalize flex items-center gap-1">
            {user?.subscription_plan === "premium" && <Crown className="h-3 w-3 text-amber-400" />}
            {user?.role} · {user?.subscription_plan} plan
          </p>
        </div>
      </div>

      {message && (
        <div className="mb-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 px-4 py-3 text-sm text-emerald-400">
          {message}
        </div>
      )}

      <form onSubmit={handleSave} className="glass-card space-y-4">
        {[
          { key: "full_name", label: "Full Name" },
          { key: "company", label: "Company" },
          { key: "job_title", label: "Job Title" },
          { key: "location", label: "Location" },
          { key: "linkedin_url", label: "LinkedIn URL" },
        ].map(({ key, label }) => (
          <div key={key}>
            <label className="text-sm text-slate-400 mb-1 block">{label}</label>
            <input
              type="text"
              value={form[key as keyof typeof form]}
              onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              className="input-field"
            />
          </div>
        ))}
        <div>
          <label className="text-sm text-slate-400 mb-1 block">Bio</label>
          <textarea
            value={form.bio}
            onChange={(e) => setForm({ ...form, bio: e.target.value })}
            className="input-field min-h-[100px]"
          />
        </div>
        <button type="submit" disabled={saving} className="btn-primary">
          <Save className="h-4 w-4" /> {saving ? "Saving..." : "Save Changes"}
        </button>
      </form>

      <div className="glass-card mt-6">
        <h3 className="font-semibold mb-2">Referral Usage</h3>
        <div className="flex items-center gap-4">
          <div className="flex-1 h-3 rounded-full bg-white/5 overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-brand-500 to-violet-500"
              style={{ width: `${((user?.referrals_used || 0) / (user?.referral_limit || 1)) * 100}%` }}
            />
          </div>
          <span className="text-sm text-slate-400">
            {user?.referrals_used}/{user?.referral_limit}
          </span>
        </div>
      </div>

      {user?.subscription_plan === "free" && (
        <div className="glass-card mt-6 border-brand-500/20">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <p className="font-semibold flex items-center gap-2">
                <Crown className="h-4 w-4 text-amber-400" /> Upgrade to Premium
              </p>
              <p className="text-sm text-slate-400 mt-1">₹999/month — 25 referrals + advanced AI</p>
            </div>
            <div className="flex gap-2">
              <button onClick={handleUpgrade} className="btn-primary text-sm">Demo Upgrade</button>
              <Link href="/pricing" className="btn-secondary text-sm">View Plans</Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
