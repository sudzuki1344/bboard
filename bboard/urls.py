from django.urls import path

from bboard.views import index, by_rubric, BbCreateView, add, add_save, add_and_save, bb_detail

app_name = 'bboard'

urlpatterns = [
    # path('add/', BbCreateView.as_view(), name='add'),
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='add'),
    path('add/', add_and_save, name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('detail/<int:bb_id>/', bb_detail, name='detail'),
    path('', index, name='index'),
]
