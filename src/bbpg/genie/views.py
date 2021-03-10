from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from genie.models import Event
import datetime

def index(request):
    return render(request, 'genie/index.html')

def lots(request):
    return render(request, 'genie/lots.html')

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
    events = Event.objects.filter(startTime__gt=datetime.datetime.now())
    months = ["", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return render(request, "genie/events.html", {"events": events, "months": months})