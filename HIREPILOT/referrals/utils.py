import io
import re

# Domain keyword taxonomy for tag matching
DOMAIN_KEYWORDS = [
    # Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'ruby', 'php', 'scala', 'r',
    # Web Frameworks
    'django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'nextjs', 'nodejs', 'express', 'spring', 'rails',
    # Data / ML
    'machine learning', 'deep learning', 'data science', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'sql', 'spark', 'hadoop',
    # Cloud / DevOps
    'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'terraform', 'ansible', 'ci/cd', 'devops', 'linux',
    # Databases
    'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
    # Mobile
    'android', 'ios', 'flutter', 'react native',
    # Design
    'ui/ux', 'figma', 'product design', 'graphic design',
    # Business / Domain
    'product management', 'marketing', 'sales', 'finance', 'hr', 'operations', 'consulting',
    # Other tech
    'cybersecurity', 'blockchain', 'api', 'microservices', 'system design', 'agile', 'scrum',
]


def extract_text_from_resume(file_obj):
    """Extract raw text from an uploaded PDF or DOCX resume file."""
    name = getattr(file_obj, 'name', '').lower()
    try:
        if name.endswith('.pdf'):
            from PyPDF2 import PdfReader
            reader = PdfReader(file_obj)
            return ' '.join(page.extract_text() or '' for page in reader.pages)
        elif name.endswith('.docx'):
            import docx2txt
            return docx2txt.process(file_obj)
        else:
            # Try reading as plain text
            content = file_obj.read()
            return content.decode('utf-8', errors='ignore')
    except Exception:
        return ''


def extract_keywords_from_text(text):
    """Extract matching domain keywords from resume text."""
    if not text:
        return []
    text_lower = text.lower()
    found = []
    for kw in DOMAIN_KEYWORDS:
        # Match whole word / phrase
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text_lower):
            found.append(kw.title() if len(kw.split()) == 1 else kw.upper() if '/' in kw else kw.title())
    return list(dict.fromkeys(found))  # deduplicate, preserve order


def match_employees_to_keywords(keywords):
    """Return verified EmployeeProfiles whose domain_tags overlap with keywords."""
    from .models import EmployeeProfile
    if not keywords:
        # Return all verified employees if no keywords found
        return EmployeeProfile.objects.filter(is_verified=True).select_related('user')[:20]

    keywords_lower = [k.lower() for k in keywords]
    employees = EmployeeProfile.objects.filter(is_verified=True).select_related('user')

    results = []
    for emp in employees:
        emp_tags_lower = [t.lower() for t in emp.domain_tags]
        overlap = [t for t in emp_tags_lower if t in keywords_lower]
        if overlap:
            emp.match_score = len(overlap)
            emp.matched_keywords = overlap
            results.append(emp)

    # Sort by match score descending
    results.sort(key=lambda e: getattr(e, 'match_score', 0), reverse=True)
    return results
