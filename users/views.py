from django.shortcuts import render, redirect
from .forms import ProfileForm, UserForm
from .models import Profile


# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ProfileForm()
#     return render(request, 'profile.html', {'form': form})

def index(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            profile = Profile(user=user)
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
    user_form = UserForm()
    profile_form = ProfileForm()
    
    
    return render(request, 'users/index.html', {'user_form': user_form, 'profile_form': profile_form})