from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from genie.models import Event
import datetime

def sample(request):
    return render(request, 'genie/sample.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("")

    else:
        form = UserCreationForm()

    return render(request, "genie/register.html", {"form": form})

def events(request):
    events = Event.objects.get(startTime__gt=datetime.datetime.now())
    return render(request, "genie/events.html", {"events": events})
