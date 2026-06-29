from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: str = "candidate"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class GoogleAuthRequest(BaseModel):
    id_token: str


# ── User ──────────────────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    avatar_url: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    subscription_plan: str
    referral_limit: int
    referrals_used: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None


# ── Resume ────────────────────────────────────────────────────────────────────

class ResumeOut(BaseModel):
    id: int
    file_name: str
    file_url: Optional[str] = None
    skills: List[str] = []
    education: list = []
    experience: list = []
    projects: list = []
    ats_score: float
    parsed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeAnalysisOut(BaseModel):
    id: int
    ats_score: float
    missing_keywords: List[str] = []
    matched_keywords: List[str] = []
    suggestions: List[str] = []
    ai_feedback: Optional[str] = None
    job_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnalyzeJobRequest(BaseModel):
    job_id: Optional[int] = None
    job_description: Optional[str] = None


# ── Jobs ──────────────────────────────────────────────────────────────────────

class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    skills_required: List[str] = []
    location: Optional[str] = None
    experience_years: int = 0
    salary_range: Optional[str] = None
    job_type: str = "full-time"


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    description: str
    skills_required: List[str] = []
    location: Optional[str] = None
    experience_years: int
    salary_range: Optional[str] = None
    job_type: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class JobMatchOut(BaseModel):
    id: int
    eligibility_score: float
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    job: JobOut
    created_at: datetime

    class Config:
        from_attributes = True


# ── Referrals ─────────────────────────────────────────────────────────────────

class ReferralCreate(BaseModel):
    employee_id: int
    job_id: int
    resume_id: Optional[int] = None
    message: Optional[str] = None


class ReferralUpdate(BaseModel):
    status: str
    notes: Optional[str] = None


class ReferralOut(BaseModel):
    id: int
    status: str
    message: Optional[str] = None
    ai_generated_message: Optional[str] = None
    notes: Optional[str] = None
    candidate: UserOut
    employee: UserOut
    job: JobOut
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── AI ────────────────────────────────────────────────────────────────────────

class AIReferralMessageRequest(BaseModel):
    job_id: int
    resume_id: Optional[int] = None
    tone: str = "professional"


class AIInterviewQuestionsRequest(BaseModel):
    job_id: int
    count: int = 5


class AIEligibilityRequest(BaseModel):
    job_id: int
    resume_id: Optional[int] = None


class AIChatResponse(BaseModel):
    response: str
    eligibility_score: Optional[float] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []


# ── Payments ──────────────────────────────────────────────────────────────────

class CreateOrderRequest(BaseModel):
    plan: str = "premium"


class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminStats(BaseModel):
    total_users: int
    total_jobs: int
    total_referrals: int
    pending_referrals: int
    premium_users: int
    resumes_uploaded: int


Token.model_rebuild()
