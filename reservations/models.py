from django.db import models
from django.conf import settings
from services.models import Service

# Create your models here.

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings_as_customer', limit_choices_to={'role': 'customer'})
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    hairdresser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings_as_hairdresser', limit_choices_to={'role': 'hairdresser'})
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('hairdresser', 'date', 'start_time')

    def __str__(self):
        return f"Booking for {self.customer.username} with {self.hairdresser.username} on {self.date} at {self.start_time}"
