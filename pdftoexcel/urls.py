from django.urls import path
from pdftoexcel import views

urlpatterns = [
    path('process-files/', views.process_files, name='process_files'),
]
