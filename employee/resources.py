from import_export.resources import ModelResource
from .models import Employee


class EmployeeResource(ModelResource):
    class Meta:
        model = Employee
