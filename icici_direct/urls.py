from django.urls import path
from .views import StartICICIDirectLogin, ProvideOTPICICIDirect

urlpatterns = [
    path('StartICICIDirectLogin/', StartICICIDirectLogin.as_view(), name='StartICICIDirectLogin'),
    path('ProvideOTPICICIDirect/', ProvideOTPICICIDirect.as_view(), name='ProvideOTPICICIDirect'),
]
