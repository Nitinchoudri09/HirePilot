from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import User, Job, JobMatch, Resume
from app.schemas import JobCreate, JobOut, JobMatchOut
from app.auth.security import get_current_user, get_current_admin
from app.services.job_matcher import compute_eligibility

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=List[JobOut])
def list_jobs(
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Job).filter(Job.is_active == True)
    if search:
        q = q.filter(
            (Job.title.ilike(f"%{search}%")) | (Job.company.ilike(f"%{search}%")) | (Job.description.ilike(f"%{search}%"))
        )
    if location:
        q = q.filter(Job.location.ilike(f"%{location}%"))
    if type:
        q = q.filter(Job.job_type.ilike(f"%{type}%"))
    return q.order_by(Job.created_at.desc()).all()


# IMPORTANT: /matches/me MUST come before /{job_id} to avoid route shadowing
@router.get("/matches/me", response_model=List[JobMatchOut])
def my_matches(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(JobMatch)
        .filter(JobMatch.user_id == current_user.id)
        .order_by(JobMatch.eligibility_score.desc())
        .all()
    )


@router.post("/match", response_model=List[JobMatchOut])
def match_jobs(
    resume_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if resume_id:
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()

    if not resume:
        raise HTTPException(status_code=400, detail="Upload a resume first")

    jobs = db.query(Job).filter(Job.is_active == True).all()
    results = []

    for job in jobs:
        score, matched, missing = compute_eligibility(resume.skills or [], job)
        existing = db.query(JobMatch).filter(
            JobMatch.user_id == current_user.id, JobMatch.job_id == job.id
        ).first()

        if existing:
            existing.eligibility_score = score
            existing.matched_skills = matched
            existing.missing_skills = missing
            existing.resume_id = resume.id
            match = existing
        else:
            match = JobMatch(
                user_id=current_user.id,
                job_id=job.id,
                resume_id=resume.id,
                eligibility_score=score,
                matched_skills=matched,
                missing_skills=missing,
            )
            db.add(match)

        db.flush()
        results.append(match)

    db.commit()
    for m in results:
        db.refresh(m)

    results.sort(key=lambda x: x.eligibility_score, reverse=True)
    return results


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobOut, status_code=201)
def create_job(
    data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    job = Job(**data.model_dump(), posted_by_id=current_user.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
