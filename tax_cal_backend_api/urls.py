# tax_api/urls.py
from django.urls import path
from .views import calculate_tax

urlpatterns = [
    path('calculate-tax/', calculate_tax, name='calculate-tax'),
    # Other URL patterns...
]
