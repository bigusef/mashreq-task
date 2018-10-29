from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Employee, Salary, Earnings, Deductions


@receiver(post_save, sender=Employee)
def create_employee_salary(sender, instance, created, **kwargs):
    if created:
        Salary.objects.create(employee=instance, main_salary=instance.main_salary)


@receiver(post_save, sender=Earnings)
def change_total_earnings(sender, instance, created, **kwargs):
    emp_salary = Salary.objects.get(employee=instance.employee)

    if created:
        emp_salary.total_earnings += instance.amount
    else:
        all_earnings = instance.employee.earnings_set.all()
        total_earnings = 0
        for item in all_earnings:
            total_earnings += item.amount
        emp_salary.total_earnings = total_earnings

    emp_salary.save()


@receiver(post_save, sender=Deductions)
def change_total_deductions(sender, instance, created, **kwargs):
    emp_salary = Salary.objects.get(employee=instance.employee)

    if created:
        emp_salary.total_deductions += instance.amount
    else:
        all_deductions = instance.employee.deductions_set.all()
        total_deductions = 0
        for item in all_deductions:
            total_deductions += item.amount
        emp_salary.total_deductions = total_deductions

    emp_salary.save()
