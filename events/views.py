'''
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

'''
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from . import models

class EventView(ListView):
    
    '''Eventview defination'''
    model = models.Event
    paginate_by = 6
    paginate_orphans = 3
    context_object_name = "events"
    

def event_detail(request,pk):
    try:
        event = models.Event.objects.get(pk=pk)
        return render(request,"events/event_detail.html",{"event":event})
    except models.Event.DoesNotExist:
        raise Http404()

def search(request):
    city = request.GET.get("city")
    city = str.capitalize(city)
    return render(request, "events/search.html",{"city":city})




