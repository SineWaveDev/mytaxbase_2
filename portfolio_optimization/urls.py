# urls.py
from django.urls import path
from .views import calculate_portfolio_performance

urlpatterns = [
    path('portfolio/performance/', calculate_portfolio_performance, name='portfolio_performance'),
]
