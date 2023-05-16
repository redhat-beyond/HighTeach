from django.shortcuts import render


def homePage(request):
    if request.user.is_authenticated:
        return render(request, 'main/loggedInPage.html')
    return render(request, 'main/homePage.html')
