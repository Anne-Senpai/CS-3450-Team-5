from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from genie.models import Event
from genie.forms import RegisterForm
import datetime

def index(request):
    return render(request, 'genie/index.html')

def lots(request):
    return render(request, 'genie/lots.html')

def spots(request):
    return render(request, 'genie/spots.html')

def reservation(request):
    return render(request, 'genie/reservation.html')

def user(request):
    return render(request, 'genie/user.html')

def sample(request):
    return render(request, 'genie/sample.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("")

    else:
        form = RegisterForm()

    return render(request, "genie/register.html", {"form": form})

def events(request):
    events = Event.objects.filter(startTime__gt=datetime.datetime.now())
    months = ["", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return render(request, "genie/events.html", {"events": events, "months": months})
