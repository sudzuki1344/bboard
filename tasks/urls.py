from django.urls import path
from . import views

urlpatterns = [
    # Task List endpoints
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    
    # Users endpoint
    path('users/', views.users_list, name='users_list'),
] 