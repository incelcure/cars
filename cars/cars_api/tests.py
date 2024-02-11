from django.test import TestCase
from .models import *
from django.test import Client


c = Client()


class AuthTest(TestCase):

    def setUp(self):
        Car.objects.create(name="lion", sound="roar")
        Car.objects.create(name="cat", sound="meow")

    def test_auth_login(self):
        c = Client()
        response = c.post("/api/login/", {"username": "Alice", "password": "Alice_pass"})


        # response = c.post("/api/login/", {"username": "root", "password": "Alice_pass"})

        self.assertTrue(response.body.decode("json").__contains__("Bearer"), "should contains bearer token")


# c = Client()
# response = c.post("/login/", {"username": "john", "password": "smith"})
# response.status_code
# response = c.get("/customer/details/")
# response.content
