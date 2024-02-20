from django.urls import reverse, path
from rest_framework.test import APITestCase
from cars_api.models import *


class CarApiTestCase(APITestCase):
    def test_get(self):
        # url = path('api/cars/', CarApiList.as_view())
        # print(url)
        car_1 = Car.objectc.create(model="supra 1",
                                   description="supra 1",
                                   mileage=1,
                                   brand=2)
        response = self.client.get('/api/cars/')
        print(response)
