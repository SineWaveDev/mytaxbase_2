from django.urls import path
from .views import PortfolioChart

urlpatterns = [
    path('portfolio/', PortfolioChart.as_view(), name='portfolio'),
]
