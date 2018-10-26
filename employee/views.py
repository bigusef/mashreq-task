from django.views.generic import ListView

from .models import Employee


class DashboardView(ListView):
    template_name = 'employee/dashboard.html'
    model = Employee
    context_object_name = 'employee_list'
