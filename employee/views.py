from django.views.generic import ListView

from .models import Employee


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
