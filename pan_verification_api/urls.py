from django.urls import path
from .views import check_pan_details

urlpatterns = [
    path('check-pan/', check_pan_details, name='check_pan_details'),
]