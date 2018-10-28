from django.contrib import admin
from .models import Employee, Jobs, Salary, Earnings, Deductions

admin.site.register(Employee)
admin.site.register(Jobs)
admin.site.register(Salary)
admin.site.register(Earnings)
admin.site.register(Deductions)
