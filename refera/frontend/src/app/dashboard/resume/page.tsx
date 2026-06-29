"use client";

import { useEffect, useState, useRef } from "react";
import { Upload, FileText, Sparkles, AlertCircle, CheckCircle2 } from "lucide-react";
import { api, Resume, ResumeAnalysis, Job } from "@/lib/api";
import { scoreColor, scoreBg } from "@/lib/utils";

export default function ResumeAnalyzerPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selected, setSelected] = useState<Resume | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<number | "">("");
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api.getResumes().then((r) => {
      setResumes(r);
      if (r[0]) setSelected(r[0]);
    }).catch(() => {});
    api.getJobs().then(setJobs).catch(() => {});
  }, []);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError("");
    try {
      const resume = await api.uploadResume(file);
      setResumes((prev) => [resume, ...prev]);
      setSelected(resume);
      await api.matchJobs(resume.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!selected) return;
    setAnalyzing(true);
    setError("");
    try {
      const result = await api.analyzeResume(selected.id, {
        job_id: selectedJob ? Number(selectedJob) : undefined,
      });
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold font-display">Resume Analyzer</h1>
        <p className="text-slate-400 mt-1">Upload, parse, and optimize your resume for ATS</p>
      </div>

      {error && (
        <div className="mb-6 flex items-center gap-2 rounded-xl bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
          <AlertCircle className="h-4 w-4 shrink-0" /> {error}
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="space-y-6">
          <div
            className="glass-card border-dashed border-brand-500/30 cursor-pointer text-center py-8 hover:border-brand-500/50 transition-colors"
            onClick={() => fileRef.current?.click()}
          >
            <input ref={fileRef} type="file" accept=".pdf,.docx,.txt" className="hidden" onChange={handleUpload} />
            <Upload className="h-10 w-10 text-brand-400 mx-auto mb-3" />
            <p className="font-medium">{uploading ? "Uploading..." : "Drop resume or click to upload"}</p>
            <p className="text-xs text-slate-500 mt-1">PDF, DOCX, TXT — max 5MB</p>
          </div>

          {resumes.length > 0 && (
            <div className="glass-card">
              <h3 className="text-sm font-semibold mb-3">Your Resumes</h3>
              <div className="space-y-2">
                {resumes.map((r) => (
                  <button
                    key={r.id}
                    onClick={() => { setSelected(r); setAnalysis(null); }}
                    className={`w-full flex items-center gap-3 rounded-xl p-3 text-left transition-all ${
                      selected?.id === r.id ? "bg-brand-500/15 border border-brand-500/30" : "bg-white/5 hover:bg-white/10"
                    }`}
                  >
                    <FileText className="h-4 w-4 text-brand-400 shrink-0" />
                    <div className="min-w-0">
                      <p className="text-sm truncate">{r.file_name}</p>
                      <p className={`text-xs ${scoreColor(r.ats_score)}`}>ATS: {r.ats_score}%</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="lg:col-span-2 space-y-6">
          {selected ? (
            <>
              <div className={`glass-card bg-gradient-to-br ${scoreBg(selected.ats_score)}`}>
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <div>
                    <p className="text-xs text-slate-500 uppercase">Overall ATS Score</p>
                    <p className={`text-5xl font-bold ${scoreColor(selected.ats_score)}`}>{selected.ats_score}%</p>
                  </div>
                  <div className="flex gap-6">
                    <div className="text-center">
                      <p className="text-2xl font-bold">{selected.skills?.length || 0}</p>
                      <p className="text-xs text-slate-500">Skills</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold">{selected.experience?.length || 0}</p>
                      <p className="text-xs text-slate-500">Experience</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold">{selected.projects?.length || 0}</p>
                      <p className="text-xs text-slate-500">Projects</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="glass-card">
                <h3 className="font-semibold mb-3">Extracted Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {(selected.skills || []).map((s) => (
                    <span key={s} className="rounded-lg bg-brand-500/10 border border-brand-500/20 px-3 py-1 text-xs text-brand-300">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div className="glass-card">
                <h3 className="font-semibold mb-4 flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-brand-400" /> Compare with Job
                </h3>
                <select
                  value={selectedJob}
                  onChange={(e) => setSelectedJob(e.target.value ? Number(e.target.value) : "")}
                  className="input-field mb-4"
                >
                  <option value="">Select a job to compare</option>
                  {jobs.map((j) => (
                    <option key={j.id} value={j.id}>{j.title} @ {j.company}</option>
                  ))}
                </select>
                <button
                  onClick={handleAnalyze}
                  disabled={!selectedJob || analyzing}
                  className="btn-primary"
                >
                  {analyzing ? "Analyzing..." : "Run ATS Analysis"}
                </button>
              </div>

              {analysis && (
                <div className="glass-card space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">Analysis Results</h3>
                    <span className={`text-2xl font-bold ${scoreColor(analysis.ats_score)}`}>
                      {analysis.ats_score}%
                    </span>
                  </div>

                  <div className="grid sm:grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-emerald-400 font-medium mb-2 flex items-center gap-1">
                        <CheckCircle2 className="h-3 w-3" /> Matched Keywords
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {analysis.matched_keywords.map((k) => (
                          <span key={k} className="text-xs bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded">{k}</span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-xs text-red-400 font-medium mb-2 flex items-center gap-1">
                        <AlertCircle className="h-3 w-3" /> Missing Keywords
                      </p>
                      <div className="flex flex-wrap gap-1">
                        {analysis.missing_keywords.map((k) => (
                          <span key={k} className="text-xs bg-red-500/10 text-red-400 px-2 py-0.5 rounded">{k}</span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div>
                    <p className="text-xs text-slate-500 font-medium mb-2">Suggestions</p>
                    <ul className="space-y-1">
                      {analysis.suggestions.map((s, i) => (
                        <li key={i} className="text-sm text-slate-400 flex items-start gap-2">
                          <span className="text-brand-400 mt-0.5">•</span> {s}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {analysis.ai_feedback && (
                    <div className="rounded-xl bg-brand-500/5 border border-brand-500/20 p-4">
                      <p className="text-xs text-brand-300 font-medium mb-2">AI Feedback</p>
                      <p className="text-sm text-slate-300 leading-relaxed">{analysis.ai_feedback}</p>
                    </div>
                  )}
                </div>
              )}
            </>
          ) : (
            <div className="glass-card text-center py-16 text-slate-500">
              <FileText className="h-12 w-12 mx-auto mb-3 opacity-30" />
              <p>Upload a resume to see analysis</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
