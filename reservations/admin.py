from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Reservation)
class Reservation(admin.ModelAdmin):
    """Reservation Admin Defination"""

    pass