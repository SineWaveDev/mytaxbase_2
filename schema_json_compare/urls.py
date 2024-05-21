from django.urls import path
from .views import validate_json

urlpatterns = [
    path('validate-json/', validate_json, name='validate_json'),
]