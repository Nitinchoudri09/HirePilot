from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import (
    User, Job, ReferralRequest, ReferralStatus, Resume,
    SubscriptionPlan, AnalyticsEvent,
)
from app.schemas import AdminStats, JobCreate, JobOut, UserOut, ReferralOut
from app.auth.security import get_current_admin
from app.routers.referrals import _referral_out

router = APIRouter(prefix="/admin", tags=["Admin"])


def _user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id, email=user.email, full_name=user.full_name, role=user.role.value,
        avatar_url=user.avatar_url, company=user.company, job_title=user.job_title,
        bio=user.bio, location=user.location, linkedin_url=user.linkedin_url,
        subscription_plan=user.subscription_plan.value,
        referral_limit=user.referral_limit, referrals_used=user.referrals_used,
        created_at=user.created_at,
    )


@router.get("/stats", response_model=AdminStats)
def admin_stats(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return AdminStats(
        total_users=db.query(User).count(),
        total_jobs=db.query(Job).count(),
        total_referrals=db.query(ReferralRequest).count(),
        pending_referrals=db.query(ReferralRequest).filter(ReferralRequest.status == ReferralStatus.PENDING).count(),
        premium_users=db.query(User).filter(User.subscription_plan == SubscriptionPlan.PREMIUM).count(),
        resumes_uploaded=db.query(Resume).count(),
    )


@router.get("/users", response_model=List[UserOut])
def admin_users(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return [_user_out(u) for u in db.query(User).order_by(User.created_at.desc()).all()]


@router.patch("/users/{user_id}/toggle")
def toggle_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    return {"id": user.id, "is_active": user.is_active}


@router.get("/jobs", response_model=List[JobOut])
def admin_jobs(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return db.query(Job).order_by(Job.created_at.desc()).all()


@router.post("/jobs", response_model=JobOut, status_code=201)
def admin_create_job(data: JobCreate, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    job = Job(**data.model_dump(), posted_by_id=admin.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.delete("/jobs/{job_id}")
def admin_delete_job(job_id: int, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.is_active = False
    db.commit()
    return {"status": "deactivated"}


@router.get("/referrals", response_model=List[ReferralOut])
def admin_referrals(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    refs = db.query(ReferralRequest).order_by(ReferralRequest.created_at.desc()).all()
    return [_referral_out(r) for r in refs]
