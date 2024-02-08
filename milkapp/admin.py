from django.contrib import admin
from .models import *


# Определение классов ModelAdmin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image']  # Поля для отображения в списке
    search_fields = ['name']  # Поля для поиска


class OrderAdmin(admin.ModelAdmin):
    list_display = ['parent_name']
    # list_filter = ['services']  # Фильтры для списка заказов


# Регистрация моделей вместе с ModelAdmin классами
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Creator)
