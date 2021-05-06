from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.EventType,models.EventRule)
class TypeAdmin(admin.ModelAdmin):
    
    list_display = ("name","used_by")
    
    def used_by(self,obj):
        return obj.events.count()

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    """Event admin defination"""
    fieldsets = (
        (
            "Basic Info",
            {"fields":("name","description","address","city","price",)}
            ),
            (
                "Times",
                {"fields":("event_start","event_end","event_date")}
            ),
            (
                "More About",
                {
                    'classes':("collapse",),
                    "fields":("organizer","event_type","event_rule")}
                )
    )

    list_display = (
        "name",
        "organizer",
        "address",
        "city",
        "price",
        "event_type",
        'no_of_rules',
        'count_photos',
    )

    def no_of_rules(self,obj):        #for many to many field we cannot simply pit it in list_display instead we have to write our own function.
        return obj.event_rule.count()

    def count_photos(self,obj):
        return obj.photos.count()

    ordering = ("name","price")

    list_filter = (
        "event_type",
    )
    search_fields = ("name","^city")

    filter_horizontal = ("event_rule",)

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass