from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.EventType,models.EventRule)
class TypeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):

    pass

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass