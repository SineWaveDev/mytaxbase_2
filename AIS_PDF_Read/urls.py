from django.urls import path
from .views import PDFToJsonView

urlpatterns = [
    path('pdf-to-json/', PDFToJsonView.as_view(), name='pdf_to_json'),
]
