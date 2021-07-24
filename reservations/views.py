from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Reservation
from users.models import User
from events.models import Event

# Create your views here.
def register(request, event_id):
    if request.user.is_authenticated:
        user = request.user
        event = Event.objects.get(pk=event_id)
        if not Reservation.objects.filter(user  = request.user, event = event):
            Reservation.objects.create(status="pending", event=event, user=user)
        reservation = Reservation.objects.get(user = request.user, event = event)
        args = {"user": user, "event": event, "reservation": reservation}
    else:
        html = "<html><body>You are not logged in. Log in first to register for any Events.</body></html>"
        return HttpResponse(html)
    
    
    return render(request, "register/afterregister.html", args)

def view_status(request, event_id):
    user = request.user
    event = Event.objects.get(pk=event_id)
    reservation = Reservation.objects.get(user = request.user, event = event)
    args = {"user": user, "event": event, "reservation": reservation}

    return render(request, "register/afterregister.html" , args)
    
