from django import forms #==============
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profession', 'city', 'phone_number', 'account_type', 'meeting_method']

class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

#=============================================================
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=500, required=False)
    profession = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'profession', 'city', 'phone_number', 'account_type', 'meeting_method']