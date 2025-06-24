from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_customer, name='register_customer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
] 