from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
def homePage(request):
    if request.user.is_authenticated:
        return render(request, 'main/loggedInPage.html')
    return render(request, 'main/homePage.html')


def logout_view(request):
    logout(request)
    return redirect('homePage')