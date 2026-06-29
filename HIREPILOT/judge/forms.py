from django import forms

class SubmissionForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea(attrs={'rows':20,'cols':100}), help_text="Submit Python code. Your function should read input from STDIN and print output to STDOUT.")
