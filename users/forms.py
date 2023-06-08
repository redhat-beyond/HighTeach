from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['account_type', 'phone_number', 'city', 'meeting_method', 'image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=500, required=False)
    profession = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'profession', 'city', 'phone_number', 'account_type', 'meeting_method', 'image']
