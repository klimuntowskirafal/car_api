from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import render

from .models import Car, Rate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response

from .methods import get_all_cars_with_calculated_avg_rating, \
    add_new_car_if_found_in_external_api, get_car_object, logger


def car_api_main_page(request):
    if request.method == "GET":
        return render(request, "car_api_introduction.html")


@api_view(['GET', 'POST'])
def car_api(request):
    if request.method == 'GET':
        cars = get_all_cars_with_calculated_avg_rating()
        return Response(cars, status=status.HTTP_200_OK)

    if request.method == 'POST':
        return add_new_car_if_found_in_external_api(request)


class CarApiDelete(APIView):

    def delete(self, request, id):
        car = get_car_object(id, class_name='CarApiDelete')
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RateACar(APIView):

    def post(self, request):
        expected_request_parameters = 2
        try:
            # valide only two parameters are send to the endpoint
            if len(request.data) != expected_request_parameters:
                logger.warning(
                    f"Wrong key:value pairs in request body '{request.data}'")
                return Response(status=status.HTTP_400_BAD_REQUEST)

            car_id = request.data["car_id"]
            rating = request.data["rating"]

            # validate if passed request rating is integer, return ValueError
            if not isinstance(rating, int):
                logger.warning(
                    f"rating value must be an integer: {request.data}")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            car = get_car_object(car_id=car_id, class_name='RateACar')
            instance = Rate(car=car, rating=rating)
            instance.save()
            return Response(status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.warning(f"rating value must be an integer: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            logger.warning(f"invalid request data: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def car_popular(request):
    popular_cars = []
    cars = Car.objects.annotate(
        num_rate=Count('rate')).order_by('-num_rate')
    for car in cars:
        data = {
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'rates_number': car.num_rate
        }
        popular_cars.append(data)
    return Response(popular_cars, status=status.HTTP_200_OK)
