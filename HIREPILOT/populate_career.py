import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prep2Hire.settings')
django.setup()

from Home.models import Question, Option, CareerSuggestion

def populate_career():
    print("Clearing old career data...")
    Question.objects.all().delete()
    CareerSuggestion.objects.all().delete()

    print("Creating career suggestions...")
    careers = [
        CareerSuggestion(career="Software Engineer", description="Design, develop, and maintain software applications. You love logic, coding, and building things from scratch.", skills_required="Python, Java, C++, Problem Solving, Data Structures"),
        CareerSuggestion(career="Data Scientist", description="Analyze and interpret complex data to help organizations make decisions. You love math, patterns, and machine learning.", skills_required="Python, R, Statistics, SQL, Machine Learning"),
        CareerSuggestion(career="Product Manager", description="Guide the success of a product and lead the cross-functional team that is responsible for improving it. You are a leader and visionary.", skills_required="Leadership, Communication, Agile, Strategy, Roadmapping"),
        CareerSuggestion(career="UX/UI Designer", description="Design the user interfaces and user experiences for digital products. You are creative and empathetic to user needs.", skills_required="Figma, Wireframing, User Research, Prototyping, CSS"),
        CareerSuggestion(career="Cybersecurity Analyst", description="Protect computer systems and networks from cyber threats. You love solving puzzles and thinking like a hacker.", skills_required="Network Security, Ethical Hacking, Linux, Cryptography"),
        CareerSuggestion(career="DevOps Engineer", description="Bridge the gap between development and IT operations to improve deployment speed and reliability.", skills_required="AWS/GCP, Docker, Kubernetes, CI/CD pipelines, Scripting")
    ]
    CareerSuggestion.objects.bulk_create(careers)

    print("Creating questions and options...")
    questions_data = [
        {
            "text": "When faced with a complex problem, what is your preferred approach?",
            "options": [
                {"text": "Write a script, algorithm, or code to solve it systematically.", "scores": {"Software Engineer": 10, "Data Scientist": 2}},
                {"text": "Analyze the data, create charts, and find underlying patterns.", "scores": {"Data Scientist": 10, "Software Engineer": 2}},
                {"text": "Organize a team meeting to discuss business solutions and timelines.", "scores": {"Product Manager": 10, "DevOps Engineer": 2}},
                {"text": "Sketch out possible visual solutions and map out user flows.", "scores": {"UX/UI Designer": 10, "Product Manager": 2}},
                {"text": "Look for vulnerabilities or edge cases where the system might fail.", "scores": {"Cybersecurity Analyst": 10, "DevOps Engineer": 5}}
            ]
        },
        {
            "text": "What type of work environment do you thrive in?",
            "options": [
                {"text": "Working independently with long blocks of focused coding time.", "scores": {"Software Engineer": 10, "Cybersecurity Analyst": 5}},
                {"text": "Diving deep into spreadsheets, algorithms, and numbers.", "scores": {"Data Scientist": 10, "Software Engineer": 2}},
                {"text": "Leading meetings, making strategic decisions, and talking to stakeholders.", "scores": {"Product Manager": 10, "UX/UI Designer": 2}},
                {"text": "Collaborating with users and testing out new creative ideas.", "scores": {"UX/UI Designer": 10, "Product Manager": 5}},
                {"text": "Automating infrastructure and making sure servers never go down.", "scores": {"DevOps Engineer": 10, "Software Engineer": 5}}
            ]
        },
        {
            "text": "Which tool or subject do you find most interesting to learn?",
            "options": [
                {"text": "A new programming language (like Rust or Go) or web framework.", "scores": {"Software Engineer": 10}},
                {"text": "A new statistical model, AI, or machine learning algorithm.", "scores": {"Data Scientist": 10}},
                {"text": "A new project management, roadmapping, or productivity software.", "scores": {"Product Manager": 10}},
                {"text": "A new design tool, prototyping software, or color theory.", "scores": {"UX/UI Designer": 10}},
                {"text": "Cloud computing platforms (AWS, Azure) or containerization (Docker).", "scores": {"DevOps Engineer": 10, "Software Engineer": 2}}
            ]
        },
        {
            "text": "How do you define a 'successful' project?",
            "options": [
                {"text": "The code is clean, bug-free, and highly efficient.", "scores": {"Software Engineer": 10, "DevOps Engineer": 5}},
                {"text": "The insights generated saved the company money or optimized a process.", "scores": {"Data Scientist": 10}},
                {"text": "The product launched on time and users are paying for it.", "scores": {"Product Manager": 10}},
                {"text": "The users find it incredibly beautiful, intuitive, and easy to use.", "scores": {"UX/UI Designer": 10}},
                {"text": "The system is impenetrable and perfectly secure from threats.", "scores": {"Cybersecurity Analyst": 10}}
            ]
        },
        {
            "text": "If you had a free weekend to build something, what would you make?",
            "options": [
                {"text": "A mobile app or a web application.", "scores": {"Software Engineer": 10}},
                {"text": "A predictive model for stock prices or sports scores.", "scores": {"Data Scientist": 10}},
                {"text": "I would write a business plan for a new startup idea.", "scores": {"Product Manager": 10}},
                {"text": "A beautiful portfolio website or a digital art piece.", "scores": {"UX/UI Designer": 10}},
                {"text": "A personal home server or a custom automated smart-home network.", "scores": {"DevOps Engineer": 10, "Cybersecurity Analyst": 5}}
            ]
        },
        {
            "text": "When using a new app, what is the first thing you notice?",
            "options": [
                {"text": "How fast it loads and if there are any bugs.", "scores": {"Software Engineer": 5, "DevOps Engineer": 5}},
                {"text": "The recommendation algorithms (like Netflix or TikTok).", "scores": {"Data Scientist": 10}},
                {"text": "The overall business model and how they monetize the app.", "scores": {"Product Manager": 10}},
                {"text": "The colors, typography, and how the buttons feel when clicked.", "scores": {"UX/UI Designer": 10}},
                {"text": "What data it asks for and how it handles my privacy.", "scores": {"Cybersecurity Analyst": 10}}
            ]
        },
        {
            "text": "Which of these tasks sounds the most exhausting to you?",
            "options": [
                {"text": "Leading a 3-hour meeting with marketing and sales teams.", "scores": {"Software Engineer": 5, "Data Scientist": 5, "Product Manager": -10}},
                {"text": "Staring at a massive Excel spreadsheet trying to find a math error.", "scores": {"UX/UI Designer": 10, "Product Manager": 5, "Data Scientist": -10}},
                {"text": "Spending hours fixing a single line of broken code.", "scores": {"Product Manager": 5, "UX/UI Designer": 5, "Software Engineer": -10}},
                {"text": "Worrying about a server crashing in the middle of the night.", "scores": {"UX/UI Designer": 5, "Data Scientist": 5, "DevOps Engineer": -10}}
            ]
        },
        {
            "text": "How do you handle conflict in a team setting?",
            "options": [
                {"text": "I rely on logic, documentation, and technical facts to prove my point.", "scores": {"Software Engineer": 10, "DevOps Engineer": 5}},
                {"text": "I run an A/B test or pull data to see which side is statistically correct.", "scores": {"Data Scientist": 10}},
                {"text": "I mediate the discussion, find a compromise, and keep the team moving.", "scores": {"Product Manager": 10}},
                {"text": "I try to understand the other person's perspective and find a creative solution.", "scores": {"UX/UI Designer": 10}},
                {"text": "I enforce the strict rules and protocols, regardless of feelings.", "scores": {"Cybersecurity Analyst": 10}}
            ]
        },
        {
            "text": "Which superpower would you rather have?",
            "options": [
                {"text": "The ability to instantly learn any language (including programming).", "scores": {"Software Engineer": 10, "DevOps Engineer": 5}},
                {"text": "The ability to predict the future.", "scores": {"Data Scientist": 10, "Product Manager": 5}},
                {"text": "The ability to read people's minds and influence them.", "scores": {"Product Manager": 10, "UX/UI Designer": 5}},
                {"text": "The ability to make everything you touch perfectly beautiful.", "scores": {"UX/UI Designer": 10}},
                {"text": "The ability to be completely invisible and undetectable.", "scores": {"Cybersecurity Analyst": 10}}
            ]
        },
        {
            "text": "What kind of news articles do you click on most often?",
            "options": [
                {"text": "New software releases, tech stack updates, or programming tips.", "scores": {"Software Engineer": 10}},
                {"text": "Breakthroughs in AI, ChatGPT, and deep learning.", "scores": {"Data Scientist": 10}},
                {"text": "Startup funding, company acquisitions, and CEO interviews.", "scores": {"Product Manager": 10}},
                {"text": "Design trends, new typography, or psychology of users.", "scores": {"UX/UI Designer": 10}},
                {"text": "Massive data breaches, hacker groups, or new zero-day exploits.", "scores": {"Cybersecurity Analyst": 10}}
            ]
        },
        {
            "text": "If someone asked you to build a bridge, what is your first step?",
            "options": [
                {"text": "Calculate the physics, load-bearing capacities, and material strengths.", "scores": {"Software Engineer": 10, "Data Scientist": 5}},
                {"text": "Determine the budget, timeline, and who is going to use the bridge.", "scores": {"Product Manager": 10}},
                {"text": "Sketch what the bridge will look like and how pedestrians will experience it.", "scores": {"UX/UI Designer": 10}},
                {"text": "Build the foundational scaffolding and ensure the supply chain is automated.", "scores": {"DevOps Engineer": 10}},
                {"text": "Analyze how an enemy might try to destroy the bridge so I can reinforce it.", "scores": {"Cybersecurity Analyst": 10}}
            ]
        },
        {
            "text": "How do you prefer your daily schedule?",
            "options": [
                {"text": "Highly structured with long uninterrupted blocks for deep work.", "scores": {"Software Engineer": 10, "Data Scientist": 5}},
                {"text": "A mix of independent research and presenting findings to a team.", "scores": {"Data Scientist": 10, "Software Engineer": 5}},
                {"text": "Constantly shifting, full of meetings, planning, and putting out fires.", "scores": {"Product Manager": 10, "DevOps Engineer": 5}},
                {"text": "Flexible and fluid, allowing inspiration to strike when it does.", "scores": {"UX/UI Designer": 10}}
            ]
        },
        {
            "text": "Choose a desk setup:",
            "options": [
                {"text": "Two vertical monitors full of terminal windows and code.", "scores": {"Software Engineer": 10, "DevOps Engineer": 5}},
                {"text": "A massive ultrawide monitor with a dozen charts and graphs open.", "scores": {"Data Scientist": 10}},
                {"text": "A laptop, a notebook, sticky notes, and a very large coffee.", "scores": {"Product Manager": 10}},
                {"text": "An iPad Pro, an Apple Pencil, and a beautifully minimalist desk.", "scores": {"UX/UI Designer": 10}},
                {"text": "Three monitors, a VPN running, and a mechanical keyboard.", "scores": {"Cybersecurity Analyst": 10, "DevOps Engineer": 5}}
            ]
        },
        {
            "text": "What is the most satisfying part of a project?",
            "options": [
                {"text": "Finally getting the code to compile and run perfectly.", "scores": {"Software Engineer": 10}},
                {"text": "Discovering an insight in the data that no one else saw.", "scores": {"Data Scientist": 10}},
                {"text": "Shipping the final product to users and watching them use it.", "scores": {"Product Manager": 10}},
                {"text": "Seeing your design come to life exactly as you envisioned it.", "scores": {"UX/UI Designer": 10}},
                {"text": "Knowing the system is completely automated and runs itself.", "scores": {"DevOps Engineer": 10}}
            ]
        },
        {
            "text": "What sounds like the worst nightmare at work?",
            "options": [
                {"text": "Having to talk to customers all day.", "scores": {"Software Engineer": 10, "Cybersecurity Analyst": 5}},
                {"text": "Having to make a decision without any data to back it up.", "scores": {"Data Scientist": 10}},
                {"text": "Being told you have zero authority over the project's direction.", "scores": {"Product Manager": 10}},
                {"text": "Being forced to use ugly, outdated colors and fonts.", "scores": {"UX/UI Designer": 10}},
                {"text": "A massive production database gets deleted and there are no backups.", "scores": {"DevOps Engineer": 10, "Cybersecurity Analyst": 5}}
            ]
        }
    ]

    for q_data in questions_data:
        question = Question.objects.create(text=q_data["text"])
        for opt_data in q_data["options"]:
            Option.objects.create(
                question=question,
                text=opt_data["text"],
                score_map=opt_data["scores"]
            )
            
    print(f"Career data populated successfully! Created {len(questions_data)} questions.")

if __name__ == '__main__':
    populate_career()
