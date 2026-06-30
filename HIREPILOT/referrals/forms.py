from django import forms
from .models import EmployeeProfile, ReferralRequest


class EmployeeSignupForm(forms.ModelForm):
    """Employee self-registration form."""
    domain_tags_input = forms.CharField(
        max_length=500,
        required=False,
        help_text='Comma-separated skills/domains, e.g. Python, Django, Backend',
        widget=forms.TextInput(attrs={'placeholder': 'Python, Django, Backend, React...'})  
    )

    class Meta:
        model = EmployeeProfile
        fields = ['company', 'job_title', 'department', 'work_email']
        widgets = {
            'company': forms.TextInput(attrs={'placeholder': 'e.g. Google'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'e.g. Senior Software Engineer'}),
            'department': forms.TextInput(attrs={'placeholder': 'e.g. Engineering (optional)'}),
            'work_email': forms.EmailInput(attrs={'placeholder': 'you@company.com'}),
        }

    def clean_domain_tags_input(self):
        raw = self.cleaned_data.get('domain_tags_input', '')
        tags = [t.strip() for t in raw.split(',') if t.strip()]
        return tags

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.domain_tags = self.cleaned_data['domain_tags_input']
        if commit:
            instance.save()
        return instance


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': '______',
            'class': 'otp-input',
            'autocomplete': 'one-time-code',
            'inputmode': 'numeric',
        }),
        label='Enter 6-digit code'
    )


class ReferralRequestForm(forms.ModelForm):
    """Form for job seekers to send a referral request."""
    class Meta:
        model = ReferralRequest
        fields = ['resume', 'note']
        widgets = {
            'note': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Introduce yourself briefly — your background, target role, and why you\'d be a great fit...'
            }),
        }


class ReferralStageForm(forms.ModelForm):
    """Employee updates the pipeline stage."""
    class Meta:
        model = ReferralRequest
        fields = ['stage']


class ChatMessageForm(forms.Form):
    body = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type a message...'})
    )
