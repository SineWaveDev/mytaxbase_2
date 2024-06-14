from django.urls import path
from .views import DownloadZipView

urlpatterns = [
    path('download-zip/', DownloadZipView.as_view(), name='download-zip'),
]