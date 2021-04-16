from django.contrib.auth.models import AbstractUser
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False, blank=False, related_name="cities")

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class User(AbstractUser):
    gender = models.CharField(null=True, blank=False, max_length=128, choices=[("male", "male"), ("female", "female"), ("other", "other")])
    age = models.IntegerField(null=True, blank=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class Sale(models.Model):
    product = models.CharField(max_length=256, blank=True, null=True)
    sales_number = models.IntegerField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="sales")
