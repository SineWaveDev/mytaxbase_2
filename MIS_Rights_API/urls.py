from django.urls import path
from .views import CheckDeptLevelAPI

urlpatterns = [
    path('check/', CheckDeptLevelAPI.as_view(), name='check-dept-level'),
]
