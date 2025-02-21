from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.permissions import BasePermission, AllowAny

class IsAuthenticatedForAPI(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class AllowAnyForLogin(BasePermission):
    def has_permission(self, request, view):
        return True


# 2. Middleware для защиты веб-страниц

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [reverse('login')]
    
    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in self.exempt_urls:
            return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response
