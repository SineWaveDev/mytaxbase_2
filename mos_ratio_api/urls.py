from django.urls import path
from .views import StockDataAPIView

urlpatterns = [
    path('get-stock-data/', StockDataAPIView.as_view(), name='get_stock_data'),
]
