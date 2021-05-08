from django.shortcuts import render
from . import models

# Create your views here.
def all_events(request):
    all_events = models.Event.objects.all()
    return render(request,"all_events.html",context={"event":all_events})