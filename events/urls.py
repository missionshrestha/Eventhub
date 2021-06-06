from django.urls import path
from . import views

app_name = "events"

urlpatterns = [path("<int:pk>",views.event_detail,name="event_detail"),
path("<int:pk>/edit",views.EditEventView.as_view(),name="edit"),
path("search/",views.search,name="search"),
]