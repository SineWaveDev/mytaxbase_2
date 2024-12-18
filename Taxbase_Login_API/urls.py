from django.urls import path
from . import views  

urlpatterns = [
    path('run-multiple-apis/', views.run_multiple_apis, name='run_multiple_apis'),
]
