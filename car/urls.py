from django.urls import path
from .views import CarApiDelete, RateACar, car_api_main_page, car_api, car_popular

urlpatterns = [
    path('', car_api_main_page, name='car_api_main_page'),
    path('cars/', car_api, name='cars'),
    path('cars/<id>/', CarApiDelete.as_view(), name='car-delete'),
    path('rate/', RateACar.as_view(), name='rate-car'),
    path('popular/', car_popular, name='popular'),
]
