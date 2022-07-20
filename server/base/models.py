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


class CarDealer:
    """
    Data object for car dealer.
    """
    def __init__(self, id, full_name, address, city, st, state, zip, lat, long, short_name):
        self.id = id
        self.full_name = full_name
        self.address = address
        self.city = city
        self.st = st
        self.state = state
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    """
    Data object for dealer review.
    """
    def __init__(self, dealership, name, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        # self.id = id
        self.dealership = dealership
        self.name = name
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review
