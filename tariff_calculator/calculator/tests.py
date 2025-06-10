from django.test import TestCase
import unittest
from calculator.models import Tariff
from utils.date_formetter import ru_to_ISO
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
        filter_tariffs = Tariff.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
        all_tarrifs = Tariff.objects.all()
        self.assertTrue(len(all_tarrifs)!=0)
        self.assertEqual(len(filter_tariffs), 2)