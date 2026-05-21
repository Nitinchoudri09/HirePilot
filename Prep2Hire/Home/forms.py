from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
