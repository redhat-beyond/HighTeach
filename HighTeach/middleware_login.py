from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login


class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'POST' and request.path == reverse('admin:login'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and not user.is_staff:
                login(request, user)
                return redirect('homePage')
        return response
