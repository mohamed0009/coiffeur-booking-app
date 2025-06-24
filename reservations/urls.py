from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('book/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.booking_list, name='booking_list'),
    path('booking/<int:pk>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
] 