from django.db import models
from django.conf import settings

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    hairdresser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'hairdresser'})

    def __str__(self):
        return f"{self.name} by {self.hairdresser.username}"
