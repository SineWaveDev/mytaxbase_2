
from .views import get_otp, verify_otp
from django.urls import path

urlpatterns = [
    path('get_otp', get_otp, name='get_otp'),
    path('verify_otp', verify_otp, name='verify_otp'),

]
