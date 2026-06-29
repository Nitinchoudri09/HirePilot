from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db
from app.models import User, ReferralRequest, ReferralStatus, Job, Resume, UserRole
from app.schemas import ReferralCreate, ReferralUpdate, ReferralOut, UserOut, JobOut
from app.auth.security import get_current_user
from app.services.ai_service import generate_referral_message
from app.config import get_settings

router = APIRouter(prefix="/referrals", tags=["Referrals"])
settings = get_settings()


def _referral_out(r: ReferralRequest) -> ReferralOut:
    def u(user: User) -> UserOut:
        return UserOut(
            id=user.id, email=user.email, full_name=user.full_name, role=user.role.value,
            avatar_url=user.avatar_url, company=user.company, job_title=user.job_title,
            bio=user.bio, location=user.location, linkedin_url=user.linkedin_url,
            subscription_plan=user.subscription_plan.value,
            referral_limit=user.referral_limit, referrals_used=user.referrals_used,
            created_at=user.created_at,
        )

    return ReferralOut(
        id=r.id, status=r.status.value, message=r.message,
        ai_generated_message=r.ai_generated_message, notes=r.notes,
        candidate=u(r.candidate), employee=u(r.employee), job=JobOut.model_validate(r.job),
        created_at=r.created_at, updated_at=r.updated_at,
    )


@router.post("/", response_model=ReferralOut, status_code=201)
async def create_referral(
    data: ReferralCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.referrals_used >= current_user.referral_limit:
        raise HTTPException(status_code=403, detail="Referral limit reached. Upgrade to premium.")

    employee = db.query(User).filter(User.id == data.employee_id, User.role == UserRole.EMPLOYEE).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    job = db.query(Job).filter(Job.id == data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    resume = None
    if data.resume_id:
        resume = db.query(Resume).filter(Resume.id == data.resume_id, Resume.user_id == current_user.id).first()
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()

    skills = resume.skills if resume else []
    ai_msg = await generate_referral_message(
        current_user.full_name, job.title, job.company, skills
    )

    referral = ReferralRequest(
        candidate_id=current_user.id,
        employee_id=employee.id,
        job_id=job.id,
        resume_id=resume.id if resume else None,
        message=data.message,
        ai_generated_message=ai_msg,
        status=ReferralStatus.PENDING,
    )
    current_user.referrals_used += 1
    db.add(referral)
    db.commit()
    db.refresh(referral)
    return _referral_out(referral)


@router.get("/sent", response_model=List[ReferralOut])
def sent_referrals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    refs = db.query(ReferralRequest).filter(ReferralRequest.candidate_id == current_user.id).all()
    return [_referral_out(r) for r in refs]


@router.get("/received", response_model=List[ReferralOut])
def received_referrals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    refs = db.query(ReferralRequest).filter(ReferralRequest.employee_id == current_user.id).all()
    return [_referral_out(r) for r in refs]


@router.patch("/{referral_id}", response_model=ReferralOut)
def update_referral(
    referral_id: int,
    data: ReferralUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    referral = db.query(ReferralRequest).filter(ReferralRequest.id == referral_id).first()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")

    if current_user.role.value != "admin" and referral.employee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    status_map = {"pending": ReferralStatus.PENDING, "accepted": ReferralStatus.ACCEPTED, "rejected": ReferralStatus.REJECTED}
    if data.status not in status_map:
        raise HTTPException(status_code=400, detail="Invalid status")

    referral.status = status_map[data.status]
    if data.notes:
        referral.notes = data.notes
    referral.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(referral)
    return _referral_out(referral)
