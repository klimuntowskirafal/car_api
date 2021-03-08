import logging
import requests
from django.db.models import Avg
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from .models import Car, Rate
from .serializers import CarSerializer

logger = logging.getLogger(__name__)


def get_all_cars_with_calculated_avg_rating():
    cars = []
    car_set = Car.objects.all()

    for car in car_set:
        data = {}
        avg_rating = Rate.objects.filter(car=car).\
            aggregate(avg_rating=Avg('rating'))
        # rounding avg value to 2 decimal places
        if avg_rating['avg_rating'] is not None:
            number = avg_rating['avg_rating']
            avg_rating['avg_rating'] = round(number, 2)
        data = {
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'avg_rating': avg_rating['avg_rating']
        }
        cars.append(data)
    return cars


def add_new_car_if_found_in_external_api(request):
    expected_request_parameters = 2
    try:
        # validate number of parameters in POST body request
        # only 'make' and 'model' can be in a request body
        if len(request.data) != expected_request_parameters:
            logger.warning(
                f"Wrong key:value pairs in request body '{request.data}'")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        make = request.data['make']
        model = request.data['model']

        if car_exist_in_external_api(make=make, model=model):
            serializer = CarSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                logger.warning(
                    f"request serialization problem '{request.data}'")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.warning(f"car not found in external API {make} {model}")
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except KeyError as e:
        logger.warning(f"invalid request data: {e}")
        return Response(status=status.HTTP_400_BAD_REQUEST)


def car_exist_in_external_api(make, model):
    """
    checks car existance in 3rd party api
    """
    make = make
    model = model

    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json'
    try:
        response = requests.get(url).json()
    except Exception as e:
        # log warning and error
        logger.error(f"3rd party request error: {e}")
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # find model in api
    results = list(
        filter(
            lambda x: x.get(
                "Model_Name",
                "") == model,
            response['Results']))

    return len(results) > 0


def get_car_object(car_id, class_name):
    try:
        return Car.objects.get(id=car_id)
    except Car.DoesNotExist as e:
        logger.error(f"requested car does not exists: {e} - from {class_name}")
        raise Http404
