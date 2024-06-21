from django.urls import path
from .views import event_report

urlpatterns = [
    path('reports/event/<int:event_id>/', event_report, name='event_report'),
]
