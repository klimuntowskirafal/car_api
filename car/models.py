from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Car(models.Model):
    """
    make is limited and short set of records
    in other case make and model could be separate models
    """
    make = models.CharField(max_length=50, null=True, blank=False)
    model = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} - {self.model}"

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        self.make = self.make.title()
        self.model = self.model.title()

        super(Car, self).save(*args, **kwargs)


class Rate(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.rating}"
