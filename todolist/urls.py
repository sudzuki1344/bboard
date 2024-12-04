from django.urls import path

from todolist.views import todo_create, todo_detail, todo_delete, todo_list, index

app_name = 'todolist'

urlpatterns = [
    # path('add/', BbCreateView.as_view(), name='add'),
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='add'),
    # path('add/', add_and_save, name='add'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    # path('detail/<int:bb_id>/', bb_detail, name='detail'),
    path('index/', index, name='index'),
    path('<int:todo_id>/', todo_detail, name='todo_detail'),
    path('create/', todo_create, name='todo_create'),
    path('delete/<int:todo_id>/', todo_delete, name='todo_delete')
]
