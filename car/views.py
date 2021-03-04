import json

from django.core.serializers import serialize
from django.shortcuts import render
from .models import Car
from rest_framework import status
from rest_framework.views import APIView, Response

from .serializers import CarSerializer


class CarApi(APIView):

    # for form display on browsable API
    serializer_class = CarSerializer

    def get(self, request, *args, **kwargs):
        queryset = Car.objects.all()
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        # TO IMPLEMENT
        # add validation if make and model exist in api
        # here https://vpic.nhtsa.dot.gov/api/
        # If the car doesn't exist - return an error
        # If the car exists - it should be saved in the database

        # avg_rating can not be send via POST,
        # this will be calculated from Rates
        if request.data['avg_rating'] is None:
            serializer = CarSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
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



