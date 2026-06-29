from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db
from app.models import User, Resume, ResumeAnalysis, Job
from app.schemas import ResumeOut, ResumeAnalysisOut, AnalyzeJobRequest
from app.auth.security import get_current_user
from app.services.resume_parser import parse_resume, compare_with_job
from app.services.ai_service import generate_ai_feedback
from app.services.storage import save_file

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeOut)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed = (".pdf", ".docx", ".txt")
    if not file.filename.lower().endswith(allowed):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported")

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    try:
        parsed = parse_resume(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    file_url = await save_file(content, file.filename, current_user.id)

    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        file_url=file_url,
        file_type=file.filename.split(".")[-1],
        raw_text=parsed["raw_text"],
        skills=parsed["skills"],
        education=parsed["education"],
        experience=parsed["experience"],
        projects=parsed["projects"],
        ats_score=parsed["ats_score"],
        parsed_at=datetime.utcnow(),
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("/", response_model=List[ResumeOut])
def list_resumes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.post("/{resume_id}/analyze", response_model=ResumeAnalysisOut)
async def analyze_resume(
    resume_id: int,
    data: AnalyzeJobRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    job_description = data.job_description or ""
    job_skills: list = []
    job_id = data.job_id

    if data.job_id:
        job = db.query(Job).filter(Job.id == data.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        job_description = job.description
        job_skills = job.skills_required or []

    if not job_description:
        raise HTTPException(status_code=400, detail="Provide job_id or job_description")

    score, matched, missing, suggestions = compare_with_job(
        resume.raw_text or "",
        resume.skills or [],
        job_description,
        job_skills,
    )

    ai_feedback = await generate_ai_feedback(resume.raw_text or "", job_description, score)

    analysis = ResumeAnalysis(
        resume_id=resume.id,
        job_id=job_id,
        job_description=job_description,
        ats_score=score,
        missing_keywords=missing,
        matched_keywords=matched,
        suggestions=suggestions,
        ai_feedback=ai_feedback,
    )
    resume.ats_score = score
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/{resume_id}/analyses", response_model=List[ResumeAnalysisOut])
def list_analyses(resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume_id).order_by(ResumeAnalysis.created_at.desc()).all()
