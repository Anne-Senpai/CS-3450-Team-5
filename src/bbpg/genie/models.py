from django.db import models
from django.contrib.auth.models import User, Permission


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField()

    def is_manager(self):
        perm = Permission.objects.get(codename="is_manager")
        return perm in self.user.user_permissions.all()

    def is_supervisor(self):
        perm = Permission.objects.get(codename="is_supervisor")
        return perm in self.user.user_permissions.all()

    def is_attendant(self):
        perm = Permission.objects.get(codename="is_attendant")
        return perm in self.user.user_permissions.all()


class ParkingLot(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_types(self):
        types = []
        lot_areas = self.lotarea_set.all()
        for area in lot_areas:
            if area.type not in types:
                types.append(area.type)

        return types

    def get_num_spots(self):
        num_spots = 0
        lot_areas = self.lotarea_set.all()
        for area in lot_areas:
            num_spots += area.capacity

        return num_spots

    def num_spots_available(self, event):
        num_spots = 0
        lot_areas = self.lotarea_set.all()
        for area in lot_areas:
            num_spots += area.num_spots_available(event)

        return num_spots

class Event(models.Model):
    startTime = models.DateTimeField('Start Time')
    endTime = models.DateTimeField('End Time')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    parkingLots = models.ManyToManyField(ParkingLot)



class LotArea(models.Model):
    areaIdentifier = models.CharField(max_length=200)
    parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    price = models.FloatField()
    type = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def num_spots_available(self, event):
        reservations = self.reservation_set.filter(event=event)
        return self.capacity - len(reservations)

class Reservation(models.Model):
    code = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    lotArea = models.ForeignKey(LotArea, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

