from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib import messages


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
