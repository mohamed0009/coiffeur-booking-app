from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hairdresser', 'duration', 'price')
    list_filter = ('hairdresser',)
    search_fields = ('name', 'hairdresser__username')
