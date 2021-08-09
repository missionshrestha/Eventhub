from django.urls import path
from events import views as event_views
from . import views
app_name = "core"

urlpatterns =[
    path("",views.home_view,name="home"),
    path("events/",event_views.EventView.as_view(),name="event"),
    path("abutus/",views.aboutus, name="aboutus")
    ]