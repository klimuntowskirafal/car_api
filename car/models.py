from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=50, null=True, blank=False)
    model = models.CharField(max_length=50, null=True, blank=False)
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model} - {self.make}"

    class Meta:
        ordering = ['created']


class Rate(models.Model):
    rate_model = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rate_model} - {self.rating}"
