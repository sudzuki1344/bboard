from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from bboard.models import Rubric, Bb

# @admin.display(description='Название и рубрика')
# def title_and_rubric(rec):
#     return f'{rec.title} ({rec.rubric.name})'


class PriceListFilter(admin.SimpleListFilter):
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Низкая цена (до 500)'),
            ('medium', 'Средняя цена (500-5000)'),
            ('high', 'Высокая цена (более 5000)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=500, price__lte=5000)
        elif self.value() == 'high':
            return queryset.filter(price__gt=5000)


@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    # Улучшенное отображение списка
    list_display = ('title_with_link', 'rubric', 'price', 'price_formatted', 'kind', 'published')
    list_display_links = ('title_with_link',)
    list_editable = ('rubric', 'price', 'kind')
    list_per_page = 20
    list_select_related = ('rubric',)
    
    # Улучшенный поиск
    search_fields = ('title', 'content', 'rubric__name')
    search_help_text = 'Поиск по названию, содержанию и рубрике'
    
    # Расширенная фильтрация
    list_filter = ('kind', PriceListFilter, 'rubric', 'published')
    date_hierarchy = 'published'
    
    # Улучшенная организация полей
    fieldsets = (
        ('Основная информация', {
            'fields': (('title', 'kind'), 'rubric', 'content'),
            'classes': ('wide',),
        }),
        ('Цена и изображение', {
            'fields': ('price', 'img'),
            'classes': ('collapse',),
            'description': 'Укажите цену и при необходимости добавьте изображение'
        }),
        ('Дополнительно', {
            'fields': ('published',),
            'classes': ('collapse',),
        })
    )
    readonly_fields = ('published',)
    
    # Действия
    actions = ['mark_as_sold', 'recalculate_prices']
    
    def title_with_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
                         obj.get_absolute_url() if hasattr(obj, 'get_absolute_url') else '#',
                         obj.title)
    title_with_link.short_description = 'Название'
    title_with_link.admin_order_field = 'title'
    
    def price_formatted(self, obj):
        if obj.price:
            price_str = '{:,.2f}'.format(float(obj.price))
            color = 'green' if obj.price < 5000 else 'red'
            return format_html('<span style="color: {}">{} ₸</span>', 
                             color, price_str)
        return '-'
    price_formatted.short_description = 'Цена (форматированная)'
    price_formatted.admin_order_field = 'price'
    
    def mark_as_sold(self, request, queryset):
        # В реальном приложении здесь была бы логика отметки как проданных
        self.message_user(request, f'Отмечено как проданные: {queryset.count()} объявлений')
    mark_as_sold.short_description = 'Отметить как проданные'
    
    def recalculate_prices(self, request, queryset):
        # В реальном приложении здесь был бы пересчет цен
        self.message_user(request, f'Цены пересчитаны для {queryset.count()} объявлений')
    recalculate_prices.short_description = 'Пересчитать цены'


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'bb_count')
    list_editable = ('order',)
    search_fields = ('name',)
    
    def bb_count(self, obj):
        return obj.bb_set.count()
    bb_count.short_description = 'Количество объявлений'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(bb_count=Count('bb'))
