from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from genie.models import Event, Reservation, ParkingLot, LotArea
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
    if 'event' in params:
        event = int(unquote(params['event']))
        event_obj = Event.objects.get(pk=event)
        lts = ParkingLot.objects.filter(event=event_obj)
        return render(request, 'genie/lots.html', {"lots": lts, "event": event_obj})

    else:
        return redirect("genie:events")


@login_required
def spots(request):
    params = request.GET
    if 'event' in params and 'lot' in params:
        event = int(unquote(params['event']))
        event_obj = Event.objects.get(pk=event)
        lot = int(unquote(params['lot']))
        lot_obj = ParkingLot.objects.get(pk=lot)
        area_avail_map = []
        areas = LotArea.objects.filter(parkingLot=lot_obj)
        for area in areas:
            area_avail_map.append([area, area.num_spots_available(event_obj)])
        return render(request, 'genie/spots.html', {"event": event_obj, "lot": lot_obj, "areas": area_avail_map})

    else:
        return redirect("genie:events")


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
    evts = Event.objects.filter(startTime__gt=datetime.datetime.now())
    return render(request, "genie/events.html", {"events": evts})


@login_required
def profile(request):
    return redirect("genie:index")


def logout(request):
    auth_logout(request)
    return redirect("genie:login_view")


def add_funds(request):
    profile = request.user.profile
    funds = float(request.POST["funds_to_add"])
    profile.balance = profile.balance + funds
    profile.save()
    return redirect("genie:index")


def assign_events(request):
    params = request.GET
    if "lot" in params:
        lot_id = int(unquote(params["lot"]))
        lot = ParkingLot.objects.get(pk=lot_id)
        evts = Event.objects.filter(startTime__gt=datetime.datetime.now())
        return render(request, "genie/assign_event.html", {"events": evts, "lot": lot})


def assign_event(request):
    params = request.GET
    res = {"success": False}
    if "event" in params and "lot" in params:
        event_id = int(unquote(params["event"]))
        lot_id = int(unquote(params["lot"]))
        event = Event.objects.get(pk=event_id)
        lot = ParkingLot.objects.get(pk=lot_id)
        if lot in event.parkingLots.all():
            event.parkingLots.remove(lot)
        else:
            event.parkingLots.add(lot)
        res["success"] = True

    return JsonResponse(res)