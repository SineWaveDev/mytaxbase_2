from django.urls import path
from .views import StockDataView

urlpatterns = [
    path('dividend-data/', StockDataView.as_view(), name='dividend-data'),
]
