from django.urls import path
from .views import CarApi, CarApiDelete, RateACar, CarPopularity, car_api_main_page

urlpatterns = [
    path('', car_api_main_page, name='car_api_main_page'),
    path('cars/', CarApi.as_view(), name='cars'),
    path('cars/<id>/', CarApiDelete.as_view(), name='car-delete'),
    path('rate/', RateACar.as_view(), name='rate-car'),
    path('popular/', CarPopularity.as_view(), name='popular')
]
