"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Send, Sparkles, User, Building2, Clock } from "lucide-react";
import { api, Referral, User as UserType, Job } from "@/lib/api";
import { formatDate } from "@/lib/utils";

function ReferralsContent() {
  const searchParams = useSearchParams();
  const preselectedJob = searchParams.get("job");

  const [sent, setSent] = useState<Referral[]>([]);
  const [employees, setEmployees] = useState<UserType[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [showForm, setShowForm] = useState(!!preselectedJob);
  const [form, setForm] = useState({ employee_id: "", job_id: preselectedJob || "", message: "" });
  const [aiMessage, setAiMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [tab, setTab] = useState<"sent" | "received">("sent");

  useEffect(() => {
    api.getSentReferrals().then(setSent).catch(() => {});
    api.getEmployees().then(setEmployees).catch(() => {});
    api.getJobs().then(setJobs).catch(() => {});
  }, []);

  const generateMessage = async () => {
    if (!form.job_id) return;
    try {
      const res = await api.generateReferralMessage({ job_id: Number(form.job_id) });
      setAiMessage(res.message);
      setForm((f) => ({ ...f, message: res.message }));
    } catch {
      setAiMessage("Failed to generate message");
    }
  };

  const submitReferral = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const ref = await api.createReferral({
        employee_id: Number(form.employee_id),
        job_id: Number(form.job_id),
        message: form.message,
      });
      setSent((prev) => [ref, ...prev]);
      setShowForm(false);
      setForm({ employee_id: "", job_id: "", message: "" });
      setAiMessage("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create referral");
    } finally {
      setLoading(false);
    }
  };

  const statusStyle = (s: string) =>
    s === "accepted" ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" :
    s === "rejected" ? "bg-red-500/20 text-red-400 border-red-500/30" :
    "bg-amber-500/20 text-amber-400 border-amber-500/30";

  return (
    <div>
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold font-display">Referral Requests</h1>
          <p className="text-slate-400 mt-1">Request and track warm referrals</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary">
          <Send className="h-4 w-4" /> New Referral
        </button>
      </div>

      {showForm && (
        <div className="glass-card mb-8">
          <h3 className="font-semibold mb-4">Request a Referral</h3>
          {error && <p className="text-sm text-red-400 mb-4">{error}</p>}
          <form onSubmit={submitReferral} className="space-y-4 max-w-xl">
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Select Employee</label>
              <select
                value={form.employee_id}
                onChange={(e) => setForm({ ...form, employee_id: e.target.value })}
                className="input-field"
                required
              >
                <option value="">Choose a referrer...</option>
                {employees.map((e) => (
                  <option key={e.id} value={e.id}>{e.full_name} — {e.company} ({e.job_title})</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Select Job</label>
              <select
                value={form.job_id}
                onChange={(e) => setForm({ ...form, job_id: e.target.value })}
                className="input-field"
                required
              >
                <option value="">Choose a job...</option>
                {jobs.map((j) => (
                  <option key={j.id} value={j.id}>{j.title} @ {j.company}</option>
                ))}
              </select>
            </div>
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-sm text-slate-400">Message</label>
                <button type="button" onClick={generateMessage} className="text-xs text-brand-400 flex items-center gap-1 hover:text-brand-300">
                  <Sparkles className="h-3 w-3" /> AI Generate
                </button>
              </div>
              <textarea
                value={form.message}
                onChange={(e) => setForm({ ...form, message: e.target.value })}
                className="input-field min-h-[120px] resize-y"
                placeholder="Your referral request message..."
              />
            </div>
            {aiMessage && (
              <div className="rounded-xl bg-brand-500/5 border border-brand-500/20 p-3 text-sm text-slate-400">
                <p className="text-xs text-brand-300 mb-1">AI Generated Preview</p>
                {aiMessage}
              </div>
            )}
            <div className="flex gap-3">
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? "Sending..." : "Send Request"}
              </button>
              <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      <div className="flex gap-2 mb-6">
        {(["sent", "received"] as const).map((t) => (
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

      <ReferralList tab={tab} sent={sent} statusStyle={statusStyle} />
    </div>
  );
}

function ReferralList({
  tab, sent, statusStyle,
}: {
  tab: "sent" | "received";
  sent: Referral[];
  statusStyle: (s: string) => string;
}) {
  const [received, setReceived] = useState<Referral[]>([]);

  useEffect(() => {
    if (tab === "received") {
      api.getReceivedReferrals().then(setReceived).catch(() => {});
    }
  }, [tab]);

  const list = tab === "sent" ? sent : received;

  if (list.length === 0) {
    return (
      <div className="glass-card text-center py-16 text-slate-500">
        <Send className="h-12 w-12 mx-auto mb-3 opacity-30" />
        <p>No {tab} referrals yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {list.map((r) => (
        <div key={r.id} className="glass-card">
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <h3 className="font-semibold">{r.job.title}</h3>
              <p className="text-sm text-brand-400 flex items-center gap-1 mt-0.5">
                <Building2 className="h-3.5 w-3.5" /> {r.job.company}
              </p>
              <p className="text-xs text-slate-500 mt-2 flex items-center gap-3">
                <span className="flex items-center gap-1">
                  <User className="h-3 w-3" />
                  {tab === "sent" ? r.employee.full_name : r.candidate.full_name}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="h-3 w-3" /> {formatDate(r.created_at)}
                </span>
              </p>
            </div>
            <span className={`text-xs px-3 py-1 rounded-full border capitalize ${statusStyle(r.status)}`}>
              {r.status}
            </span>
          </div>
          {r.ai_generated_message && (
            <div className="mt-4 rounded-xl bg-white/5 p-3 text-sm text-slate-400">
              <p className="text-xs text-slate-500 mb-1">Referral Message</p>
              {r.message || r.ai_generated_message}
            </div>
          )}
          {r.notes && (
            <p className="mt-2 text-xs text-slate-500">Note: {r.notes}</p>
          )}
        </div>
      ))}
    </div>
  );
}

export default function ReferralsPage() {
  return (
    <Suspense fallback={<div className="animate-pulse text-slate-500">Loading...</div>}>
      <ReferralsContent />
    </Suspense>
  );
}
