# forms.py

from django import forms
from .models import Profile

ROLE_CHOICES = [
    ('Frontend Developer', 'Frontend Developer'),
    ('Backend Developer', 'Backend Developer'),
    ('Full Stack Developer', 'Full Stack Developer'),
    ('Data Analyst', 'Data Analyst'),
    ('Data Scientist', 'Data Scientist'),
    ('Machine Learning Engineer', 'Machine Learning Engineer'),
    ('DevOps Engineer', 'DevOps Engineer'),
    ('Mobile App Developer', 'Mobile App Developer'),
    ('UI/UX Designer', 'UI/UX Designer'),
    ('Product Manager', 'Product Manager'),
    ('QA Engineer', 'QA Engineer'),
    ('Cybersecurity Analyst', 'Cybersecurity Analyst'),
    ('AI Engineer', 'AI Engineer'),
    ('Cloud Engineer', 'Cloud Engineer'),
    ('Systems Administrator', 'Systems Administrator'),
    ('Database Administrator', 'Database Administrator'),
    ('Blockchain Developer', 'Blockchain Developer'),
    ('AR/VR Developer', 'AR/VR Developer'),
    ('Game Developer', 'Game Developer'),
    ('Business Analyst', 'Business Analyst'),
    ('Technical Support Engineer', 'Technical Support Engineer'),
    ('Site Reliability Engineer', 'Site Reliability Engineer'),
    ('Software Tester', 'Software Tester'),
    ('Embedded Systems Engineer', 'Embedded Systems Engineer'),
    ('Network Engineer', 'Network Engineer'),
    ('Property Manager', 'Property Manager'),
]

class DesiredRoleForm(forms.ModelForm):
    desired_role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(required=True, help_text="Enter your email to receive matching jobs.")

    class Meta:
        model = Profile
        fields = ['desired_role']
