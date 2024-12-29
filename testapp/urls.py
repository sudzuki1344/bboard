from django.urls import path
from testapp.views import SmsListView

app_name = 'testapp'

urlpatterns = [
    path('sms/', SmsListView.as_view(), name='sms_list'),
]
