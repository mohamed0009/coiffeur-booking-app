from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'hairdresser', 'service', 'date', 'start_time', 'status')
    list_filter = ('date', 'hairdresser', 'status')
    search_fields = ('customer__username', 'hairdresser__username', 'service__name')
    date_hierarchy = 'date'
    actions = ['confirm_bookings', 'cancel_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"{queryset.count()} bookings were successfully confirmed.")
    confirm_bookings.short_description = "Confirm selected bookings"

    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} bookings were successfully cancelled.")
    cancel_bookings.short_description = "Cancel selected bookings"
