from typing import Optional, List
from app.config import get_settings

settings = get_settings()


def _openai_available() -> bool:
    return bool(settings.OPENAI_API_KEY)


async def generate_ai_feedback(resume_text: str, job_description: str, score: float) -> str:
    if _openai_available():
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert career coach and ATS specialist."},
                    {"role": "user", "content": f"Resume excerpt:\n{resume_text[:2000]}\n\nJob:\n{job_description[:1500]}\n\nATS score: {score}%. Give 3-4 actionable improvements."},
                ],
                max_tokens=400,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            pass

    return (
        f"Your resume scores {score}% for this role. "
        "Strengthen your summary with role-specific keywords, quantify achievements with metrics, "
        "and align project descriptions with the job's core technologies. "
        "Consider adding certifications or open-source contributions relevant to this position."
    )


async def generate_referral_message(
    candidate_name: str,
    job_title: str,
    company: str,
    skills: List[str],
    tone: str = "professional",
) -> str:
    skills_str = ", ".join(skills[:6]) if skills else "relevant technical skills"
    if _openai_available():
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"Write a {tone} employee referral message for an internal referral program."},
                    {"role": "user", "content": f"Refer {candidate_name} for {job_title} at {company}. Skills: {skills_str}. Keep under 150 words."},
                ],
                max_tokens=250,
            )
            return resp.choices[0].message.content or ""
        except Exception:
            pass

    return (
        f"Hi Team,\n\nI'd like to refer {candidate_name} for the {job_title} position at {company}. "
        f"They have strong experience in {skills_str} and would be a great cultural fit. "
        f"I've reviewed their background and believe they can contribute immediately.\n\n"
        f"Please let me know if you'd like an introduction.\n\nBest regards"
    )


async def generate_interview_questions(job_title: str, skills: List[str], count: int = 5) -> List[str]:
    skills_str = ", ".join(skills[:5])
    if _openai_available():
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            resp = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Generate interview questions, one per line, no numbering."},
                    {"role": "user", "content": f"Generate {count} interview questions for {job_title}. Focus on: {skills_str}"},
                ],
                max_tokens=400,
            )
            text = resp.choices[0].message.content or ""
            return [q.strip().lstrip("0123456789.-) ") for q in text.split("\n") if q.strip()][:count]
        except Exception:
            pass

    base = [
        f"Describe your experience with {skills[0] if skills else 'the core stack'} in production.",
        f"How would you design a scalable system for a {job_title} role?",
        "Tell me about a challenging bug you solved and your debugging process.",
        "How do you prioritize tasks when working on multiple features?",
        "Walk me through a project you're most proud of.",
        "How do you stay updated with industry trends?",
        "Describe a time you collaborated with cross-functional teams.",
    ]
    return base[:count]


async def eligibility_chat(
    candidate_name: str,
    job_title: str,
    company: str,
    eligibility_score: float,
    matched: List[str],
    missing: List[str],
) -> str:
    if eligibility_score >= 75:
        verdict = "Yes — you're a strong match for this role."
    elif eligibility_score >= 50:
        verdict = "Partially — you're eligible but should upskill in a few areas."
    else:
        verdict = "Not yet — consider building more relevant experience first."

    matched_str = ", ".join(matched[:6]) if matched else "limited overlap"
    missing_str = ", ".join(missing[:5]) if missing else "none critical"

    return (
        f"{verdict}\n\n"
        f"For **{job_title}** at **{company}**, your eligibility score is **{eligibility_score}%**.\n\n"
        f"**Matching skills:** {matched_str}\n"
        f"**Gaps to address:** {missing_str}\n\n"
        f"Tip: Tailor your resume summary and add 1-2 projects demonstrating {missing[0] if missing else 'the required stack'}."
    )
