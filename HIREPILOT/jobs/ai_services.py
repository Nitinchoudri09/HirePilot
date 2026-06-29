def mock_check_eligibility(resume_text, job_description):
    # Basic mock logic for eligibility
    return {
        'score': 85.0,
        'matched_skills': ['Python', 'Django', 'React'],
        'missing_skills': ['AWS', 'Docker']
    }

def mock_generate_referral_message(candidate_name, job_title, skills):
    return f"Hi, I am {candidate_name}. I noticed the open {job_title} role. With my background in {', '.join(skills)}, I would be a great fit. I'd love a referral."
