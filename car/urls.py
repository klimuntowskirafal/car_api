from django.urls import path
from .views import CarApi, CarApiDelete

urlpatterns = [
    path('cars/', CarApi.as_view(), name='cars'),
    path('cars/<id>/', CarApiDelete.as_view(), name='car-delete'),
]
