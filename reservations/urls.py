from django.urls import path 
from . import views

app_name = "reservations"

urlpatterns = [
    path("<int:event_id>/register", views.register, name="register"),
    path("<int:event_id>/view_status", views.view_status, name="view_status"),
    path("cancel/<int:event_id>", views.cancel_registration, name="cancel")
]