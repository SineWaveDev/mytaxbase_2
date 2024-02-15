from django.urls import path
from .views import TechnicalAnalysis

urlpatterns = [
    path('stock-data/', TechnicalAnalysis.as_view(), name='stock-data-list'),
]
