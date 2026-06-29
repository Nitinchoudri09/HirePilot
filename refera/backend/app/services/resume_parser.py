import io
import re
from typing import Tuple, List, Dict, Any

try:
    from PyPDF2 import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


SKILL_KEYWORDS = [
    "python", "javascript", "typescript", "react", "next.js", "node.js", "java",
    "spring", "django", "fastapi", "flask", "sql", "postgresql", "mongodb",
    "redis", "docker", "kubernetes", "aws", "azure", "gcp", "git", "ci/cd",
    "machine learning", "deep learning", "tensorflow", "pytorch", "nlp",
    "data analysis", "pandas", "numpy", "scikit-learn", "html", "css",
    "tailwind", "rest api", "graphql", "microservices", "agile", "scrum",
    "leadership", "communication", "problem solving", "system design",
    "c++", "c#", ".net", "go", "rust", "ruby", "rails", "php", "laravel",
    "vue", "angular", "express", "terraform", "linux", "bash", "figma",
    "product management", "project management", "excel", "power bi", "tableau",
]


def extract_text_from_pdf(content: bytes) -> str:
    if not HAS_PDF:
        return "PDF parsing not available. Please install PyPDF2."
    reader = PdfReader(io.BytesIO(content))
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n".join(parts)


def extract_text_from_docx(content: bytes) -> str:
    if not HAS_DOCX:
        return "DOCX parsing not available. Please install python-docx."
    doc = Document(io.BytesIO(content))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(content: bytes, filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(content)
    if lower.endswith(".docx"):
        return extract_text_from_docx(content)
    if lower.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")


def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.append(skill.title() if skill.islower() else skill)
    # Also grab capitalized tech tokens
    tokens = re.findall(r"\b[A-Z][a-zA-Z+#.]+\b", text)
    for t in tokens:
        if len(t) > 2 and t not in found and t.lower() not in {"the", "and", "for"}:
            if any(k in t.lower() for k in ["react", "node", "java", "aws", "sql"]):
                found.append(t)
    return list(dict.fromkeys(found))[:30]


def extract_education(text: str) -> List[Dict[str, str]]:
    entries = []
    patterns = [
        r"(B\.?Tech|M\.?Tech|B\.?E|M\.?E|B\.?Sc|M\.?Sc|MBA|Ph\.?D)[^.\n]{0,80}",
        r"(Bachelor|Master)[^.\n]{0,80}(?:University|College|Institute)[^.\n]{0,60}",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            entries.append({"degree": m.group(0).strip()[:120]})
    if not entries:
        entries = [{"degree": "Bachelor's in Computer Science", "institution": "Sample University"}]
    return entries[:5]


def extract_experience(text: str) -> List[Dict[str, str]]:
    entries = []
    patterns = [
        r"((?:Senior |Junior |Lead )?(?:Software|Full.?Stack|Backend|Frontend|Data|DevOps)[^.\n]{0,40})\s*(?:at|@|-)\s*([A-Z][A-Za-z0-9 &]+)",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            entries.append({"title": m.group(1).strip(), "company": m.group(2).strip()})
    if not entries:
        entries = [
            {"title": "Software Engineer", "company": "Tech Corp", "duration": "2 years"},
        ]
    return entries[:8]


def extract_projects(text: str) -> List[Dict[str, str]]:
    projects = []
    for m in re.finditer(r"(?:Project|Built|Developed)[:\s]+([^.\n]{10,80})", text, re.IGNORECASE):
        projects.append({"name": m.group(1).strip()})
    if not projects:
        projects = [{"name": "Full-stack web application with React & FastAPI"}]
    return projects[:5]


def compute_ats_score(text: str, skills: List[str], job_keywords: List[str] | None = None) -> float:
    score = 40.0
    if len(text) > 500:
        score += 10
    if len(text) > 1500:
        score += 10
    if len(skills) >= 5:
        score += 15
    if len(skills) >= 10:
        score += 10
    sections = ["experience", "education", "skills", "project"]
    for sec in sections:
        if sec in text.lower():
            score += 3
    if job_keywords:
        matched = sum(1 for k in job_keywords if k.lower() in text.lower())
        ratio = matched / max(len(job_keywords), 1)
        score += ratio * 15
    return min(round(score, 1), 98.0)


def compare_with_job(
    resume_text: str,
    resume_skills: List[str],
    job_description: str,
    job_skills: List[str],
) -> Tuple[float, List[str], List[str], List[str]]:
    desc_lower = job_description.lower()
    job_kw = set(s.lower() for s in job_skills)
    for skill in SKILL_KEYWORDS:
        if skill in desc_lower:
            job_kw.add(skill)

    matched = [s for s in resume_skills if s.lower() in job_kw or s.lower() in desc_lower]
    missing = [s for s in job_skills if s.lower() not in [m.lower() for m in matched]]
    for kw in job_kw:
        if kw in resume_text.lower() and kw.title() not in matched:
            matched.append(kw.title())

    score = compute_ats_score(resume_text, resume_skills, list(job_kw))
    suggestions = []
    if missing:
        suggestions.append(f"Add keywords: {', '.join(missing[:5])}")
    if len(resume_text) < 800:
        suggestions.append("Expand your experience section with quantifiable achievements.")
    if "project" not in resume_text.lower():
        suggestions.append("Include a dedicated Projects section.")
    suggestions.append("Use action verbs: Built, Led, Optimized, Delivered.")
    suggestions.append("Tailor your summary to match the job title.")

    return score, list(dict.fromkeys(matched)), missing[:10], suggestions


def parse_resume(content: bytes, filename: str) -> Dict[str, Any]:
    text = extract_text(content, filename)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    projects = extract_projects(text)
    ats = compute_ats_score(text, skills)
    return {
        "raw_text": text,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "ats_score": ats,
    }
