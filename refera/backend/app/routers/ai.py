from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User, Job, Resume
from app.schemas import (
    AIReferralMessageRequest, AIInterviewQuestionsRequest,
    AIEligibilityRequest, AIChatResponse,
)
from app.auth.security import get_current_user
from app.services.ai_service import generate_referral_message, generate_interview_questions, eligibility_chat
from app.services.job_matcher import compute_eligibility

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/referral-message")
async def ai_referral_message(
    data: AIReferralMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    skills = []
    if data.resume_id:
        resume = db.query(Resume).filter(Resume.id == data.resume_id, Resume.user_id == current_user.id).first()
        skills = resume.skills if resume else []
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()
        skills = resume.skills if resume else []

    message = await generate_referral_message(
        current_user.full_name, job.title, job.company, skills, data.tone
    )
    return {"message": message}


@router.post("/interview-questions")
async def ai_interview_questions(
    data: AIInterviewQuestionsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    questions = await generate_interview_questions(job.title, job.skills_required or [], data.count)
    return {"questions": questions}


@router.post("/eligibility", response_model=AIChatResponse)
async def ai_eligibility(
    data: AIEligibilityRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if data.resume_id:
        resume = db.query(Resume).filter(Resume.id == data.resume_id, Resume.user_id == current_user.id).first()
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()

    skills = resume.skills if resume else []
    score, matched, missing = compute_eligibility(skills, job)

    response = await eligibility_chat(
        current_user.full_name, job.title, job.company, score, matched, missing
    )
    return AIChatResponse(
        response=response,
        eligibility_score=score,
        matched_skills=matched,
        missing_skills=missing,
    )
