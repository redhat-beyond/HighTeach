from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from study_group.models import StudyGroup
from course.models import TeacherCourse
from users.models import Profile


def homePage(request):
    if request.user.is_authenticated:
        return render(request, 'main/loggedInPage.html')
    return render(request, 'main/homePage.html')


class CustomLoginView(LoginView):
    template_name = 'main/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'main/loggedInPage.html')
        else:
            error_message = "Invalid username or password."
            messages.error(request, error_message)
            return render(request, 'main/login.html')


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        keyword = request.GET.get('q')
        context = {"study_groups": StudyGroup.objects.search_group_by_keyword(keyword),
                   "users": Profile.search_users_by_keyword(keyword),
                   "teacher_courses": TeacherCourse.objects.search_name(keyword)}
        return render(request, 'search.html', context)
