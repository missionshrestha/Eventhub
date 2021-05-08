from django.shortcuts import render
from . import models

# Create your views here.
def all_events(request):
    page = int(request.GET.get("page",1))
    page_size = 6
    limit = page_size * page
    offset = limit - page_size
    all_events = models.Event.objects.all()[offset:limit]
    return render(request,"events/all_events.html",context={"event":all_events})