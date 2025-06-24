from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from .models import Service
from .forms import ServiceForm

def is_hairdresser(user):
    return user.is_authenticated and user.role == 'hairdresser'

# Create your views here.

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

@login_required
@user_passes_test(is_hairdresser)
def manage_services_list(request):
    services = Service.objects.filter(hairdresser=request.user)
    return render(request, 'services/manage_service_list.html', {'services': services})

@login_required
@user_passes_test(is_hairdresser)
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.hairdresser = request.user
            service.save()
            messages.success(request, 'Service added successfully.')
            return redirect('services:manage_services_list')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Add Service'})

@login_required
@user_passes_test(is_hairdresser)
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk, hairdresser=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('services:manage_services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Edit Service'})

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'
    success_url = reverse_lazy('services:manage_services_list')

    def get_queryset(self):
        return super().get_queryset().filter(hairdresser=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Service deleted successfully.")
        return super().form_valid(form)

delete_service = login_required(user_passes_test(is_hairdresser)(ServiceDeleteView.as_view()))
