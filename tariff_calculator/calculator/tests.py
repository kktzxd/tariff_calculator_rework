from django.test import TestCase
import unittest
from decimal import Decimal
from calculator.models import Tariff
from utils.date_formetter import ru_to_ISO
from datetime import timedelta
from math import ceil
from utils.timeit import timeit
from calculator.calculator import calculator, calculator_month
import calendar #для calculator_month
class DateFilterTest(TestCase):

    def setUp(self):
        # Данные будут доступны во всех тестах
        self.start_dates = ["10.10.2020", "10.11.2020", "01.01.2021", "01.05.2021"]
        self.end_dates = ["09.11.2020", "31.12.2020", '30.04.2021', "31.12.2021"]
        self.costs = [100, 150, 160, 170]

        # Создаём тарифы
        for start, end, cost in zip(
            map(ru_to_ISO, self.start_dates),
            map(ru_to_ISO, self.end_dates),
            self.costs
        ):
            Tariff.objects.create(start_date=start, end_date=end, cost=cost)

    def test_get_date(self):
        start_dates = ["10.10.2020", "10.11.2020", "01.01.2021", "01.05.2021"]
        start_dates = map(ru_to_ISO, start_dates)
        for start_date in start_dates:
            tariff = Tariff.objects.get(start_date=start_date)
            self.assertIsNotNone(tariff)
            print(tariff)
    def test_filter_date(self):
        start_date = "10.10.2020"
        end_date = "10.01.2021"
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        filter_tariffs = Tariff.objects.filter(start_date__lte=start_date, end_date__gte=end_date)
        all_tarrifs = Tariff.objects.all()
        # self.assertTrue(len(all_tarrifs)!=0)
        # self.assertEqual(len(filter_tariffs), 2)

    def test_calculate_month(self):
        start_date = "10.10.2020"
        end_date = "09.11.2020"
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        filter_tariffs = Tariff.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
        print("Платежи за месяц")
        result = 0
        for tariff in filter_tariffs:
            print(tariff.start_date, tariff.end_date)
            cost_per_day = tariff.cost/30
            cur_date = tariff.start_date
            while cur_date < tariff.end_date:
                result += cost_per_day
                cur_date+=timedelta(days=1)
        result = ceil(result)
        print(result)
    def test_calculate_all_period(self):
        start_date = "10.10.2020"
        end_date = "31.12.2021"
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        filter_tariffs = Tariff.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
        print("Платежи за все время")
        result = 0
        for tariff in filter_tariffs:
            print(tariff.start_date, tariff.end_date)
            cost_per_day = tariff.cost/30
            cur_date = tariff.start_date
            while cur_date <= tariff.end_date:
                result += cost_per_day
                cur_date+=timedelta(days=1)
        result = ceil(result)
        print(result)
    def test_get_total_days(self):
        date_set = set()
        tariffs = Tariff.objects.all()
        for tariff in tariffs:
            start = tariff.start_date
            end = tariff.end_date
            cur = start
            while cur <= end:
                date_set.add(cur)
                cur+=timedelta(days=1)
        self.assertEqual(len(date_set), 448)
    @timeit
    def test_calculate_payment(self):
        start_date = "10.10.2020"
        end_date = "20.10.2020"
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        tariffs = list(Tariff.objects.filter(start_date__lte=start_date, end_date__gte=end_date))
        cur_date = start_date
        result = 0
        while cur_date<=end_date:
            cost_per_day = None
            for tariff in tariffs:
                if tariff.start_date <= cur_date <= tariff.end_date:
                    cost_per_day = tariff.cost/30
                    break
            self.assertIsNotNone(cost_per_day)
            result+=cost_per_day
            cur_date += timedelta(days=1)
        print("За 10 дней", result)
        self.assertTrue(36<=result<=37)
    @timeit
    def test_big_data(self):
        start_date = "10.10.2020"
        end_date = "20.10.2020"
        square = 100
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        cur_date = start_date
        tariffs = Tariff.objects.all()
        result = 0
        while cur_date < end_date:
            cost_per_day = None
            for tariff in tariffs:
                 if tariff.start_date <= cur_date <= tariff.end_date:
                    cost_per_day = tariff.cost/30
                    break
            cur_date+=timedelta(days=1)
            result+=cost_per_day
        result*=square
    def test_compare_code(self):
        start_date = "10.10.2020"
        end_date = "20.10.2020"
        square = 100
        compare_result = calculator(start_date, end_date, square)
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        cur_date = start_date
        tariffs = Tariff.objects.all()
        result = 0
        while cur_date < end_date:
            cost_per_day = None
            for tariff in tariffs:
                 if tariff.start_date <= cur_date <= tariff.end_date:
                    cost_per_day = tariff.cost/30
                    break
            cur_date+=timedelta(days=1)
            result+=cost_per_day
        result*=square
        self.assertEqual(result,compare_result)
        
    #новый тест
    def test_compare_code_month(self):
        start_date = "10.11.2020"
        end_date = "20.01.2021"
        square = 100
        compare_result = calculator_month(start_date, end_date, square)
        start_date = ru_to_ISO(start_date)
        end_date = ru_to_ISO(end_date)
        cur_date = start_date
        tariffs = Tariff.objects.all()
        result = 0
        while cur_date <= end_date:
            cost_per_day = None
            days_in_month = calendar.monthrange(cur_date.year, cur_date.month)[1]
            for tariff in tariffs:
                if tariff.start_date <= cur_date <= tariff.end_date:
                    cost_per_day = tariff.cost / days_in_month
                    break
            cur_date += timedelta(days=1)
            result += cost_per_day
        result *= square
        result = round(result, 2)
        result = float(result)
        print(f"[DEBUG] Результат вручную: {result} ({type(result)})")
        print(f"[DEBUG] Результат calculator_month: {compare_result} ({type(compare_result)})")
        self.assertEqual(result, compare_result)