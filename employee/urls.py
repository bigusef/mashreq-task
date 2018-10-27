from django.urls import path

from .views import DashboardView, LoadExcelView

app_name = 'employee'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('load-excel/', LoadExcelView.as_view(), name='load_excel'),
]
