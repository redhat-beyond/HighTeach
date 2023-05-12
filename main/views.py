from django.shortcuts import render


def homePage(request):
    return render(request, 'main/homePage.html')
