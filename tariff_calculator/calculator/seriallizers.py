from django.core import serializers
import calculator.models as models
from datetime import date
def tariff_serializer():
    tariffs = models.Tariff.objects.all().order_by('pk')
    data = serializers.serialize('python', tariffs)
    tariffs = []
    for item in data:
        tariffs.append({
            "id": item["pk"],
            "start_date": item["fields"]["start_date"].strftime("%d.%m.%y"),
            "end_date": item["fields"]["end_date"].strftime("%d.%m.%y"),
            "cost": float(item["fields"]["cost"]),  # Decimal → float
        })
    
    return {"tariffs": tariffs}