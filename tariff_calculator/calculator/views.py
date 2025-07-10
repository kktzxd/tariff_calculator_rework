from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from calculator.models import Tariff
from logging import log
from django.views.decorators.csrf import csrf_exempt
from utils.date_formetter import ru_to_ISO
import json
from decimal import Decimal
import calculator.seriallizers
from rest_framework.response import Response
#from calculator.calculator import calculator as calc
from calculator.calculator import calculator_month as calc2 #новая функция

# Create your views here.
def tariffs(request):
    # data = {
    # "tariffs": [
    #     {"id":1, "start_date":"01.01.2000", "end_date":"01.02.2000", "cost":50},
    #     {"id":2, "start_date":"05.02.2000", "end_date":"15.03.2000", "cost":75},
    # ]
    #}
    data = calculator.seriallizers.tariff_serializer()
    return render(request, "tariffs.html", data)
@csrf_exempt
def save_tariff(request:HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
        start_date = data["start_date"]
        start_date = ru_to_ISO(start_date)
        end_date = data["end_date"]
        end_date = ru_to_ISO(end_date)
        cost = data["cost"]
        cost = Decimal(cost)
        new_tarriff = Tariff(start_date=start_date, end_date=end_date, cost=cost)
        try:
            new_tarriff.save()
            return HttpResponse("OK")
        except Exception as e:
            print(e)
            return Response(status=404)
@csrf_exempt
def delete_tariff(request:HttpRequest, tariff_id:int):
    if request.method == "DELETE":
        tariff = Tariff.objects.get(id=tariff_id)
        if tariff:
            tariff.delete()
        return HttpResponse()

def calculator_view(request:HttpRequest):
    tariffs = calculator.seriallizers.tariff_serializer()
    return render(request, "calculator.html", tariffs)
def get_tarrifs(request:HttpRequest):
        tariffs = calculator.seriallizers.tariff_serializer()
        tariffs = json.loads(tariffs)
        return JsonResponse(tariffs)
@csrf_exempt
def get_payment_cost(request:HttpRequest):
    if request.method=="POST":
        data = json.loads(request.body)
        start_date = data["start_date"]
        end_date = data["end_date"]
        square = data["square"]
        #payment = calc(start_date, end_date, square)
        payment = calc2(start_date, end_date, square) #новая
        data = {"payment":payment}
        return JsonResponse(data)
