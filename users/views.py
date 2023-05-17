from django.shortcuts import render, redirect
from .forms import ProfileForm, UserForm
from .forms import UserUpdateForm, ProfileUpdateForm #=================
from django.contrib.auth.decorators import login_required #=================
from .models import Profile
from django.contrib import messages
from django.views.generic import DetailView
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return 'user__username'


# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ProfileForm()
#     return render(request, 'profile.html', {'form': form})

def index(request):
    user_form = UserForm()
    profile_form = ProfileForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        try:
            if user_form.is_valid():
                user = user_form.save()
                profile = Profile(user=user)
                profile_form = ProfileForm(request.POST, instance=profile)
                if profile_form.is_valid():
                    profile_form.save()
        except Exception as error:
            messages.error(request, error)
            return render(request, 'users/index.html', {'user_form': user_form, 'profile_form': profile_form})
    # user_form = UserForm()
    # profile_form = ProfileForm()
    
    
    return render(request, 'users/index.html', {'user_form': user_form, 'profile_form': profile_form})

#===============================================================================

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('homePage')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit-profile.html', context)