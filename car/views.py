from django.db.models import Count
from django.http import JsonResponse
from .models import Car, Rate
from rest_framework import status
from rest_framework.views import APIView, Response

from .methods import get_all_cars_with_calculated_avg_rating, \
    add_new_car_if_found_in_external_api, get_car_object, logger


class CarApi(APIView):

    def get(self, request):
        return get_all_cars_with_calculated_avg_rating()

    def post(self, request):
        return add_new_car_if_found_in_external_api(self, request)


class CarApiDelete(APIView):

    def delete(self, request, id):
        car = get_car_object(id, type(self).__name__)
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
            # if not
            if isinstance(rating, float):
                logger.warning(
                    f"rating value must be an integer: {request.data}")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            car = get_car_object(car_id=car_id, class_name=type(self).__name__)
            instance = Rate(car=car, rating=rating)
            instance.save()
            return Response(status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.warning(f"rating value must be an integer: {request.data}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            logger.warning(f"invalid request data: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CarPopularity(APIView):

    def get(self, request):
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

        return JsonResponse(popular_cars,
                            json_dumps_params={'indent': 2},
                            safe=False)
