from django.db import migrations
from django.utils import timezone

def populate_db(apps, schema_editor):
    Event = apps.get_model("genie", "Event")
    