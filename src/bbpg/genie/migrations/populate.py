from django.db import migrations
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth.models import Permission
import datetime

def populate_db(apps, schema_editor):
    Event = apps.get_model("genie", "Event")

    event1 = Event(name="Cool Event 1", description="This is a super cool event", address="123 Logan Street",
                   startTime=make_aware(datetime.datetime(month=6, day=26, year=2021, hour=18)),
                   endTime=make_aware(datetime.datetime(month=6, day=26, year=2021, hour=19)))

    event1.save()

    event2 = Event(name="Cool Event 2", description="This is another super cool event", address="123 Logan Street",
                   startTime=make_aware(datetime.datetime(month=8, day=15, year=2021, hour=12)),
                   endTime=make_aware(datetime.datetime(month=8, day=15, year=2021, hour=14)))

    event2.save()

    is_manager_permission = Permission(name="Is Manager")

    is_manager_permission.save()



class Migration(migrations.Migration):

    dependencies = [
        ('genie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]