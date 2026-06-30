import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Prep2Hire.settings")
django.setup()

from resume_analyzer.models import SubscriptionPlan

def populate_plans():
    plans = [
        {
            "name": "Basic Plan",
            "plan_type": "basic",
            "price": 99.00,
            "credits": 2,
            "validity_days": 30,
            "description": "Perfect for students and freshers to improve resumes before applying.\n- 2 Resume Analyses\n- ATS Score Generation\n- Keyword Analysis\n- Missing Skills Detection\n- Resume Improvement Suggestions",
        },
        {
            "name": "Premium Plan",
            "plan_type": "premium",
            "price": 299.00,
            "credits": 20,
            "validity_days": 30,
            "description": "Best for active job seekers needing detailed ATS insights.\n- 20 Resume Analyses\n- Advanced ATS Scoring\n- Job Description Matching\n- Optimization Suggestions\n- Skill Gap Analysis\n- Priority Processing",
        },
    ]

    print("Populating Subscription Plans...")
    for plan_data in plans:
        plan, created = SubscriptionPlan.objects.get_or_create(
            plan_type=plan_data["plan_type"],
            defaults={
                "name": plan_data["name"],
                "price": plan_data["price"],
                "credits": plan_data["credits"],
                "validity_days": plan_data["validity_days"],
                "description": plan_data["description"],
            }
        )
        if created:
            print(f"Created: {plan.name}")
        else:
            print(f"Already exists: {plan.name}")

    print("Successfully populated Subscription Plans!")

if __name__ == "__main__":
    populate_plans()
