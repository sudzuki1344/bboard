from django.urls import path

from testapp.views import test_cookie

app_name = 'testapp'

urlpatterns = [
    path('', test_cookie, name='test_cookie'),
]
