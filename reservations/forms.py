from django import forms
from .models import Booking
import datetime

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().isoformat()}))

    class Meta:
        model = Booking
        fields = ['service', 'date', 'start_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        service = cleaned_data.get("service")

        if date and start_time and service:
            hairdresser = service.hairdresser
            end_time = (datetime.datetime.combine(date, start_time) + service.duration).time()

            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                hairdresser=hairdresser,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if overlapping_bookings:
                raise forms.ValidationError("This time slot is already booked. Please choose a different time.")

        return cleaned_data 