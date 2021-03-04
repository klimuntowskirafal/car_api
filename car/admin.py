from django.contrib import admin
from .models import Car, Rate


class CarAdmin(admin.ModelAdmin):
    list_display = [
        'make',
        'model',
        'avg_rating'
    ]
    list_filter = [
        'make',
        'model',
        'avg_rating',
    ]


class RateAdmin(admin.ModelAdmin):
    list_display = [
        'rate_model',
        'rating',
        'created'
    ]
    list_filter = [
        'rate_model',
        'rating',
        'created'
    ]


admin.site.register(Car, CarAdmin)
admin.site.register(Rate, RateAdmin)

