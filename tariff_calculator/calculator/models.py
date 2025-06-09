from django.db import models

class Tariff(models.Model):
    start_date = models.DateField(unique=True)
    end_date = models.DateField(unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

