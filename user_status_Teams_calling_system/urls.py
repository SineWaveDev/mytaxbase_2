from django.urls import path
from .views import CallStatusAPIsView

urlpatterns = [
    path('CallStatusAPIsView/', CallStatusAPIsView.as_view(), name='CallStatusAPIsView'),
]
