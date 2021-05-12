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
from django.core.paginator import Paginator
from . import models,forms

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
    if city:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            address = form.cleaned_data.get("address")
            city = form.cleaned_data.get("city")
            event_type =form.cleaned_data.get("event_type")
            price = form.cleaned_data.get("price")
            super_organizer = form.cleaned_data.get("super_organizer")

            filter_args = {}

            if address != "Anywhere":
                filter_args["address__startswith"] = address

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            if event_type is not None:
                filter_args["event_type"] = event_type

            if price is not None:
                filter_args["price__lte"] = price

            if super_organizer is True:
                filter_args["organizer__superorganizer"] = True

            
            qs = models.Event.objects.filter(**filter_args)
            paginator = Paginator(qs,6,orphans=3)
            page = request.GET.get("page",1)
            events = paginator.get_page(page)
            return render(request, "events/search.html",{"form":form,"events":events})

    else:

        form = forms.SearchForm()

    return render(request, "events/search.html",{"form":form,})
    
    



'''Implementing searching without using django form'''
'''
def search(request):
    city = request.GET.get("city","Anywhere")
    city = str.capitalize(city)
    address = request.GET.get("address","Anywhere")
    event_type = int(request.GET.get("event_type",0))
    event_types = models.EventType.objects.all()
    price = int(request.GET.get("price",0))
    super_organizer = bool(request.GET.get("super_organizer",False))
    choices = {
        "event_types":event_types,
    }

    form = {
        "s_event_type":event_type,
        "s_city":city,
        "price":price,
        "address":address,
        "super_organizer":super_organizer,
    }
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    if event_type != 0:
        filter_args["event_type__pk__exact"] = event_type

    if price != 0:
        filter_args["price__lte"] = price

    if super_organizer is True:
        filter_args["organizer__superorganizer"] = True

    events = models.Event.objects.filter(**filter_args)
    return render(request, "events/search.html",{**form,**choices,"events":events,"price":price,"super_organizer":super_organizer,})
'''