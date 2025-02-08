from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic.dates import DayArchiveView
from django.views.generic.edit import CreateView

from bboard.models import Bb
from bboard.views import (index, BbCreateView, BbEditView, BbDeleteView,
                         BbDetailView, BbRubricBbsView, BbRedirectView,
                         rubrics, bbs, search, flash_and_sign_view)

app_name = 'bboard'

urlpatterns = [
    # Объединяем маршруты для работы с объявлениями
    path('bb/', BbRubricBbsView.as_view(), name='bb_list'),  # список всех объявлений
    path('bb/<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),  # объявления рубрики
    path('bb/add/', BbCreateView.as_view(), name='add'),  # добавление
    path('bb/<int:pk>/', BbDetailView.as_view(), name='detail'),  # просмотр
    path('bb/<int:pk>/edit/', BbEditView.as_view(), name='edit'),  # редактирование
    path('bb/<int:pk>/delete/', BbDeleteView.as_view(), name='delete'),  # удаление

    # Объединяем маршруты для работы с рубриками
    path('rubrics/', rubrics, name='rubrics'),
    path('rubrics/<int:rubric_id>/bbs/', bbs, name='bbs'),

    # Поиск
    path('search/', search, name='search'),

    # Дополнительные функции
    path('flash-sign/', flash_and_sign_view, name='flash_sign'),
    
    # Архивные маршруты
    path('<int:year>/<int:month>/<int:day>/', BbRedirectView.as_view(), name='old_archive'),

    # Главная страница
    path('', index, name='index'),
]
