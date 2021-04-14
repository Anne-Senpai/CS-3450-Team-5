from django.test import TestCase
from genie.models import Event, Reservation, ParkingLot, LotArea, Profile
from django.contrib.auth.models import User, Permission

parkingLot = ParkingLot(name="Arthur's Kingdom", address="123 Arthur Street", )

class unittest(TestCase):

    def testLot(self):
        parkingLot = ParkingLot()
        parkingLot.owner = "Arthur"
        parkingLot.name = "Arthur's Kingdom"
        parkingLot.address = "123 Arthur Street"

        self.assertTrue(parkingLot != None)
        self.assertEqual(parkingLot.owner, "Arthur")
        self.assertEqual(parkingLot.name, "Arthur's Kingdom")
        self.assertEqual(parkingLot.address, "123 Arthur Street")


    def testEvent(self):
        parkingLot = ParkingLot()
        parkingLot.owner = "Arthur"
        parkingLot.name = "Arthur's Kingdom"
        parkingLot.address = "123 Arthur Street"

        event = Event()
        event.startTime = "1:00 p.m."
        event.endTime = "1:01 p.m."
        event.name = "Tuna Fish"
        event.description = "Eat Yummy Dinner!!"
        event.address = "123 Arthur Street"
        event.parkingLots = parkingLot

        self.assertTrue(event != None)
        self.assertEqual(parkingLot.startTime, "1:00 p.m.")
        self.assertEqual(parkingLot.endTime, "1:01 p.m.")
        self.assertEqual(parkingLot.name, "Tuna Fish")
        self.assertEqual(parkingLot.description, "Eat Yummy Dinner!!")
        self.assertEqual(parkingLot.address, "123 Arthur Street")
        self.assertEqual(parkingLot.parkingLots, parkingLot)

    def testLotArea(self):
        parkingLot = ParkingLot()
        parkingLot.owner = "Arthur"
        parkingLot.name = "Arthur's Kingdom"
        parkingLot.address = "123 Arthur Street"

        lotArea = LotArea()
        lotArea.areaIdentifier = "Area 51"
        lotArea.parkingLot = parkingLot
        lotArea.price = "Your left kidney"
        lotArea.type = "Regular"
        lotArea.capacity = "1"

        self.assertTrue(lotArea != None)
        self.assertEqual(lotArea.areaIdentifier, "Area 51")
        self.assertEqual(lotArea.parkingLot, parkingLot)
        self.assertEqual(lotArea.price, "Your left kidney")
        self.assertEqual(lotArea.type, "Regular")
        self.assertEqual(lotArea.capacity, "1")




