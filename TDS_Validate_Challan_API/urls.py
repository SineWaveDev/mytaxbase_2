# myproject/urls.py

from django.urls import path
from .views import ChainAPIsView

urlpatterns = [
    path('chain-apis/', ChainAPIsView.as_view(), name='chain-apis')
]
