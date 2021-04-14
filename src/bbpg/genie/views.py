from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from genie.models import Event, Reservation, ParkingLot, LotArea, Profile
from genie.forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Permission
from urllib.parse import unquote
import datetime
from django.contrib.auth.views import auth_logout
import random
from django.utils.http import urlencode
from django.http.response import HttpResponsePermanentRedirect
from django.contrib import messages


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
        return render(request, 'genie/areas.html', {"event": event_obj, "lot": lot_obj, "areas": area_avail_map})

    else:
        return redirect("genie:events")


@login_required
def reservation(request):
    return render(request, 'genie/reservation.html')


@login_required
def user(request):
    if request.user.profile.is_supervisor():
        users = User.objects.all()
        return render(request, 'genie/user.html', {"users": users})
    return redirect("genie:index")


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
            profile = Profile(user=user, balance=0)
            profile.save()
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


@login_required
def logout(request):
    auth_logout(request)
    return redirect("genie:login_view")


@login_required
def add_funds(request):
    profile = request.user.profile
    funds = float(request.POST["funds_to_add"])
    profile.balance = profile.balance + funds
    profile.save()
    return redirect("genie:index")


@login_required
def assign_events(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.GET
        if "lot" in params:
            lot_id = int(unquote(params["lot"]))
            lot = ParkingLot.objects.get(pk=lot_id)
            if request.user == lot.owner:
                evts = Event.objects.filter(startTime__gt=datetime.datetime.now())
                return render(request, "genie/assign_event.html", {"events": evts, "lot": lot})


@login_required
def assign_event(request):

    params = request.GET
    res = {"success": False}
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        if "event" in params and "lot" in params:
            event_id = int(unquote(params["event"]))
            lot_id = int(unquote(params["lot"]))
            event = Event.objects.get(pk=event_id)
            lot = ParkingLot.objects.get(pk=lot_id)
            if request.user == lot.owner:
                if lot in event.parkingLots.all():
                    event.parkingLots.remove(lot)
                else:
                    event.parkingLots.add(lot)
                res["success"] = True

    return JsonResponse(res)


@login_required
def make_reservation(request):
    params = request.GET
    if "event" in params and "area" in params:
        prof = request.user.profile
        event_id = int(unquote(params["event"]))
        area_id = int(unquote(params["area"]))
        event = Event.objects.get(pk=event_id)
        area = LotArea.objects.get(pk=area_id)

        if area.num_spots_available(event) > 0:

            new_reservation = Reservation(event=event, lotArea=area, user=request.user)
            code = f"{new_reservation.pk}R{random.randint(111111, 999999)}"
            new_reservation.code = code
            new_reservation.save()

            prof.balance -= area.price
            prof.save()

            owner = area.parkingLot.owner.profile
            owner.balance += area.price * .85
            owner.save()

    return redirect("genie:index")


@login_required
def cancel_reservation(request):
    params = request.GET
    if "reservation" in params:
        reserve_id = int(unquote(params["reservation"]))
        reserve = Reservation.objects.get(pk=reserve_id)
        if request.user == reserve.user:
            refund = reserve.lotArea.price
            reserve.delete()
            prof = request.user.profile
            prof.balance += refund
            prof.save()

            owner = reserve.lotArea.parkingLot.owner.profile
            owner.balance -= reserve.lotArea.price * .85
            owner.save()

    return redirect("genie:index")


@login_required
def create_lot(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.POST
        lot_name = params['lotName']
        lot_address = params['lotAddress']

        new_lot = ParkingLot(name=lot_name, address=lot_address, owner=request.user)
        new_lot.save()

        return HttpResponsePermanentRedirect(f"/assign_areas?lot={new_lot.pk}")
    return redirect("genie:index")


@login_required
def assign_areas(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.GET
        if "lot" in params:
            lot_record = ParkingLot.objects.get(pk=int(unquote(params["lot"])))
            if request.user == lot_record.owner:
                areas = lot_record.lotarea_set.all()

                return render(request, "genie/assign-areas.html", {"lot": lot_record, "areas": areas})
    return redirect("genie:index")

@login_required
def delete_lot(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.GET

        if "lot" in params:
            lot_id = int(unquote(params["lot"]))
            lot = ParkingLot.objects.get(pk=lot_id)
            if request.user == lot.owner:
                reservations = Reservation.objects.filter(lotArea__parkingLot=lot).all()
                if not reservations:
                    lot.delete()
                else:
                    messages.error(request, f"Cannot delete lot {lot.name}. Reservations for this lot have already been made.", "error")

    return redirect("genie:index")


@login_required
def add_area(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.POST
        if "lot" in request.GET:
            lot_pk = int(unquote(request.GET["lot"]))
            lot = ParkingLot.objects.get(pk=lot_pk)
            if request.user == lot.owner:
                area_id = unquote(params["new_area"])
                capacity = unquote(params["new_capacity"])
                type = unquote(params["new_type"])
                price = float(unquote(params["new_price"]))

                area = LotArea(areaIdentifier=area_id, capacity=capacity, type=type, price=price, parkingLot=lot)

                area.save()
                return HttpResponsePermanentRedirect(f"/assign_areas?lot={lot.pk}")
    return redirect("genie:index")


@login_required
def update_area(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.POST
        if "area" in request.GET:
            area_pk = int(unquote(request.GET["area"]))
            area = LotArea.objects.get(pk=area_pk)
            if request.user == area.parkingLot.owner:
                area_id = unquote(params["area"])
                capacity = unquote(params["capacity"])
                type = unquote(params["type"])
                price = float(unquote(params["price"]))

                area.areaIdentifier = area_id
                area.capacity = capacity
                area.type = type
                area.price = price

                area.save()
                return HttpResponsePermanentRedirect(f"/assign_areas?lot={area.parkingLot.pk}")
    return redirect("genie:index")


@login_required
def delete_area(request):
    if request.user.profile.is_manager() or request.user.profile.is_supervisor():
        params = request.GET

        if "area" in params:
            area_id = int(unquote(params["area"]))
            area = LotArea.objects.get(pk=area_id)
            if request.user == area.parkingLot.owner:
                reservations = Reservation.objects.filter(lotArea=area).all()
                if not reservations:
                    area.delete()
                else:
                    messages.error(request, f"Cannot delete area {area.areaIdentifier}. Reservations for this area have already been made.",
                                   "error")
                return HttpResponsePermanentRedirect(f"/assign_areas?lot={area.parkingLot.pk}")
    return redirect("genie:index")


@login_required
def add_event(request):
    if request.user.profile.is_supervisor():
        params = request.POST
        name = params["eventName"]
        date = params["eventDate"]
        startTime = params["startTime"]
        endTime = params["endTime"]
        address = params["address"]

        format = '%m/%d/%Y %H:%M' if "/" in date else '%Y-%m-%d %H:%M'
        startDatetime = datetime.datetime.strptime(f"{date} {startTime}", format)
        endDatetime = datetime.datetime.strptime(f"{date} {endTime}", format)

        new_event = Event(name=name, address=address, startTime=startDatetime, endTime=endDatetime)
        new_event.save()

    return redirect("genie:events")


@login_required
def update_event(request):
    if request.user.profile.is_supervisor():
        params = request.POST
        if "event" in request.GET:
            event_pk = int(unquote(request.GET["event"]))
            event = Event.objects.get(pk=event_pk)
            name = params["eventName"]
            date = params["eventDate"]
            startTime = params["startTime"]
            endTime = params["endTime"]
            address = params["address"]

            format = '%m/%d/%Y %H:%M' if "/" in date else '%Y-%m-%d %H:%M'
            startDatetime = datetime.datetime.strptime(f"{date} {startTime}", format)
            endDatetime = datetime.datetime.strptime(f"{date} {endTime}", format)

            event.name = name
            event.address = address
            event.startTime = startDatetime
            event.endTime = endDatetime

            event.save()

            return redirect("genie:events")
    return redirect("genie:index")


@login_required
def delete_event(request):
    if request.user.profile.is_supervisor():
        params = request.GET

        if "event" in params:
            event_id = int(unquote(params["event"]))
            event = Event.objects.get(pk=event_id)
            reservations = Reservation.objects.filter(event=event).all()
            if not reservations:
                event.delete()
            else:
                messages.error(request, f"Cannot delete event {event.name}. Reservations for this event have already been made.",
                               "error")

    return redirect("genie:events")

@login_required
def assign_supervisor(request):
    params = request.GET
    res = {"success": False}
    if request.user.profile.is_supervisor():
        perm = Permission.objects.get(codename="is_supervisor")
        if "user" in params:
            user_id = int(unquote(params["user"]))
            user_rec = User.objects.get(pk=user_id)
            if user_rec.profile.is_supervisor():
                user_rec.user_permissions.remove(perm)
            else:
                user_rec.user_permissions.add(perm)
            res["success"] = True

    return JsonResponse(res)

@login_required
def assign_manager(request):
    params = request.GET
    res = {"success": False}
    if request.user.profile.is_supervisor():
        perm = Permission.objects.get(codename="is_manager")
        if "user" in params:
            user_id = int(unquote(params["user"]))
            user_rec = User.objects.get(pk=user_id)
            if user_rec.profile.is_manager():
                user_rec.user_permissions.remove(perm)
            else:
                user_rec.user_permissions.add(perm)
            res["success"] = True

    return JsonResponse(res)

@login_required
def assign_attendant(request):
    params = request.GET
    res = {"success": False}
    if request.user.profile.is_supervisor():
        perm = Permission.objects.get(codename="is_attendant")
        if "user" in params:
            user_id = int(unquote(params["user"]))
            user_rec = User.objects.get(pk=user_id)
            if user_rec.profile.is_attendant():
                user_rec.user_permissions.remove(perm)
            else:
                user_rec.user_permissions.add(perm)
            res["success"] = True

    return JsonResponse(res)

@login_required
def verify(request):
    if request.user.profile.is_attendant():
        params = request.GET
        if "code" in params:
            code = unquote(params["code"])
            reserve = Reservation.objects.get(code=code)
            return render(request, "genie/verify.html", {"reservation": reserve})
    return redirect("genie:index")

