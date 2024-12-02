from django.urls import path
from .views import StartKiteLogin, ProvideOTPZerodhaKite

urlpatterns = [
    path('StartKiteLogin/', StartKiteLogin.as_view(), name='StartKiteLogin'),
    path('ProvideOTPZerodhaKite/', ProvideOTPZerodhaKite.as_view(), name='ProvideOTPZerodhaKite'),
]
