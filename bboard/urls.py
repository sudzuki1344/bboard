from django.urls import path
from django.views.generic.edit import CreateView

from bboard.models import Bb
from bboard.views import index, by_rubric, BbCreateView, add_and_save, bb_detail, BbRubricBbsView, BbDetail, Index1

app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='add'),
    # path('add/', add_and_save, name='add'),
    # path('add/', CreateView.as_view(model=Bb, template_name="bboard/bb_create.html"), name='add'),

    # path('<int:rubric_id>/', by_rubric, name='by_rubric')
    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),
    path('detail/<int:bb_id>/', BbDetail.as_view(), name='detail'),
    path('', Index1.as_view(), name='index'),
]
