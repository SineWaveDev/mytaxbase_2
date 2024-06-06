from django.urls import path
from .views import SendCampaignAPIView

urlpatterns = [
    path('send-campaign/', SendCampaignAPIView.as_view(), name='send-campaign'),
]
