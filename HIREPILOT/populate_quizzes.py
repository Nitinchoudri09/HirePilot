import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prep2Hire.settings')
django.setup()

from skill_development.models import Quiz, Question, Option

# 10 High-Quality Manual Quizzes
real_quizzes = [
    {
        "title": "Python Basics",
        "description": "Test your fundamental Python knowledge.",
        "questions": [
            {
                "text": "Which of the following is a mutable data type in Python?",
                "options": [("List", True), ("Tuple", False), ("String", False), ("Integer", False)]
            },
            {
                "text": "What is the output of 3 ** 2?",
                "options": [("9", True), ("6", False), ("8", False), ("32", False)]
            }
        ]
    },
    {
        "title": "Django Framework Basics",
        "description": "Quiz on Django fundamentals.",
        "questions": [
            {
                "text": "Which file is used to configure database settings in Django?",
                "options": [("settings.py", True), ("models.py", False), ("urls.py", False), ("views.py", False)]
            },
            {
                "text": "What command is used to apply database migrations?",
                "options": [("python manage.py migrate", True), ("python manage.py makemigrations", False), ("django-admin migrate", False), ("python migrate.py", False)]
            }
        ]
    },
    {
        "title": "HTML & CSS Fundamentals",
        "description": "Test your web design basics.",
        "questions": [
            {
                "text": "Which HTML tag is used to create a hyperlink?",
                "options": [("<a>", True), ("<link>", False), ("<href>", False), ("<url>", False)]
            },
            {
                "text": "How do you select an element with id 'header' in CSS?",
                "options": [("#header", True), (".header", False), ("header", False), ("*header", False)]
            }
        ]
    },
    {
        "title": "Comprehensive Interview Prep",
        "description": "A 20-question deep dive into full-stack development, algorithms, and general software engineering.",
        "questions": [
            {
                "text": "What does HTTP stand for?",
                "options": [("HyperText Transfer Protocol", True), ("HyperText Transmission Protocol", False), ("Hyper Transfer Text Protocol", False), ("Hyperlink Transfer Technology Protocol", False)]
            },
            {
                "text": "Which CSS property controls the text size?",
                "options": [("font-size", True), ("text-style", False), ("font-style", False), ("text-size", False)]
            },
            {
                "text": "In Python, which of the following is NOT a built-in data type?",
                "options": [("Array", True), ("Dictionary", False), ("Set", False), ("List", False)]
            },
            {
                "text": "What is the primary purpose of the 'git clone' command?",
                "options": [("To copy a repository to your local machine", True), ("To upload local changes to a remote repository", False), ("To create a new branch", False), ("To merge two branches together", False)]
            },
            {
                "text": "Which SQL statement is used to extract data from a database?",
                "options": [("SELECT", True), ("EXTRACT", False), ("GET", False), ("OPEN", False)]
            },
            {
                "text": "What does the 'self' keyword represent in Python classes?",
                "options": [("The instance of the class", True), ("The parent class", False), ("A private variable", False), ("A static method", False)]
            },
            {
                "text": "Which of the following is a Javascript framework?",
                "options": [("React", True), ("Django", False), ("Laravel", False), ("Flask", False)]
            },
            {
                "text": "What does API stand for?",
                "options": [("Application Programming Interface", True), ("Automated Program Integration", False), ("Applied Programming Interface", False), ("Application Process Integration", False)]
            },
            {
                "text": "In Django, what is the role of 'models.py'?",
                "options": [("To define database tables and relationships", True), ("To handle URL routing", False), ("To write HTML templates", False), ("To manage CSS and static files", False)]
            },
            {
                "text": "What is the time complexity of a binary search?",
                "options": [("O(log n)", True), ("O(n)", False), ("O(n^2)", False), ("O(1)", False)]
            },
            {
                "text": "Which HTTP method is typically used to create a new resource?",
                "options": [("POST", True), ("GET", False), ("PUT", False), ("DELETE", False)]
            },
            {
                "text": "What does a 404 HTTP status code mean?",
                "options": [("Not Found", True), ("Internal Server Error", False), ("Unauthorized", False), ("Bad Request", False)]
            },
            {
                "text": "What is the purpose of 'Docker'?",
                "options": [("To containerize applications for consistent environments", True), ("To write server-side code", False), ("To manage SQL databases", False), ("To compile C++ code", False)]
            },
            {
                "text": "In JavaScript, what does '===' check?",
                "options": [("Both value and type equality", True), ("Only value equality", False), ("Only type equality", False), ("If an object is empty", False)]
            },
            {
                "text": "What does 'ORM' stand for in Django?",
                "options": [("Object-Relational Mapping", True), ("Object-Routine Mapping", False), ("Operational Resource Management", False), ("Object-Relational Model", False)]
            },
            {
                "text": "Which design pattern restricts a class to a single instance?",
                "options": [("Singleton", True), ("Factory", False), ("Observer", False), ("Decorator", False)]
            },
            {
                "text": "What is the difference between a list and a tuple in Python?",
                "options": [("Lists are mutable, tuples are immutable", True), ("Tuples are mutable, lists are immutable", False), ("Lists can hold mixed types, tuples cannot", False), ("Tuples are faster for sorting", False)]
            },
            {
                "text": "What command is used to save changes in Git?",
                "options": [("git commit", True), ("git add", False), ("git save", False), ("git push", False)]
            },
            {
                "text": "Which HTML tag is used to define an unordered list?",
                "options": [("<ul>", True), ("<ol>", False), ("<li>", False), ("<list>", False)]
            },
            {
                "text": "What is the main function of CSS?",
                "options": [("To style and layout web pages", True), ("To add interactivity to elements", False), ("To define the structure of a document", False), ("To query the database", False)]
            }
        ]
    }
]

# We will generate 100 total quizzes
topics = [
    "JavaScript", "React", "Node.js", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP",
    "SQL", "MongoDB", "PostgreSQL", "AWS", "Azure", "GCP", "Docker", "Kubernetes",
    "Git", "Linux", "Data Structures", "Algorithms", "Machine Learning", "Deep Learning",
    "Natural Language Processing", "Computer Vision", "Cybersecurity", "Networking",
    "System Design", "Microservices", "REST APIs", "GraphQL", "TypeScript", "Vue.js",
    "Angular", "Svelte", "Tailwind CSS", "Bootstrap", "Webpack", "Babel", "Jest",
    "Mocha", "Cypress", "Selenium", "TensorFlow", "PyTorch", "Scikit-Learn", "Pandas"
]

created_count = 0

# Create the real quizzes first
for q_data in real_quizzes:
    quiz, created = Quiz.objects.get_or_create(title=q_data["title"], defaults={"description": q_data["description"]})
    if created:
        for question_data in q_data["questions"]:
            q = Question.objects.create(quiz=quiz, text=question_data["text"])
            for opt_text, is_corr in question_data["options"]:
                Option.objects.create(question=q, text=opt_text, is_correct=is_corr)
        created_count += 1
        print(f"Created Real Quiz: {quiz.title}")

# Procedurally generate the rest to reach 100
quizzes_needed = 100 - created_count

for i in range(quizzes_needed):
    topic = random.choice(topics)
    level = random.randint(1, 10)
    title = f"{topic} Mastery - Level {level} (Part {i+1})"
    description = f"A dynamically generated quiz to test your skills in {topic} at Level {level}."
    
    quiz, created = Quiz.objects.get_or_create(title=title, defaults={"description": description})
    if created:
        # Create 5 procedural questions
        for q_num in range(1, 6):
            question = Question.objects.create(quiz=quiz, text=f"Which of the following best describes a core concept in {topic} (Question {q_num})?")
            
            # 1 correct, 3 incorrect
            correct_opt = random.randint(1, 4)
            for opt_num in range(1, 5):
                if opt_num == correct_opt:
                    Option.objects.create(question=question, text=f"The correct implementation principle for {topic}.", is_correct=True)
                else:
                    Option.objects.create(question=question, text=f"An incorrect or deprecated approach.", is_correct=False)
                    
        created_count += 1
        print(f"Created Procedural Quiz: {quiz.title}")

print(f"\nSuccessfully added {created_count} quizzes to the database.")
