from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Reservation)
class Reservation(admin.ModelAdmin):
    """Reservation Admin Defination"""

    list_display = ("event","status")

    list_filter = ("status",)