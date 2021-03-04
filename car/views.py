import json

import requests
from django.core.serializers import serialize
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Car, Rate
from rest_framework import status
from rest_framework.views import APIView, Response

from .serializers import CarSerializer


class CarApi(APIView):

    # for form display on browsable API
    serializer_class = CarSerializer

    def get(self, request, *args, **kwargs):

        cars = []
        car_set = Car.objects.all()
        for car in car_set:
            data = {}
            avg_rating = Rate.objects.filter(car=car).aggregate(avg_rating=Avg('rating'))
            data['id'] = car.id
            data['make'] = car.make
            data['model'] = car.model
            data.update(avg_rating)
            cars.append(data)

        return JsonResponse(cars, json_dumps_params={'indent': 2}, safe=False)

    def post(self, request, *args, **kwargs):

        # check if make and model only are in request
        try:
            request.data['make']
            request.data['model']
            # avg_rating can not be send via POST,
            # this will be calculated from Rates
            if request.data.get("avg_rating") is not None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CarApiDelete(APIView):

    def delete(self, request, id):
        car_id = id
        queryset = Car.objects.get(id=car_id)
        if queryset:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RateACar(APIView):

    def post(self, request):
        data = {
            "car_id" : 1,
            "rating" : 5,
        }
        pass


class CarPopularity(APIView):

    def get(self, request):
        # Response:
        # [
        #
        #     {
        #
        #         "id": 1,
        #
        #         "make": "Volkswagen",
        #
        #         "model": "Golf",
        #
        #         "rates_number": 100,
        #
        #     },
        # ]
        pass



