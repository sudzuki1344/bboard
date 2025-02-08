from django.contrib import admin
from .models import IceCreamStand, IceCream, Parent, Child

@admin.register(IceCreamStand)
class IceCreamStandAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'working_hours', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')

@admin.register(IceCream)
class IceCreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'flavor', 'price', 'stand', 'is_available')
    list_filter = ('type', 'is_available', 'stand')
    search_fields = ('name', 'flavor')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'phone')
    search_fields = ('last_name', 'first_name', 'email')

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date', 'parent')
    list_filter = ('birth_date',)
    search_fields = ('last_name', 'first_name')
