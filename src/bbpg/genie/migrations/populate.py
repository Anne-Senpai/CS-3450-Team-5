from django.db import migrations
from django.utils import timezone
import datetime

def populate_db(apps, schema_editor):
    Event = apps.get_model("genie", "Event")

    event1 = Event(name="Cool Event 1", description="This is a super cool event", address="123 Logan Street",
                   startTime=datetime.datetime(month=6, day=26, year=2021, hour=18),
                   endTime=datetime.datetime(month=6, day=26, year=2021, hour=19))

    event1.save()

    event2 = Event(name="Cool Event 2", description="This is another super cool event", address="123 Logan Street",
                   startTime=datetime.datetime(month=8, day=15, year=2021, hour=12),
                   endTime=datetime.datetime(month=8, day=15, year=2021, hour=14))

    event2.save()

class Migration(migrations.Migration):

    dependencies = [
        ('genie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]