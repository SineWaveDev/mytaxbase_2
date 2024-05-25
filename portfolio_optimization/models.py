# models.py
from django.db import models

class PortfolioPerformance(models.Model):
    ticker = models.CharField(max_length=20)
    weight = models.FloatField()
    expected_return = models.FloatField()
    volatility = models.FloatField()
    sharpe_ratio = models.FloatField()
    risk_free_rate = models.FloatField()
