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

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

from jobs.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture',)

from .models import UserTask

class UserTaskForm(forms.ModelForm):
    class Meta:
        model = UserTask
        fields = ('title',)

from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            except UserModel.DoesNotExist:
                user = None
            except UserModel.MultipleObjectsReturned:
                user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()

            if user is not None:
                if user.check_password(password):
                    if not user.is_active:
                        raise forms.ValidationError(
                            "Please verify your email before logging in. Check your inbox.",
                            code='inactive',
                        )
            
        return super().clean()
