from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

app_name = 'employee'

urlpatterns = [
    path('', TemplateView.as_view(template_name='employee/dashboard.html'), name='dashboard')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
