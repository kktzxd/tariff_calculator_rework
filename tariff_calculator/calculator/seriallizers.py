from django.core import serializers
import calculator.models as models
def tariff_serializer():
    tariffs = models.Tariff.objects.all()
    data = serializers.serialize('python', tariffs)
    tariffs = []
    for item in data:
        tariffs.append({
            "id": item["pk"],
            "start_date": item["fields"]["start_date"],
            "end_date": item["fields"]["end_date"],
            "cost": float(item["fields"]["cost"]),  # Decimal → float
        })
    
    return {"tariffs": tariffs}