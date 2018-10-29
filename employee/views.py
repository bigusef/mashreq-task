from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import redirect
from tablib import Dataset
from django.http import HttpResponse
from django.core.mail import EmailMessage

from .models import Employee
from .resources import EmployeeResource
from .forms import EmployeeForm
from .utils import render_to_pdf


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
        return context


class CreateEmployeeView(LoginRequiredMixin, CreateView):
    template_name = 'employee/partial/add.html'
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee:dashboard')


class UpdateEmployeeView(LoginRequiredMixin, UpdateView):
    template_name = 'employee/partial/edit.html'
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee:dashboard')


class DeleteEmployeeView(LoginRequiredMixin, DeleteView):
    template_name = 'employee/partial/delete.html'
    model = Employee
    success_url = reverse_lazy('employee:dashboard')


class LoadExcelView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        resource = EmployeeResource()
        dataset = Dataset()
        new_persons = request.FILES['emp_file']
        dataset.load(new_persons.read())
        result = resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            resource.import_data(dataset, dry_run=False)
        return redirect('employee:dashboard')


class SalaryDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('admin:login')
    template_name = 'employee/salary-detials.html'
    model = Employee

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            employee = Employee.objects.get(pk=kwargs['pk'])
            context = {
                'employee': employee
            }
            pdf = render_to_pdf('employee/pdf_template.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return super(SalaryDetailView, self).dispatch(request, args, kwargs)


class SendReportView(View):
    http_method_names = ['post']

    def dispatch(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=kwargs['pk'])
        recipient = [request.POST['email'], ]
        context = {
            'employee': employee
        }
        pdf = render_to_pdf('employee/pdf_template.html', context)

        subject = f'Salary Details for {employee.full_name}'
        message = 'Please find Salary Details PDF file on Attachments'
        email_from = 'e@g.com'

        mail = EmailMessage(subject, message, email_from, recipient)
        mail.attach_file(pdf)
        mail.send()
        return redirect('employee:dashboard')
