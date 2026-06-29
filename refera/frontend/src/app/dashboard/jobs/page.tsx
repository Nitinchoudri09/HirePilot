"use client";

import { useEffect, useState } from "react";
import { MapPin, Briefcase, MessageCircle, Send, Sparkles } from "lucide-react";
import { api, JobMatch } from "@/lib/api";
import { scoreColor, scoreBg } from "@/lib/utils";

export default function JobMatchesPage() {
  const [matches, setMatches] = useState<JobMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [chatJob, setChatJob] = useState<number | null>(null);
  const [chatResponse, setChatResponse] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [questions, setQuestions] = useState<string[]>([]);

  useEffect(() => {
    api.getMyMatches()
      .then(setMatches)
      .catch(() => api.matchJobs().then(setMatches).catch(() => {}))
      .finally(() => setLoading(false));
  }, []);

  const askEligibility = async (jobId: number) => {
    setChatJob(jobId);
    setChatLoading(true);
    setChatResponse("");
    try {
      const res = await api.checkEligibility({ job_id: jobId });
      setChatResponse(res.response);
    } catch {
      setChatResponse("Unable to check eligibility. Upload a resume first.");
    } finally {
      setChatLoading(false);
    }
  };

  const getQuestions = async (jobId: number) => {
    try {
      const res = await api.generateInterviewQuestions({ job_id: jobId, count: 5 });
      setQuestions(res.questions);
    } catch {
      setQuestions(["Tell me about your experience with the required tech stack."]);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold font-display">Job Matches</h1>
        <p className="text-slate-400 mt-1">AI-matched roles based on your resume skills</p>
      </div>

      {matches.length === 0 ? (
        <div className="glass-card text-center py-16">
          <Briefcase className="h-12 w-12 mx-auto mb-3 text-slate-600" />
          <p className="text-slate-400">No matches yet. Upload your resume first.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {matches.map((m) => (
            <div key={m.id} className="glass-card">
              <div className="flex flex-col lg:flex-row lg:items-start gap-4">
                <div className="flex-1">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="text-lg font-semibold">{m.job.title}</h3>
                      <p className="text-brand-400 text-sm">{m.job.company}</p>
                    </div>
                    <div className={`shrink-0 rounded-xl px-4 py-2 text-center bg-gradient-to-br ${scoreBg(m.eligibility_score)} border`}>
                      <p className={`text-2xl font-bold ${scoreColor(m.eligibility_score)}`}>{m.eligibility_score}%</p>
                      <p className="text-xs text-slate-500">Match</p>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-3 mt-3 text-xs text-slate-500">
                    {m.job.location && (
                      <span className="flex items-center gap-1"><MapPin className="h-3 w-3" /> {m.job.location}</span>
                    )}
                    <span className="flex items-center gap-1"><Briefcase className="h-3 w-3" /> {m.job.experience_years}+ yrs</span>
                    {m.job.salary_range && <span>{m.job.salary_range}</span>}
                  </div>

                  <p className="text-sm text-slate-400 mt-3 line-clamp-2">{m.job.description}</p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {m.matched_skills.map((s) => (
                      <span key={s} className="text-xs bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded">{s}</span>
                    ))}
                    {m.missing_skills.slice(0, 3).map((s) => (
                      <span key={s} className="text-xs bg-red-500/10 text-red-400 px-2 py-0.5 rounded">{s}</span>
                    ))}
                  </div>
                </div>

                <div className="flex flex-col gap-2 shrink-0">
                  <button onClick={() => askEligibility(m.job.id)} className="btn-secondary text-xs py-2 px-4">
                    <MessageCircle className="h-3.5 w-3.5" /> Am I eligible?
                  </button>
                  <button onClick={() => getQuestions(m.job.id)} className="btn-secondary text-xs py-2 px-4">
                    <Sparkles className="h-3.5 w-3.5" /> Interview Qs
                  </button>
                  <a href={`/dashboard/referrals?job=${m.job.id}`} className="btn-primary text-xs py-2 px-4 text-center">
                    <Send className="h-3.5 w-3.5" /> Request Referral
                  </a>
                </div>
              </div>

              {chatJob === m.job.id && chatResponse && (
                <div className="mt-4 rounded-xl bg-brand-500/5 border border-brand-500/20 p-4">
                  <p className="text-xs text-brand-300 font-medium mb-2">AI Eligibility Check</p>
                  <p className="text-sm text-slate-300 whitespace-pre-line">{chatResponse}</p>
                </div>
              )}

              {chatJob === m.job.id && chatLoading && (
                <p className="mt-4 text-sm text-slate-500 animate-pulse">Checking eligibility...</p>
              )}
            </div>
          ))}
        </div>
      )}

      {questions.length > 0 && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" onClick={() => setQuestions([])}>
          <div className="glass max-w-lg w-full rounded-2xl p-6" onClick={(e) => e.stopPropagation()}>
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-brand-400" /> AI Interview Questions
            </h3>
            <ol className="space-y-3">
              {questions.map((q, i) => (
                <li key={i} className="text-sm text-slate-300 flex gap-2">
                  <span className="text-brand-400 font-bold shrink-0">{i + 1}.</span> {q}
                </li>
              ))}
            </ol>
            <button onClick={() => setQuestions([])} className="btn-secondary w-full mt-6">Close</button>
          </div>
        </div>
      )}
    </div>
  );
}
