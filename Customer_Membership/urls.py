# urls.py
from django.urls import path
from .views import check_customer_age

urlpatterns = [
    path('check_customer_age/', check_customer_age, name='check_customer_age'),
]
