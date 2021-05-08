from django.urls import path
from events import views as event_views

app_name = "core"

urlpatterns =[path("events/",event_views.all_events,name="home")]