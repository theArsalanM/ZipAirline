from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from calculator.models import Airplane


class AirplaneTests(APITestCase):
    def setUp(self):
        url = reverse('add_airplanes')
        data = [{"airplane_id": 1, "passengers_count": 30}, {"airplane_id": 2, "passengers_count": 50}]
        response = self.client.post(url, data, format='json')
        self.response = response

    def test_creation(self):
        """
        Ensure we can add data
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airplane.objects.count(), 2)

    def test_calculations(self):
        """Ensure calculations"""
        object_1 = Airplane.objects.get(airplane_id=1)
        response_1 = self.response.data[0]
        self.assertEqual(response_1['fuel_consumption_per_minute'], object_1.fuel_consumption_per_minute())
        self.assertEqual(response_1['total_flight_time_in_minutes'], object_1.total_flight_time_in_minutes())

        object_2 = Airplane.objects.get(airplane_id=2)
        response_2 = self.response.data[1]
        self.assertEqual(response_2['fuel_consumption_per_minute'], object_2.fuel_consumption_per_minute())
        self.assertEqual(response_2['total_flight_time_in_minutes'], object_2.total_flight_time_in_minutes())
