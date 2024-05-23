from django.urls import path
from .views import GenerateJSONView

urlpatterns = [
    path('Json/', GenerateJSONView.as_view(), name='Json'),
]
