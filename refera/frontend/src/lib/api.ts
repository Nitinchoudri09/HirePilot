const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  avatar_url?: string;
  company?: string;
  job_title?: string;
  bio?: string;
  location?: string;
  linkedin_url?: string;
  subscription_plan: string;
  referral_limit: number;
  referrals_used: number;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  description: string;
  skills_required: string[];
  location?: string;
  experience_years: number;
  salary_range?: string;
  job_type: string;
  is_active: boolean;
  created_at: string;
}

export interface Resume {
  id: number;
  file_name: string;
  file_url?: string;
  skills: string[];
  education: Record<string, string>[];
  experience: Record<string, string>[];
  projects: Record<string, string>[];
  ats_score: number;
  parsed_at?: string;
  created_at: string;
}

export interface JobMatch {
  id: number;
  eligibility_score: number;
  matched_skills: string[];
  missing_skills: string[];
  job: Job;
  created_at: string;
}

export interface Referral {
  id: number;
  status: string;
  message?: string;
  ai_generated_message?: string;
  notes?: string;
  candidate: User;
  employee: User;
  job: Job;
  created_at: string;
  updated_at: string;
}

export interface ResumeAnalysis {
  id: number;
  ats_score: number;
  missing_keywords: string[];
  matched_keywords: string[];
  suggestions: string[];
  ai_feedback?: string;
  job_id?: number;
  created_at: string;
}

export interface AdminStats {
  total_users: number;
  total_jobs: number;
  total_referrals: number;
  pending_referrals: number;
  premium_users: number;
  resumes_uploaded: number;
}

class ApiClient {
  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("refera_token");
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string>),
    };

    if (token) headers["Authorization"] = `Bearer ${token}`;
    if (!(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    const res = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    return res.json();
  }

  // Auth
  register(data: { email: string; password: string; full_name: string; role?: string }) {
    return this.request<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  login(data: { email: string; password: string }) {
    return this.request<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  googleAuth(idToken: string) {
    return this.request<AuthResponse>("/auth/google", {
      method: "POST",
      body: JSON.stringify({ id_token: idToken }),
    });
  }

  getMe() {
    return this.request<User>("/auth/me");
  }

  // Profile
  updateProfile(data: Partial<User>) {
    return this.request<User>("/users/profile", {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  getEmployees() {
    return this.request<User[]>("/users/employees");
  }

  // Resumes
  uploadResume(file: File) {
    const form = new FormData();
    form.append("file", file);
    return this.request<Resume>("/resumes/upload", { method: "POST", body: form });
  }

  getResumes() {
    return this.request<Resume[]>("/resumes/");
  }

  analyzeResume(resumeId: number, data: { job_id?: number; job_description?: string }) {
    return this.request<ResumeAnalysis>(`/resumes/${resumeId}/analyze`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  getAnalyses(resumeId: number) {
    return this.request<ResumeAnalysis[]>(`/resumes/${resumeId}/analyses`);
  }

  // Jobs
  getJobs() {
    return this.request<Job[]>("/jobs/");
  }

  matchJobs(resumeId?: number) {
    const q = resumeId ? `?resume_id=${resumeId}` : "";
    return this.request<JobMatch[]>(`/jobs/match${q}`, { method: "POST" });
  }

  getMyMatches() {
    return this.request<JobMatch[]>("/jobs/matches/me");
  }

  // Referrals
  createReferral(data: { employee_id: number; job_id: number; resume_id?: number; message?: string }) {
    return this.request<Referral>("/referrals/", { method: "POST", body: JSON.stringify(data) });
  }

  getSentReferrals() {
    return this.request<Referral[]>("/referrals/sent");
  }

  getReceivedReferrals() {
    return this.request<Referral[]>("/referrals/received");
  }

  updateReferral(id: number, data: { status: string; notes?: string }) {
    return this.request<Referral>(`/referrals/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  // AI
  generateReferralMessage(data: { job_id: number; resume_id?: number; tone?: string }) {
    return this.request<{ message: string }>("/ai/referral-message", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  generateInterviewQuestions(data: { job_id: number; count?: number }) {
    return this.request<{ questions: string[] }>("/ai/interview-questions", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  checkEligibility(data: { job_id: number; resume_id?: number }) {
    return this.request<{
      response: string;
      eligibility_score?: number;
      matched_skills: string[];
      missing_skills: string[];
    }>("/ai/eligibility", { method: "POST", body: JSON.stringify(data) });
  }

  // Payments
  getPlans() {
    return this.request<{ plans: Record<string, unknown>[] }>("/payments/plans");
  }

  createOrder(plan: string) {
    return this.request<Record<string, unknown>>("/payments/create-order", {
      method: "POST",
      body: JSON.stringify({ plan }),
    });
  }

  verifyPayment(data: Record<string, string>) {
    return this.request<{ status: string; plan: string }>("/payments/verify", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // Admin
  getAdminStats() {
    return this.request<AdminStats>("/admin/stats");
  }

  getAdminUsers() {
    return this.request<User[]>("/admin/users");
  }

  getAdminJobs() {
    return this.request<Job[]>("/admin/jobs");
  }

  getAdminReferrals() {
    return this.request<Referral[]>("/admin/referrals");
  }

  toggleUser(userId: number) {
    return this.request<{ id: number; is_active: boolean }>(`/admin/users/${userId}/toggle`, {
      method: "PATCH",
    });
  }

  deleteJob(jobId: number) {
    return this.request<{ status: string }>(`/admin/jobs/${jobId}`, { method: "DELETE" });
  }
}

export const api = new ApiClient();
