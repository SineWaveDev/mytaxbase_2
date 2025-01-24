from django.urls import path
from .views import StartangleLogin, ProvideOTPAngle, DownloadFile

urlpatterns = [
    path('DownloadangeloneReport/', StartangleLogin.as_view(), name='DownloadangeloneReport'),
    path('ProvideOTPAngle/', ProvideOTPAngle.as_view(), name='ProvideOTPAngle'),
    path("download-files/", DownloadFile.as_view(), name="download_files"),  # New endpoint for downloading files
]
