from django.db import migrations
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from genie.models import Event, Profile, ParkingLot, LotArea, Reservation
import datetime

def populate_db(apps, schema_editor):

    event1 = Event(name="Cool Event", description="This is a super cool event", address="123 Logan Street",
                   startTime=make_aware(datetime.datetime(month=6, day=26, year=2021, hour=18)),
                   endTime=make_aware(datetime.datetime(month=6, day=26, year=2021, hour=19)))

    event1.save()

    event2 = Event(name="Real Big Party", description="Come to my party", address="88 Party Street",
                   startTime=make_aware(datetime.datetime(month=8, day=15, year=2021, hour=12)),
                   endTime=make_aware(datetime.datetime(month=8, day=15, year=2021, hour=14)))

    event2.save()

    event3 = Event(name="Generic Sporting Event", description="Watch other people exercise a lot.", address="1 Stadium Road",
                   startTime=make_aware(datetime.datetime(month=8, day=21, year=2021, hour=12)),
                   endTime=make_aware(datetime.datetime(month=8, day=21, year=2021, hour=14)))

    event3.save()

    content_type = ContentType.objects.get(model='user')

    is_manager_permission = Permission(name="Is Manager", codename="is_manager", content_type=content_type)

    is_manager_permission.save()

    is_attendant_permission = Permission(name="Is Attendant", codename="is_attendant", content_type=content_type)
    is_attendant_permission.save()

    user_user = User.objects.create_user(first_name="User", last_name="User", password="user_user", username="user.user")
    user_user.save()

    attendant_user = User.objects.create_user(first_name="Attendant", last_name="User", password="attendant_user", username="attendant.user")
    attendant_user.save()

    manager_user = User.objects.create_user(first_name="manager", last_name="User", password="manager_user", username="manager.user")
    manager_user.save()

    attendant_user.user_permissions.add(is_attendant_permission)
    manager_user.user_permissions.add(is_manager_permission)

    user_profile = Profile(user=user_user, balance=100)
    user_profile.save()

    attendant_profile = Profile(user=attendant_user, balance=10)
    attendant_profile.save()

    manager_profile = Profile(user=manager_user, balance=1000)
    manager_profile.save()

    lot1 = ParkingLot(name="Green Lot", address="678 Green Street", owner=manager_user)
    lot1.save()

    lot2 = ParkingLot(name="Aggie Terrace", address="600 N 700 E, Logan, UT", owner=manager_user)
    lot2.save()

    lot3 = ParkingLot(name="Big Blue Lot", address="1000 Little Azul Road", owner=manager_user)
    lot3.save()

    event1.parkingLots.add(lot1, lot2)

    event2.parkingLots.add(lot2, lot3)

    event3.parkingLots.add(lot1, lot3)

    for lot in [lot1, lot2, lot3]:
        for i in range(5):
            area = LotArea(parkingLot=lot, price=i/2 + 1, type="Standard", areaIdentifier=str(i), capacity=2*i)
            area.save()

    area1 = LotArea(parkingLot=lot1, price=3.75, type="Tailgate", areaIdentifier="A", capacity=15)
    area1.save()
    area2 = LotArea(parkingLot=lot2, price=5.25, type="Oversize", areaIdentifier="B", capacity=20)
    area2.save()
    area3 = LotArea(parkingLot=lot3, price=2.00, type="Standard", areaIdentifier="C", capacity=10)
    area3.save()

    res1 = Reservation(code="L5G742SD45", event=event1, lotArea=area1, user=user_user)
    res1.save()
    res2 = Reservation(code="H462D6T9W3", event=event2, lotArea=area2, user=user_user)
    res2.save()
    res3 = Reservation(code="R794GH7123", event=event3, lotArea=area3, user=user_user)
    res3.save()

class Migration(migrations.Migration):

    dependencies = [
        ('genie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]