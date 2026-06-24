from django.core.management.base import BaseCommand
from resume_analyzer.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Populates the database with Basic and Premium subscription plans.'

    def handle(self, *args, **kwargs):
        plans = [
            {
                'name': 'Basic Plan',
                'plan_type': 'basic',
                'price': 99.00,
                'credits': 2,
                'validity_days': 30,
                'description': 'Perfect for students and freshers to improve resumes before applying.\n- 2 Resume Analyses\n- ATS Score Generation\n- Keyword Analysis\n- Missing Skills Detection\n- Resume Improvement Suggestions'
            },
            {
                'name': 'Premium Plan',
                'plan_type': 'premium',
                'price': 299.00,
                'credits': 20,
                'validity_days': 30,
                'description': 'Best for active job seekers needing detailed ATS insights.\n- 20 Resume Analyses\n- Advanced ATS Scoring\n- Job Description Matching\n- Optimization Suggestions\n- Skill Gap Analysis\n- Priority Processing'
            }
        ]

        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.get_or_create(
                plan_type=plan_data['plan_type'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {plan.name}"))
            else:
                for key, value in plan_data.items():
                    setattr(plan, key, value)
                plan.save()
                self.stdout.write(self.style.SUCCESS(f"Updated {plan.name}"))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated subscription plans.'))
