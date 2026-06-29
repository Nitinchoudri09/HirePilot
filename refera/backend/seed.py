"""Seed database with demo data for investor/HR demos."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import (
    User, UserRole, SubscriptionPlan, Job, Resume, ReferralRequest,
    ReferralStatus, JobMatch, ResumeAnalysis, Subscription,
)
from app.auth.security import get_password_hash

DEMO_PASSWORD = "Demo@12345"


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(User).filter(User.email == "admin@refera.app").first():
        print("Database already seeded. Skipping.")
        db.close()
        return

    print("Seeding Refera demo data...")

    admin = User(
        email="admin@refera.app",
        hashed_password=get_password_hash(DEMO_PASSWORD),
        full_name="Alex Morgan",
        role=UserRole.ADMIN,
        subscription_plan=SubscriptionPlan.PREMIUM,
        referral_limit=25,
        location="San Francisco, CA",
    )

    employees = [
        User(
            email="sarah.chen@refera.app",
            hashed_password=get_password_hash(DEMO_PASSWORD),
            full_name="Sarah Chen",
            role=UserRole.EMPLOYEE,
            company="Google",
            job_title="Senior Software Engineer",
            bio="5+ years at Google. Happy to refer strong backend engineers.",
            location="Mountain View, CA",
            linkedin_url="https://linkedin.com/in/sarahchen",
            referral_limit=25,
        ),
        User(
            email="mike.johnson@refera.app",
            hashed_password=get_password_hash(DEMO_PASSWORD),
            full_name="Mike Johnson",
            role=UserRole.EMPLOYEE,
            company="Microsoft",
            job_title="Engineering Manager",
            bio="Leading Azure platform team. Referring full-stack and cloud engineers.",
            location="Seattle, WA",
            referral_limit=25,
        ),
        User(
            email="priya.sharma@refera.app",
            hashed_password=get_password_hash(DEMO_PASSWORD),
            full_name="Priya Sharma",
            role=UserRole.EMPLOYEE,
            company="Amazon",
            job_title="SDE II",
            bio="AWS enthusiast. Open to referring candidates with strong system design skills.",
            location="Bangalore, India",
            referral_limit=25,
        ),
    ]

    candidates = [
        User(
            email="demo@refera.app",
            hashed_password=get_password_hash(DEMO_PASSWORD),
            full_name="Jordan Lee",
            role=UserRole.CANDIDATE,
            location="Austin, TX",
            bio="Full-stack developer looking for referral-backed opportunities.",
            referral_limit=3,
            referrals_used=1,
        ),
        User(
            email="emma.wilson@refera.app",
            hashed_password=get_password_hash(DEMO_PASSWORD),
            full_name="Emma Wilson",
            role=UserRole.CANDIDATE,
            location="New York, NY",
            subscription_plan=SubscriptionPlan.PREMIUM,
            referral_limit=25,
            referrals_used=2,
        ),
    ]

    db.add(admin)
    for e in employees:
        db.add(e)
    for c in candidates:
        db.add(c)
    db.commit()

    jobs_data = [
        {
            "title": "Senior Full Stack Engineer",
            "company": "Google",
            "description": "Build scalable web applications using React, TypeScript, and Go. Work on Google Cloud products serving millions of users.",
            "skills_required": ["React", "TypeScript", "Go", "System Design", "GCP"],
            "location": "Mountain View, CA",
            "experience_years": 5,
            "salary_range": "$180k - $250k",
            "job_type": "full-time",
        },
        {
            "title": "Backend Engineer",
            "company": "Microsoft",
            "description": "Design and implement microservices on Azure. Strong experience with C#, .NET, and distributed systems required.",
            "skills_required": ["C#", ".NET", "Azure", "Microservices", "SQL"],
            "location": "Seattle, WA",
            "experience_years": 3,
            "salary_range": "$140k - $190k",
            "job_type": "full-time",
        },
        {
            "title": "SDE II - AWS",
            "company": "Amazon",
            "description": "Join AWS team to build next-gen cloud infrastructure. Python, Java, and system design expertise needed.",
            "skills_required": ["Python", "Java", "AWS", "System Design", "Docker"],
            "location": "Bangalore, India",
            "experience_years": 4,
            "salary_range": "₹35L - ₹50L",
            "job_type": "full-time",
        },
        {
            "title": "Frontend Developer",
            "company": "Stripe",
            "description": "Create beautiful payment experiences with React and Next.js. Focus on performance and accessibility.",
            "skills_required": ["React", "Next.js", "TypeScript", "CSS", "Tailwind"],
            "location": "Remote",
            "experience_years": 2,
            "salary_range": "$120k - $160k",
            "job_type": "full-time",
        },
        {
            "title": "ML Engineer",
            "company": "OpenAI",
            "description": "Train and deploy large language models. PyTorch, NLP, and MLOps experience required.",
            "skills_required": ["Python", "PyTorch", "Machine Learning", "NLP", "MLOps"],
            "location": "San Francisco, CA",
            "experience_years": 3,
            "salary_range": "$200k - $300k",
            "job_type": "full-time",
        },
        {
            "title": "DevOps Engineer",
            "company": "Netflix",
            "description": "Manage CI/CD pipelines and cloud infrastructure at scale. Kubernetes and Terraform expertise.",
            "skills_required": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD"],
            "location": "Los Gatos, CA",
            "experience_years": 4,
            "salary_range": "$170k - $220k",
            "job_type": "full-time",
        },
    ]

    jobs = []
    for jd in jobs_data:
        job = Job(**jd, posted_by_id=admin.id)
        db.add(job)
        jobs.append(job)
    db.commit()

    demo_skills = [
        "Python", "JavaScript", "React", "TypeScript", "Node.js",
        "FastAPI", "PostgreSQL", "Docker", "AWS", "Git",
        "System Design", "REST API", "Tailwind", "Next.js",
    ]

    resume = Resume(
        user_id=candidates[0].id,
        file_name="jordan_lee_resume.pdf",
        file_type="pdf",
        raw_text=(
            "Jordan Lee — Full Stack Developer\n"
            "Experience: Software Engineer at TechCorp (2 years). Built React/Node.js applications.\n"
            "Skills: Python, JavaScript, React, TypeScript, Node.js, FastAPI, PostgreSQL, Docker, AWS.\n"
            "Education: B.Tech Computer Science, UT Austin.\n"
            "Projects: Built a SaaS referral platform with Next.js and FastAPI."
        ),
        skills=demo_skills,
        education=[{"degree": "B.Tech Computer Science", "institution": "UT Austin"}],
        experience=[{"title": "Software Engineer", "company": "TechCorp", "duration": "2 years"}],
        projects=[{"name": "AI Job Referral Network SaaS"}],
        ats_score=82.5,
        parsed_at=datetime.utcnow(),
    )
    db.add(resume)
    db.commit()

    for job in jobs:
        matched = [s for s in demo_skills if any(s.lower() in r.lower() for r in job.skills_required)]
        missing = [s for s in job.skills_required if s not in matched]
        ratio = len(matched) / max(len(job.skills_required), 1)
        score = min(round(ratio * 75 + 15, 1), 99.0)
        db.add(JobMatch(
            user_id=candidates[0].id,
            job_id=job.id,
            resume_id=resume.id,
            eligibility_score=score,
            matched_skills=matched,
            missing_skills=missing,
        ))

    db.add(ResumeAnalysis(
        resume_id=resume.id,
        job_id=jobs[0].id,
        job_description=jobs[0].description,
        ats_score=78.0,
        missing_keywords=["Go", "GCP"],
        matched_keywords=["React", "TypeScript", "System Design"],
        suggestions=[
            "Add Go programming experience or coursework",
            "Highlight GCP certifications or cloud projects",
            "Quantify impact: users served, latency reduced, etc.",
        ],
        ai_feedback="Strong frontend profile. Consider adding backend language diversity (Go) and GCP exposure to maximize match for Google roles.",
    ))

    db.add(ReferralRequest(
        candidate_id=candidates[0].id,
        employee_id=employees[0].id,
        job_id=jobs[0].id,
        resume_id=resume.id,
        status=ReferralStatus.PENDING,
        ai_generated_message=(
            "Hi Team,\n\nI'd like to refer Jordan Lee for the Senior Full Stack Engineer position at Google. "
            "They have strong experience in React, TypeScript, and system design. "
            "I've reviewed their background and believe they would be a great fit.\n\nBest regards,\nSarah Chen"
        ),
    ))
    db.add(ReferralRequest(
        candidate_id=candidates[0].id,
        employee_id=employees[1].id,
        job_id=jobs[1].id,
        resume_id=resume.id,
        status=ReferralStatus.ACCEPTED,
        notes="Strong candidate. Scheduling intro call.",
    ))
    db.add(ReferralRequest(
        candidate_id=candidates[1].id,
        employee_id=employees[2].id,
        job_id=jobs[2].id,
        status=ReferralStatus.REJECTED,
        notes="Looking for more AWS production experience.",
    ))

    db.add(Subscription(
        user_id=candidates[1].id,
        plan=SubscriptionPlan.PREMIUM,
        amount=999.0,
        expires_at=datetime.utcnow() + timedelta(days=25),
    ))

    db.commit()
    db.close()

    print("\n✅ Demo data seeded successfully!\n")
    print("Demo accounts (password: Demo@12345):")
    print("  Admin:     admin@refera.app")
    print("  Candidate: demo@refera.app")
    print("  Premium:   emma.wilson@refera.app")
    print("  Employee:  sarah.chen@refera.app")


if __name__ == "__main__":
    seed()
