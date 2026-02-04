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
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
@login_required(login_url="login")
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
        cost = cost.replace(",", ".")
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
@swagger_auto_schema(
        method='post',
        operation_description='расчет платежа по тарифу за период',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['start_date', 'end_date', 'square'],
            properties={
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Дата начала периода', example='01.01.2020'),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Дата окончания периода', example='31.01.2020'),
                'square': openapi.Schema(type=openapi.TYPE_NUMBER, description='Площадь помещения', example=36.5),
            },
        ),
        responses={
            200: openapi.Response(description="Расчёт выполнен", schema=openapi.Schema(type=openapi.TYPE_NUMBER, example={'payment':500, "start_date":'01.01.2020','end_date':'31.01.2020'}))
        }
)
@csrf_exempt
@api_view(['POST'])
def get_payment_cost(request:HttpRequest):
    if request.method=="POST":
        data = json.loads(request.body)
        start_date = data["start_date"]
        end_date = data["end_date"]
        square = data["square"]
        #payment = calc(start_date, end_date, square)
        payment = calc2(start_date, end_date, square) #новая
        data = {"payment":payment, 'start_date':start_date, "end_date":end_date}
        return JsonResponse(data)
