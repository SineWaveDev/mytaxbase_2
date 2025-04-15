# webhook/urls.py
from django.urls import path
from .views import WebhookView, TriggerCampaignView

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('trigger-campaign/', TriggerCampaignView.as_view(), name='trigger-campaign'),
]