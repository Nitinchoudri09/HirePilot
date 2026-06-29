from typing import List, Tuple
from app.models import Job


def compute_eligibility(
    resume_skills: List[str],
    job: Job,
) -> Tuple[float, List[str], List[str]]:
    job_skills = [s.lower() for s in (job.skills_required or [])]
    resume_lower = [s.lower() for s in resume_skills]

    if not job_skills:
        return 65.0, resume_skills[:5], []

    matched = []
    missing = []
    for js in job_skills:
        if any(js in rs or rs in js for rs in resume_lower):
            matched.append(js.title())
        else:
            missing.append(js.title())

    ratio = len(matched) / len(job_skills)
    exp_bonus = 0
    if job.experience_years <= 2:
        exp_bonus = 10
    elif job.experience_years <= 5:
        exp_bonus = 5

    score = min(round(ratio * 75 + exp_bonus + 15, 1), 99.0)
    return score, matched, missing
