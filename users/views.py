from django.shortcuts import render, redirect
from .forms import ProfileForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import DetailView
from course.models import TeacherCourse
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('homePage')
        else:
            return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = RegistrationForm()
        profile_form = ProfileForm()
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(username=self.kwargs.get('slug')).first()
        context['courses'] = TeacherCourse.objects.get_teacher_courses(user)
        return context

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return 'user__username'


@login_required
def edit_profile(request, slug):
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
