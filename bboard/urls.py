from django.urls import path, include
from django.views.decorators.cache import cache_page
from django.views.generic.dates import WeekArchiveView, DayArchiveView
from django.views.generic.edit import CreateView
from rest_framework.routers import DefaultRouter

from bboard.models import Bb
from bboard.views import (APIRubricDetail, APIRubrics, index, by_rubric, BbCreateView,
                          add_and_save, bb_detail, BbRubricBbsView,
                          BbDetailView, BbEditView, BbDeleteView, BbIndexView,
                          BbRedirectView, edit, rubrics, bbs, search, api_rubrics, api_rubric_detail, APIRubricViewSet)

app_name = 'bboard'

router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)

urlpatterns = [
    # path('api/rubrics/<int:pk>/', api_rubric_detail),
    # path('api/rubrics/', api_rubrics),
    # path('api/rubrics/', APIRubrics.as_view()),
    # path('api/rubrics/<int:pk>/', APIRubricDetail.as_view()),
    path('api/', include(router.urls)),

    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),

    path('add/', BbCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    # path('edit/<int:pk>/', edit, name='edit'),

    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:rubric_id>/',
         BbRubricBbsView.as_view(),
         # cache_page(60 * 5)(BbRubricBbsView.as_view()),
         # cache_page(30)(BbRubricBbsView.as_view()),
         name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('search/', search, name='search'),

    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),
]
