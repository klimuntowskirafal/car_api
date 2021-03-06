from django.urls import path
from .views import CarApi, CarApiDelete, RateACar, CarPopularity

urlpatterns = [
    path('cars/', CarApi.as_view(), name='cars'),
    path('cars/<id>/', CarApiDelete.as_view(), name='car-delete'),
    path('rate/', RateACar.as_view(), name='rate-car'),
    path('popular/', CarPopularity.as_view(), name='popular')
]
