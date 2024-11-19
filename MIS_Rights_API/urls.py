from django.urls import path
from .views import ConditionEvaluatorView

urlpatterns = [
    path('check/', ConditionEvaluatorView.as_view(), name='check-dept-level'),
]
