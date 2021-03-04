import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Car


class ApiFixture(TestCase):

    def set_up(self):
        Car.objects.create(make='Audi', model='A3')
        pass

    def test_get_cars_returns_success(self):
        c = Client()
        self.assertEqual(200, c.get("/cars/").status_code)

    def test_create_car_object(self):
        c = Client()
        data = {
            'make': 'Vw',
            'model': 'Golf',
        }
        response = c.post(reverse('cars'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(201, response.status_code)

    def test_post_avg_rating_returns_err(self):
        c = Client()
        data = {
            'make': 'Vw',
            'model': 'Golf',
            'avg_rating': '4.5',
        }
        response = c.post(reverse('cars'),
                          data,
                          content_type='application/json',
                          )
        self.assertEqual(400, response.status_code)

    # def test_delete_car_object(self):
    #     c = Client()
    #     car = Car.objects.filter(model='A3').get()
    #     # weryfikuj przy wykorzystaniu assert
    #     # SPRAWDZ CZY POWSTAL CAR OBJ
    #     url = f'/cars/{car.id}/'
    #     response_delete = c.delete(url)
    #     self.assertEqual(204, response_delete.status_code)


