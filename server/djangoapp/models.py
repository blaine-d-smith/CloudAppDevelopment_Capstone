from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    """
    Model for car make.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """
    Model for car model.
    """
    SEDAN = 'Sedan'
    SUV = 'SUV'
    TRUCK = 'Truck'
    WAGON = 'Wagon'
    MODEL_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (TRUCK, 'Truck'),
        (WAGON, 'Wagon')
    ]
    name = models.CharField(max_length=50)
    model_type = models.CharField(max_length=5, choices=MODEL_TYPES, default=SEDAN)
    year = models.DateField(null=True)
    dealerId = models.IntegerField()
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
