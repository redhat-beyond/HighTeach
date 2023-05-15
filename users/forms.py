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