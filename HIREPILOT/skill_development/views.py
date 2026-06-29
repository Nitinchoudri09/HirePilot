from django.shortcuts import render
import requests
import re
import random


def course_list(request):
    profile_ids = ["27878376", "2994446"]
    all_courses = []

    for profile_id in profile_ids:
        url = f"https://www.udemy.com/api-2.0/users/{profile_id}/taught-profile-courses/?learn_url"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            courses = data.get('results', [])
            for course in courses:
                locale_info = course.get('locale', {})
                if locale_info.get('simple_english_title') == 'English' or locale_info.get('locale', '').startswith('en_'):
                    all_courses.append(course)
        except Exception as e:
            print(f"Error fetching courses for profile ID {profile_id}: {e}")

    return render(request, 'course_list.html', {'courses': all_courses})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Option, QuizResult
from django.contrib.auth.decorators import login_required

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    score = 0
    results = []

    if request.method == 'POST':
        for q in questions:
            selected_id = request.POST.get(f'question_{q.id}')
            selected_option = Option.objects.filter(pk=selected_id).first()

            if selected_option:
                is_correct = selected_option.is_correct
                if is_correct:
                    score += 1
                results.append({
                    'question': q.text,
                    'selected': selected_option.text,
                    'is_correct': is_correct,
                    'correct_option': q.options.filter(is_correct=True).first().text
                })
            else:
                results.append({
                    'question': q.text,
                    'selected': 'Not Answered',
                    'is_correct': False,
                    'correct_option': q.options.filter(is_correct=True).first().text
                })

        # Save the result
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score, total=questions.count())

        return render(request, 'take_quiz.html', {
            'quiz': quiz,
            'questions': questions,
            'results': results,
            'score': score,
            'submitted': True,
            'total': questions.count()
        })

    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'submitted': False
    })

@login_required
def results_view(request):
    results = QuizResult.objects.filter(user=request.user)
    return render(request, 'quiz_results.html', {'results': results})

MUSE_API_URL = "https://www.themuse.com/api/public/jobs"
MAX_PAGES = random.randint(1, 10) 

SKILL_KEYWORDS = [
    "Python", "Java", "JavaScript", "React", "Angular", "Node.js",
    "Docker", "AWS", "SQL", "NoSQL", "HTML", "CSS", "Kubernetes",
    "Machine Learning", "Data Science", "Git", "REST API", "CI/CD", "TypeScript"
]

SKILL_MESSAGES = {
    "Python": "A versatile language used in web, data science, and automation.",
    "Java": "Widely used for enterprise and Android development.",
    "JavaScript": "Core of web development; essential for frontend.",
    "React": "Popular JS library for building modern UIs.",
    "Angular": "Framework by Google for dynamic web apps.",
    "Node.js": "Run JS server-side; great for scalable apps.",
    "Docker": "Essential for containerization and deployment.",
    "AWS": "Top cloud provider – learn it for DevOps and backend.",
    "SQL": "Must-know for databases and data analysis.",
    "NoSQL": "Flexible data models, useful for big data apps.",
    "HTML": "Foundation of every web page.",
    "CSS": "Styles your web pages beautifully.",
    "Kubernetes": "Orchestrates containers in production.",
    "Machine Learning": "Hot field in AI and automation.",
    "Data Science": "Combines coding, statistics, and insights.",
    "Git": "Version control for collaboration and safety.",
    "REST API": "Connect frontend and backend easily.",
    "CI/CD": "Automate testing and deployment pipeline.",
    "TypeScript": "Typed superset of JS; safer and modern."
}

@login_required
def trending_skills_view(request):
    all_descriptions = ""

    for page in range(1, MAX_PAGES + 1):
        response = requests.get(f"{MUSE_API_URL}?page={page}")
        if response.status_code != 200:
            break

        data = response.json()
        for job in data.get("results", []):
            contents = job.get("contents", "")
            all_descriptions += contents + " "

        if not data.get("page_count") or page >= data["page_count"]:
            break

    skill_found = []
    for skill in SKILL_KEYWORDS:
        pattern = re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE)
        if pattern.search(all_descriptions):
            skill_found.append({
                'name': skill,
                'message': SKILL_MESSAGES.get(skill, "A valuable technical skill."),
                'link': f"/jobs/roadmaps/{skill.lower()}"  # You can change this route
            })

    return render(request, 'trending_skills.html', {'skills': skill_found})