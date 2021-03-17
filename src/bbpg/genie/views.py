from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from genie.models import Event, Reservation, ParkingLot
from genie.forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from urllib.parse import unquote
import datetime
from django.contrib.auth.views import auth_logout


@login_required
def index(request):
    u = request.user
    reservations = Reservation.objects.filter(user=u)
    ParkingLots = ParkingLot.objects.filter(owner=u)
    ctx = {"reservations": reservations, "lots": ParkingLots}

    return render(request, 'genie/index.html', ctx)


@login_required
def lots(request):
    params = request.GET
    event = int(unquote(params['event']))
    return render(request, 'genie/lots.html')

@login_required
def spots(request):
    return render(request, 'genie/spots.html')

@login_required
def reservation(request):
    return render(request, 'genie/reservation.html')

@login_required
def user(request):
    return render(request, 'genie/user.html')

def sample(request):
    return render(request, 'genie/sample.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("genie:index")

    else:
        form = RegisterForm()

    return render(request, "genie/register.html", {"form": form})

def events(request):
    events = Event.objects.filter(startTime__gt=datetime.datetime.now())
    return render(request, "genie/events.html", {"events": events})

@login_required
def profile(request):
    return redirect("genie:index")


def logout(request):
    auth_logout(request)
    return redirect("genie:login_view")