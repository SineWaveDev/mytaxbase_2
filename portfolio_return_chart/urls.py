
from django.urls import path
from .views import GeneratePortfolioReportChart

urlpatterns = [
    path('upload_chart/', GeneratePortfolioReportChart.as_view(), name='file-upload'),
]