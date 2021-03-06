from django.contrib import admin
from .models import Car, Rate


class CarAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'make',
        'model',
        'created'
    ]
    list_filter = [
        'make',
        'model',
        'created'
    ]


class RateAdmin(admin.ModelAdmin):
    list_display = [
        'car',
        'rating',
        'created'
    ]
    list_filter = [
        'car',
        'rating',
        'created'
    ]


admin.site.register(Car, CarAdmin)
admin.site.register(Rate, RateAdmin)

