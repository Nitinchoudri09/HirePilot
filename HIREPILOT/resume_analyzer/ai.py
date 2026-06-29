from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re

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

def calculate_similarity(resume_text, job_desc):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    model = get_model()
    if model:
        from sentence_transformers import util
        embeddings = model.encode([resume_text, job_desc])
        score = util.cos_sim(embeddings[0], embeddings[1])
        return round(score.item() * 100, 2)
    else:
        # fallback: TF-IDF cosine similarity
        vect = TfidfVectorizer()
        tfidf = vect.fit_transform([resume_text, job_desc])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(score * 100, 2)

def extract_keywords(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    keywords = [w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 2]
    return set(keywords)

def missing_keywords(resume_text, job_desc):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc)
    return list(jd_keywords - resume_keywords)

def generate_suggestions(missing_words):
    suggestions = []
    if any(word in missing_words for word in ["technology", "adaptability", "passionate"]):
        suggestions.append("Highlight your passion for technology and adaptability by mentioning projects where you quickly learned new tools or concepts.")
    if any(word in missing_words for word in ["software", "engineer", "programming", "languages", "scalable", "applications"]):
        suggestions.append("Emphasize your software engineering experience, especially in programming languages and building scalable applications.")
    if any(word in missing_words for word in ["object", "oriented", "problems"]):
        suggestions.append("Add examples of object-oriented programming and problem-solving in real-world scenarios.")
    if any(word in missing_words for word in ["aspiring", "learner", "quick", "concepts"]):
        suggestions.append("Showcase yourself as an aspiring engineer who is a quick learner and able to apply technical concepts effectively.")
    if "soft" in missing_words:
        suggestions.append("Mention your soft skills, such as teamwork, communication, and leadership abilities.")
    return suggestions
