import datetime

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.models import Event, Reservation, ParkingLot, LotArea, Profile
from django.contrib.auth.models import User, Permission

arthur = User.objects.create_user(first_name="Arthur", last_name="Pendragon", password="tuna",
                                  username="sir.arthur")
arthur.save()

parkingLot = ParkingLot(owner=arthur, name="Arthur's Kingdom", address="123 Arthur Street")

start = datetime.datetime.now()
end = datetime.datetime.now()

event = Event(startTime=start, endTime=end, name="Tuna Fish", description="Eat Yummy Dinner!!", address="123 Arthur Street", parkingLots=parkingLot)

lotArea = LotArea(areaIdentifier="Area 51", parkingLot=parkingLot, price="Your left kidney", type="Regular", capacity="1")
class unittest(TestCase):


    def testLot(self):
        self.assertTrue(parkingLot != None)
        self.assertEqual(parkingLot.owner, arthur)
        self.assertEqual(parkingLot.name, "Arthur's Kingdom")
        self.assertEqual(parkingLot.address, "123 Arthur Street")


    def testEvent(self):
        self.assertTrue(event != None)
        self.assertEqual(parkingLot.startTime, start)
        self.assertEqual(parkingLot.endTime, end)
        self.assertEqual(parkingLot.name, "Tuna Fish")
        self.assertEqual(parkingLot.description, "Eat Yummy Dinner!!")
        self.assertEqual(parkingLot.address, "123 Arthur Street")
        self.assertEqual(parkingLot.parkingLots, parkingLot)

    def testLotArea(self):
        self.assertTrue(lotArea != None)
        self.assertEqual(lotArea.areaIdentifier, "Area 51")
        self.assertEqual(lotArea.parkingLot, parkingLot)
        self.assertEqual(lotArea.price, "Your left kidney")
        self.assertEqual(lotArea.type, "Regular")
        self.assertEqual(lotArea.capacity, "1")




