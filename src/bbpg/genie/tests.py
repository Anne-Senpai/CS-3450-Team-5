import datetime

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from genie.models import Event, Reservation, ParkingLot, LotArea, Profile
from django.contrib.auth.models import User, Permission

class unittest(TestCase):
    def __init__(self, *args, **kwargs):
        super(unittest, self).__init__(*args, **kwargs)
        self.user = User.objects.get(username="manager.user")

        self.parkingLot = ParkingLot(owner=self.user, name="Arthur's Kingdom", address="123 Arthur Street")
        self.parkingLot.save()
        self.start = datetime.datetime.now()
        self.end = datetime.datetime.now()

        self.event = Event(startTime=self.start, endTime=self.end, name="Tuna Fish", description="Eat Yummy Dinner!!",
                      address="123 Arthur Street")
        self.event.save()


        self.lotArea = LotArea(areaIdentifier="Area 51", parkingLot=self.parkingLot, price="Your left kidney", type="Regular",
                          capacity="1")

    def testLot(self):
        self.assertTrue(self.parkingLot != None)
        self.assertEqual(self.parkingLot.owner, self.user)
        self.assertEqual(self.parkingLot.name, "Arthur's Kingdom")
        self.assertEqual(self.parkingLot.address, "123 Arthur Street")


    def testEvent(self):
        self.assertTrue(self.event != None)
        self.assertEqual(self.event.startTime, self.start)
        self.assertEqual(self.event.endTime, self.end)
        self.assertEqual(self.event.name, "Tuna Fish")
        self.assertEqual(self.event.description, "Eat Yummy Dinner!!")
        self.assertEqual(self.event.address, "123 Arthur Street")


    def testLotArea(self):
        self.assertTrue(self.lotArea != None)
        self.assertEqual(self.lotArea.areaIdentifier, "Area 51")
        self.assertEqual(self.lotArea.parkingLot, self.parkingLot)
        self.assertEqual(self.lotArea.price, "Your left kidney")
        self.assertEqual(self.lotArea.type, "Regular")
        self.assertEqual(self.lotArea.capacity, "1")




