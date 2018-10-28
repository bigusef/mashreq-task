from django.urls import path

from .views import DashboardView, LoadExcelView, CreateEmployeeView, UpdateEmployeeView, DeleteEmployeeView

app_name = 'employee'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('add/', CreateEmployeeView.as_view(), name='add'),
    path('update/<int:pk>', UpdateEmployeeView.as_view(), name='update'),
    path('delete/<int:pk>', DeleteEmployeeView.as_view(), name='delete'),
    path('load-excel/', LoadExcelView.as_view(), name='load_excel'),
]
