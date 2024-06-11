from django.urls import path
from .views import calculate_tax

urlpatterns = [
    path('combined-api/', calculate_tax, name='combined-api'),
]
