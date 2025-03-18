from django.urls import path
from .views import verify_otp_mis

urlpatterns = [
    path('Verify/', verify_otp_mis, name='Verify'),
]
