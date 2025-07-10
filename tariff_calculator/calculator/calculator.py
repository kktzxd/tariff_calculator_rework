from datetime import datetime, timedelta
from decimal import Decimal
from calculator.models import Tariff
from utils.date_formetter import ru_to_ISO
import calendar

def calculator(start_date:str, end_date:str, square:str):
    tariffs = Tariff.objects.all()
    start_date = ru_to_ISO(start_date)
    end_date = ru_to_ISO(end_date)
    square = Decimal(square)
    payment = 0
    cur_date = start_date
    delta_day = timedelta(days=1)
    while cur_date <= end_date:
        cost_per_day = 0
        for tariff in tariffs:
                if tariff.start_date <= cur_date <= tariff.end_date:
                    cost_per_day = tariff.cost/30
                    break
        cur_date+=delta_day
        payment+=cost_per_day

    payment*=square
    payment = round(payment,2)
    payment = float(payment)
    return payment

#новая
def calculator_month(start_date:str, end_date:str, square:str):
    tariffs = Tariff.objects.all()
    start_date = ru_to_ISO(start_date)
    end_date = ru_to_ISO(end_date)
    square = Decimal(square)
    payment = 0
    cur_date = start_date
    delta_day = timedelta(days=1)
    prev_month = None
    while cur_date <= end_date:
        cost_per_day = 0
        days_in_this_month = calendar.monthrange(cur_date.year, cur_date.month)[1] #функция вовзращает день недели первого числа месяца и кол-во дней в месяце(беру это)
        for tariff in tariffs:
                if tariff.start_date <= cur_date <= tariff.end_date:
                    cost_per_day = tariff.cost/days_in_this_month #заменил 30 на точное число дней в месяце
                    if prev_month != (cur_date.year, cur_date.month):
                        print(f"{cur_date.strftime('%Y-%m')} — тариф: {tariff.cost}")
                        prev_month = (cur_date.year, cur_date.month)
                    break
        cur_date+=delta_day
        payment+=cost_per_day

    payment*=square
    payment = round(payment,2)
    payment = float(payment)
    return payment