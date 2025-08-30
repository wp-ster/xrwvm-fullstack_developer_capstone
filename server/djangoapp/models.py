from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


# CarMake model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # You can add other fields here if needed

    def __str__(self):
        return self.name


# CarModel model
class CarModel(models.Model):
    # Many-To-One relationship to CarMake (One CarMake has many CarModels)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
        ('Pickup', 'Pickup'),
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)

    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )

    dealer_id = models.IntegerField()

    # Add other fields if needed

    def __str__(self):
        return f"{self.car_make.name} {self.name}"
