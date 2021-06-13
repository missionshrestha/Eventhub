from django.urls import path
from . import views

app_name = "events"

urlpatterns = [path("<int:pk>",views.event_detail,name="event_detail"),
path("<int:pk>/edit",views.EditEventView.as_view(),name="edit"),
path("<int:pk>/photos/",views.EventPhotosView.as_view(),name="photos"),
path("<int:event_pk>/photos/<int:photo_pk>/delete/",views.delete_photo,name="delete-photo"),
path("search/",views.search,name="search"),
]