from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Booking, Service
from .forms import BookingForm
import datetime

def is_hairdresser(user):
    return user.is_authenticated and (user.role == 'hairdresser' or user.is_superuser)

# Create your views here.

@login_required
def create_booking(request):
    service_id = request.GET.get('service_id')
    initial_data = {}
    if service_id:
        service = get_object_or_404(Service, id=service_id)
        initial_data['service'] = service

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.hairdresser = booking.service.hairdresser
            
            # Calculate end_time
            start_datetime = datetime.datetime.combine(booking.date, booking.start_time)
            end_datetime = start_datetime + booking.service.duration
            booking.end_time = end_datetime.time()

            booking.save()
            messages.success(request, 'Your booking has been successfully created!')
            return redirect('reservations:booking_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'reservations/create_booking.html', {'form': form})

@login_required
def booking_list(request):
    if request.user.role == 'customer':
        bookings = Booking.objects.filter(customer=request.user).order_by('-date', '-start_time')
    elif request.user.role == 'hairdresser':
        bookings = Booking.objects.filter(hairdresser=request.user).order_by('-date', '-start_time')
    else: # for admin/superuser
        bookings = Booking.objects.all().order_by('-date', '-start_time')
        
    return render(request, 'reservations/booking_list.html', {'bookings': bookings})

@login_required
@user_passes_test(is_hairdresser)
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Ensure the user is the hairdresser for this booking or an admin
    if booking.hairdresser == request.user or request.user.is_superuser:
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Booking confirmed.')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
    return redirect('reservations:booking_list')

@login_required
@user_passes_test(is_hairdresser)
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Ensure the user is the hairdresser for this booking or an admin
    if booking.hairdresser == request.user or request.user.is_superuser:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'You are not authorized to perform this action.')
    return redirect('reservations:booking_list')
