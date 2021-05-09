from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage
from . import models

# Create your views here.
def all_events(request):
    page = request.GET.get("page",1)
    event_list = models.Event.objects.all()
    paginator = Paginator(event_list,6)
    try:
        events = paginator.page(int(page))
        return render(request,"events/all_events.html",{"page":events})
    except EmptyPage:
        return redirect('/events')