

from django.urls import path
from .views import GeneratePortfolioReport

urlpatterns = [
    path('upload/', GeneratePortfolioReport.as_view(), name='file-upload'),
]