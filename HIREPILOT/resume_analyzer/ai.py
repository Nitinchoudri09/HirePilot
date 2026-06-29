import os
import json
import logging
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

logger = logging.getLogger(__name__)

# Fallback sentence model
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            _model = None
    return _model

def setup_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            return genai
        except ImportError:
            return None
    return None

def analyze_resume_with_ai(resume_text, job_desc, job_title=""):
    """
    Returns a structured JSON dict containing score breakdown, 
    skills analysis, strengths, weaknesses, and suggestions.
    """
    genai = setup_gemini()
    if genai:
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) and senior recruiter.
        Analyze the following resume against the job title '{job_title}' and/or job description: '{job_desc}'.
        
        If the job description is short (e.g. just a title or a few words), automatically determine the standard required skills, preferred skills, and responsibilities for that role before evaluating the resume.
        
        Perform a deep semantic analysis (e.g. "Power BI Desktop" matches "Power BI", "Pandas" matches "Data Analysis").
        
        Calculate a weighted score out of 100 based on:
        - ATS Formatting (15%) - Is the resume well-structured and parsable?
        - Skills Match (30%) - Semantic matching of required skills.
        - Projects (20%) - Relevance and quality of projects.
        - Experience (20%) - Relevance of work history and internships.
        - Education (5%) - Does it meet standard requirements?
        - Resume Completeness (5%) - Are all standard sections present?
        - Grammar & Readability (5%) - Spelling, grammar, action verbs.
        
        Provide the response strictly as a JSON object with the following schema:
        {{
          "overall_match": 85,
          "breakdown": {{
            "ats_formatting": 94,
            "skills_match": 80,
            "projects": 88,
            "experience": 72,
            "education": 90,
            "resume_completeness": 96,
            "grammar_readability": 85
          }},
          "skills_analysis": {{
            "matched": ["Python", "SQL"],
            "missing": ["Tableau"],
            "recommended": ["Git"]
          }},
          "strengths": ["Strong Python skills", "Relevant internship"],
          "weaknesses": ["Missing Tableau", "No measurable achievements"],
          "suggestions": ["Add quantified achievements", "Include GitHub link"]
        }}
        
        Resume Text:
        {resume_text}
        """
        
        try:
            # We use gemini-1.5-flash as it is fast and supports JSON schema well, or pro if needed.
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(response.text)
            logger.info(f"Gemini analysis successful for job: {job_title}")
            return data
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            # Fallback to simple analysis on exception
            return fallback_analysis(resume_text, job_desc)
    else:
        # Fallback if no API key
        return fallback_analysis(resume_text, job_desc)

def fallback_analysis(resume_text, job_desc):
    """
    Fallback analysis using SentenceTransformers or TF-IDF.
    Provides basic JSON structure to match expected format.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    score = 0
    model = get_model()
    if model:
        from sentence_transformers import util
        embeddings = model.encode([resume_text, job_desc])
        sim_score = util.cos_sim(embeddings[0], embeddings[1])
        score = round(sim_score.item() * 100, 2)
    else:
        vect = TfidfVectorizer()
        tfidf = vect.fit_transform([resume_text, job_desc])
        sim_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        score = round(sim_score * 100, 2)
        
    words_resume = set(re.findall(r'\b[a-zA-Z]+\b', resume_text.lower()))
    words_jd = set(re.findall(r'\b[a-zA-Z]+\b', job_desc.lower()))
    
    keywords_resume = [w for w in words_resume if w not in ENGLISH_STOP_WORDS and len(w) > 2]
    keywords_jd = [w for w in words_jd if w not in ENGLISH_STOP_WORDS and len(w) > 2]
    
    missing = list(set(keywords_jd) - set(keywords_resume))
    matched = list(set(keywords_jd) & set(keywords_resume))
    
    return {
        "overall_match": score,
        "breakdown": {
            "ats_formatting": 70,
            "skills_match": score,
            "projects": 50,
            "experience": 50,
            "education": 50,
            "resume_completeness": 50,
            "grammar_readability": 50
        },
        "skills_analysis": {
            "matched": matched[:10],
            "missing": missing[:10],
            "recommended": []
        },
        "strengths": ["Basic formatting detected"],
        "weaknesses": ["Consider adding more keywords from the job description"],
        "suggestions": ["Tailor your resume closer to the job description to improve your score."]
    }
