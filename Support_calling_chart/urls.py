from django.urls import path
from .views import Supportcallingchart

urlpatterns = [
    path('chart/', Supportcallingchart.as_view(), name='chart'),
]
