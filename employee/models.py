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
