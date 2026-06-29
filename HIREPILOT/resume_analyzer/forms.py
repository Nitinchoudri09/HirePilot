from django import forms

class ResumeForm(forms.Form):
    job_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Software Engineer, Data Analyst',
            'class': 'form-input',
        })
    )
    job_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Paste the job description here...',
            'rows': 6,
            'class': 'form-input',
        })
    )
    resume = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': '.pdf,.docx,.doc'})
    )
