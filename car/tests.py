import json

import requests
from django.test import TestCase, Client
from django.urls import reverse

from .models import Car


class ApiFixture(TestCase):

    def setUp(self):
        Car.objects.create(make='Audi', model='A3')
        Car.objects.create(make='Audi', model='A5')
        pass

    def test_api_returns_cars_on_get_request(self):
        c = Client()
        self.assertEqual(200, c.get("/cars/").status_code)

    def test_api_returns_success_when_make_and_model_in_body_post_request(self):
        c = Client()
        data = {
            'make': 'Volkswagen',
            'model': 'Golf',
        }
        response = c.post(reverse('cars'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(201, response.status_code)

    def test_api_returns_error_because_of_the_missing_make_entry_in_json(self):
        c = Client()
        data = {
            'model': 'Golf',
        }
        response = c.post(reverse('cars'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(400, response.status_code)

    def test_api_returns_error_because_of_the_missing_model_entry_in_json(self):
        c = Client()
        data = {
            'make': 'Volkswagen',
        }
        response = c.post(reverse('cars'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(400, response.status_code)

    def test_api_returns_error_because_of_extra_key_and_value_pairs_in_json(self):
        c = Client()
        data = {
            'make': 'Volkswagen',
            'model': 'Golf',
            'avg_rating': '4.5',
        }
        response = c.post(reverse('cars'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(400, response.status_code)

    def test_status_code_from_third_party_api(self):
        make = 'Audi'
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json'
        response = requests.get(url)
        self.assertEqual(200, response.status_code)

    def test_delete_car_object(self):
        c = Client()
        car = Car.objects.get(model='A3')
        url = f'/cars/{car.id}/'
        response_delete = c.delete(url)
        self.assertEqual(204, response_delete.status_code)

    def test_delete_car_that_does_not_exist_return_error(self):
        c = Client()
        url = f'/cars/99/'
        response_delete = c.delete(url)
        self.assertEqual(404, response_delete.status_code)

    def test_add_rate_to_a_car(self):
        data = {
            "car_id": 1,
            "rating": 5
        }
        c = Client()
        response = c.post(reverse('rate-car'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(201, response.status_code)

    def test_post_decimal_rating_return_error(self):
        data = {
            "car_id": 1,
            "rating": 2.5
        }
        c = Client()
        response = c.post(reverse('rate-car'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(400, response.status_code)

    def test_api_returns_popular_rated_cars_on_get_request(self):
        c = Client()
        self.assertEqual(200, c.get("/popular/").status_code)

