from django.urls import path
from .views import ClientAPI, VerifyOtpAPI

urlpatterns = [
    path('generate-otp/', ClientAPI.as_view(), name='client_api'),
    path('verify-otp/', VerifyOtpAPI.as_view(), name='verify_otp'),
]
