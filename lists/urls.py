from django.urls import path
from django.urls import path
from . import views
app_name = "lists"

urlpatterns = [
    path("toggle/<int:event_pk>",views.toggle_event,name="toggle-event"),
    path("favs/",views.SeeFavView.as_view(),name="see-favs"),
]