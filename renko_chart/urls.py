from django.urls import path
from .views import Renko_Chart

urlpatterns = [
    path('renko/', Renko_Chart.as_view(), name='Renko_Chart'),
]
