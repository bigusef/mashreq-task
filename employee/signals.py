from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Salary, Earnings, Deductions


@receiver(post_save, sender=Earnings)
def change_total_earnings(sender, instance, created, **kwargs):
    if created:
        emp_salary = Salary.objects.get(employee=instance.employee)
        emp_salary.total_earnings += instance.amount
        emp_salary.save()


@receiver(post_save, sender=Deductions)
def change_total_deductions(sender, instance, created, **kwargs):
    print('new deduction added')
