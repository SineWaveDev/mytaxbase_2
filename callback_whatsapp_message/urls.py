from django.urls import path
from .views import SendCampaignAPIView, SendCampaignAPI2View

urlpatterns = [
    path('send-campaign/', SendCampaignAPIView.as_view(), name='send-campaign'),
    path('send-campaign2/', SendCampaignAPI2View.as_view(), name='send-campaign2'),
]
