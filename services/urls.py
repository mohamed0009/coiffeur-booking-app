from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('my-services/', views.manage_services_list, name='manage_services_list'),
    path('my-services/add/', views.add_service, name='add_service'),
    path('my-services/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('my-services/<int:pk>/delete/', views.delete_service, name='delete_service'),
] 