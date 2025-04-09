from django.urls import path
from .views import InsertCallAPIView

urlpatterns = [
    path('insert-call/', InsertCallAPIView.as_view(), name='insert-call'),
]
