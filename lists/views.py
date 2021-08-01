from django.shortcuts import render,redirect,reverse
from events import models as event_models
from django.views.generic import TemplateView
from . import models

# Create your views here.
def toggle_event(request,event_pk):
    action = request.GET.get('action',None)
    try:
        get_event = event_models.Event.objects.get(pk=event_pk)
    except event_models.DoesNotExist:
        get_event = None

    if get_event is not None and action is not None:
        the_list, created = models.List.objects.get_or_create(user=request.user,name="My Favourite Event")
        # the_list.event.add(get_event)
        if action =="add":
            the_list.event.add(get_event)
        elif action =="remove":
            the_list.event.remove(get_event)
    
    return redirect(reverse('events:event_detail',kwargs={"pk":event_pk}))

class SeeFavView(TemplateView):
    template_name = "lists/list_detail.html"