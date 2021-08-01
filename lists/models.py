from django.db import models
from core import models as core_models

# Create your models here.


class List(core_models.TimeStampedModel):
    """List Model Defination"""

    name = models.CharField(max_length=80)
    user = models.OneToOneField(
        'users.User', related_name="list", on_delete=models.CASCADE)
    event = models.ManyToManyField(
        'events.Event', related_name="event", blank=True)

    def __str__(self):
        return self.name

    def count_event(self):
        return self.event.count()
    count_event.short_description = "Number of events"
