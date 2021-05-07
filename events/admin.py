from django.contrib import admin
from django.utils.html import mark_safe  #mark a string safe for HTML output porpose
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
        'total_rating',
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
    
    """Photo admin defination"""
    list_display = ("__str__","get_thumbnail")

    def get_thumbnail(self,obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')
    get_thumbnail.short_description = "Thumbnails"