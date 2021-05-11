from django.urls import path
from . import views

app_name = "events"

urlpatterns = [path("<int:pk>",views.event_detail,name="event_detail")]