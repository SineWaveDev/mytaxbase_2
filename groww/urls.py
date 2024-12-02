from django.urls import path
from .views import StartGrowwLogin, ProvideOTP

urlpatterns = [
    path('capital-gain-report/', StartGrowwLogin.as_view(), name='capital-gain-report'),
    path('ProvideOTP/', ProvideOTP.as_view(), name='ProvideOTP'),
    

]
