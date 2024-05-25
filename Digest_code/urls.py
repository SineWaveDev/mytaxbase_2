
from django.urls import path
from .views import generate_digest

urlpatterns = [
    path('digest/', generate_digest, name='digest'),
    # path('generate-hash/', generate_hash, name='generate-hash'),
]