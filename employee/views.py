from django.views.generic import ListView, View
from django.shortcuts import redirect

from .models import Employee

from django.http import HttpResponse
from tablib import Dataset
from .resources import EmployeeResource


class DashboardView(ListView):
    template_name = 'employee/dashboard.html'
    model = Employee
    context_object_name = 'employee_list'
    paginate_by = 5

    def get_queryset(self):
        order = self.request.GET.get('orderby', 'pk')
        selected_txt = self.request.GET.get('filter')
        if order == 'age':
            context = sorted(Employee.objects.all(), key=lambda a: a.age)
        elif order == 'name':
            context = sorted(Employee.objects.all(), key=lambda a: a.full_name)
        else:
            context = Employee.objects.order_by(order)
        if selected_txt:
            context = context.filter(position__contains=selected_txt)
            print(self.request.page_obj)
        return context


class LoadExcelView(View):
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        resource = EmployeeResource()
        dataset = Dataset()
        new_persons = request.FILES['emp_file']
        dataset.load(new_persons.read())
        result = resource.import_data(dataset, dry_run=True)
        print(result)
        if not result.has_errors():
            resource.import_data(dataset, dry_run=False)
        return redirect('employee:dashboard')
