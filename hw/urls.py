from django.urls import re_path
from hw.views import task_list, task_create, task_update, task_delete

app_name = 'hw'

urlpatterns = [
    re_path(r'^$', task_list, name='task_list'),
    re_path(r'^create/$', task_create, name='task_create'),
    re_path(r'^update/(?P<pk>\d+)/$', task_update, name='task_update'),
    re_path(r'^delete/(?P<pk>\d+)/$', task_delete, name='task_delete'),
]
