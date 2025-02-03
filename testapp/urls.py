from django.urls import path

from testapp.views import test_cookie, test_mail

app_name = 'testapp'

urlpatterns = [
    path('cookie/', test_cookie, name='test_cookie'),
    path('email/', test_mail, name='test_cookie'),
]
