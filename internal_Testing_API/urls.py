from django.urls import path
from . import views  

urlpatterns = [
    path('Testing-api/', views.run_multiple_apis_Test, name='Testing-api'),
]
