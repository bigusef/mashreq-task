from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    main_salary = forms.IntegerField()

    class Meta:
        model = Employee
        fields = '__all__'

    def clean_main_salary(self):
        self.instance.main_salary = self.cleaned_data['main_salary']
