from django.db import models

class Tariff(models.Model):
    start_date = models.DateTimeField(unique=True)
    end_date = models.DateTimeField(unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

