from events.forms import CreateEventForm
from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
path("create/",views.CreateEventView.as_view(),name="create"),
path("<int:pk>",views.event_detail,name="event_detail"),
path("<int:pk>/edit",views.EditEventView.as_view(),name="edit"),
path("<int:pk>/photos/",views.EventPhotosView.as_view(),name="photos"),
path("<int:pk>/photos/add",views.AddPhotoView.as_view(),name="add-photo"),
path("<int:event_pk>/photos/<int:photo_pk>/delete/",views.delete_photo,name="delete-photo"),
path("<int:event_pk>/photos/<int:photo_pk>/edit/",views.EditPhotoView.as_view(),name="edit-photo"),
path("search/",views.search,name="search"),
]