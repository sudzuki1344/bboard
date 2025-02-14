from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at', 'updated_at')  # поля, отображаемые в списке задач
    search_fields = ('title', 'description')  # добавляем возможность поиска по полям
    list_filter = ('completed',)  # фильтрация по статусу выполнения
    ordering = ('-created_at',)  # сортировка по дате создания (от новых к старым)

admin.site.register(Task, TaskAdmin) 