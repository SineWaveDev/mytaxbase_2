from django.urls import path
from .views import StartangleLogin, ProvideOTPAngle

urlpatterns = [
    path('DownloadangeloneReport/', StartangleLogin.as_view(), name='DownloadangeloneReport'),
    path('ProvideOTPAngle/', ProvideOTPAngle.as_view(), name='ProvideOTPAngle'),
]
