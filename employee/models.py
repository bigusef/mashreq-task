from django.db import models
from datetime import date

from django_countries.fields import CountryField


class Employee(models.Model):
    GENDER_CHOICES = ('m', 'Male'), ('f', 'Female')
    MARITAL_CHOICES = ('m', 'Married'), ('w', 'Widowed'), ('p', 'Separated'), ('d', 'Divorced'), ('s', 'Single')

    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    identifier = models.BigIntegerField()
    position = models.CharField(max_length=50)
    country = CountryField()
    nationality = CountryField()
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    @property
    def full_name(self):
        if self.middle_name:
            return ' '.join([self.first_name, self.middle_name, self.last_name])
        else:
            return ' '.join([self.first_name, self.last_name])

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return self.full_name


class Jobs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Salary(models.Model):
    def __init__(self, *args, **kwargs):
        self.__tax_rate = 0.05
        super(Salary, self).__init__(*args, **kwargs)

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    main_salary = models.IntegerField()
    total_earnings = models.IntegerField(default=0)
    total_deductions = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_salary(self):
        extra = self.total_earnings - self.total_deductions
        res = self.main_salary + extra
        return res

    @property
    def taxable_salary(self):
        res = self.total_salary * self.__tax_rate
        return res

    @property
    def net_salary(self):
        res = self.total_salary - self.taxable_salary
        return res

    def __str__(self):
        return self.employee.full_name


class Earnings(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.IntegerField()
    description = models.TextField()
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.full_name


class Deductions(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.IntegerField()
    description = models.TextField()
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.full_name
