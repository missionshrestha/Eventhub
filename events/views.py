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
import datetime
import reviews
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render,redirect,reverse
from django.http import Http404
from django.views.generic import ListView,UpdateView, CreateView, FormView
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from users.models import User
from reservations.models import Reservation
from reviews.models import Review
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from users import mixins as user_mixins
from . import models,forms
from django.db.models import Q


class EventView(ListView):
    
    '''Eventview defination'''
    model = models.Event
    paginate_by = 8
    paginate_orphans = 4
    context_object_name = "events"
    

def event_detail(request,pk):
    if request.method == "POST":
        event = models.Event.objects.get(pk = pk)
        user = request.user
        review = request.POST["review"]
        rating = request.POST["rating"]
        Review.objects.create(review= review, rating = rating, user = user, event = event)

    current = datetime.datetime.now()
    now = datetime.date(current.year, current.month, current.day)
    try:
        a = False
        event = models.Event.objects.get(pk=pk)
        ended = event.event_date > now
        if request.user.is_authenticated: 
            reservation = Reservation.objects.filter(user=request.user)
            for r in reservation:
                if r.event == event:
                    a = True
                    break
                else:
                    continue
        args = {
            "event":event,
            "participated": a,
            "ended": ended
        }
        return render(request,"events/event_detail.html", args)
    except models.Event.DoesNotExist:
        raise Http404()

def approve(request, pk):
    event = models.Event.objects.get(pk = pk)
    participants = Reservation.objects.filter(event = event)
    if request.method == "POST":
        if request.POST["button_checker"] != "canceled":
            user_id = request.POST["user_id"]
            user = User.objects.get(pk = user_id)
            update_status = Reservation.objects.get(event = event, user = user)
            update_status.status = "confirmed"
            update_status.save()
        else:
            u_id = request.POST["u_id"]
            user = User.objects.get(pk = u_id)
            update_status = Reservation.objects.get(event = event, user = user)
            update_status.status = "canceled"
            update_status.save()
            
    args = {
        "event": event,
        "participants": participants,
    }
    return render(request, "events/approve.html", args)
    
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


class EditEventView(user_mixins.LogInOnlyView,UpdateView):

    model = models.Event
    template_name = "events/event_edit.html"
    form_class =forms.UpdateForm
    # fields = [
    # "name",
    # "description",
    # "city",
    # "address", 
    # "price",
    # "event_date",
    # "event_start",
    # "event_end",
    # "event_type",
    # "event_rule", 
    # ]

    def get_object(self,queryset=None):
        event = super().get_object(queryset=queryset)
        if(event.organizer.pk != self.request.user.pk):
            raise Http404()
        return event

class EventPhotosView(user_mixins.LogInOnlyView,DetailView):
    model = models.Event
    template_name = "events/event_photos.html"
    
    def get_object(self,queryset=None):
        event = super().get_object(queryset=queryset)
        if(event.organizer.pk != self.request.user.pk):
            raise Http404()
        return event


@login_required
def delete_photo(request,event_pk,photo_pk):
    user = request.user
    try:
        event = models.Event.objects.get(pk=event_pk)
        if event.organizer.pk != user.pk:
            messages.error(request,"Can't delete that photo")
        else:
            models.Photo.objects.filter(pk = photo_pk).delete()
        return redirect(reverse("events:photos",kwargs={"pk":event_pk}))
    except models.Event.DoesNotExist:
        return redirect(reverse("core:home"))

class EditPhotoView(user_mixins.LogInOnlyView, SuccessMessageMixin,UpdateView):
    
    model = models.Photo
    template_name = "events/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = (
        "caption",
    )
    
    def get_success_url(self):
        event_pk = self.kwargs.get("event_pk")
        return reverse("events:photos",kwargs={"pk":event_pk})


class AddPhotoView(user_mixins.LogInOnlyView,FormView):
    model = models.Photo
    template_name = "events/photo_create.html"
    fields = ["caption","file"]
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request,"Photo Uploaded")
        return redirect(reverse("events:photos",kwargs={"pk":pk}))


class CreateEventView(user_mixins.LogInOnlyView,FormView):
    form_class = forms.CreateEventForm
    template_name = "events/event_create.html"

    def form_valid(self,form):
        event = form.save()
        event.organizer = self.request.user
        event.save()
        form.save_m2m()
        messages.success(self.request,"Event Created")
        return redirect(reverse("events:event_detail",kwargs ={"pk":event.pk}))
        
