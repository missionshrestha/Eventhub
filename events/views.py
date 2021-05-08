from math import ceil
from django.shortcuts import render
from . import models

# Create your views here.
def all_events(request):
    page = int(request.GET.get("page",1) or 1)
    page_size = 6
    limit = page_size * page
    offset = limit - page_size
    all_events = models.Event.objects.all()[offset:limit]
    page_count = ceil(models.Event.objects.count() / page_size)
    return render(request,"events/all_events.html",context={"event":all_events,"page":page,"page_count":page_count,"page_range":range(1,page_count+1)})