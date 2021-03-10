from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField()


class ParkingLot(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Event(models.Model):
    startTime = models.DateTimeField('Start Time')
    endTime = models.DateTimeField('End Time')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    parkingLots = models.ManyToManyField(ParkingLot)


class ParkingSpot(models.Model):
    parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    price = models.FloatField()
    type = models.CharField(max_length=200)


class Reservation(models.Model):
    code = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    parkingSpot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

