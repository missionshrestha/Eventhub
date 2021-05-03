from django.db import models
from core import models as core_models
from users import models as user_models

# Create your models here.
class AbstractType(core_models.TimeStampedModel):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class EventType(AbstractType):
    
    class Meta:
        verbose_name_plural = "Event Types"


class EventRule(AbstractType):
    
    ordering = "created"
    class Meta:
        verbose_name_plural = "Event Rules"



class Event(core_models.TimeStampedModel):

    """Event model defination"""
    name = models.CharField(max_length = 150)
    description = models.TextField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    price = models.IntegerField()
    event_start = models.TimeField()
    event_end = models.TimeField()
    organizer = models.ForeignKey(user_models.User,on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType,on_delete=models.SET_NULL,null=True)
    event_rule = models.ManyToManyField(EventRule,blank=True)

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):
    """ Photo Model Defination """

    caption = models.CharField(max_length=100)
    file = models.ImageField()
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    def __str__(self):
        return self.caption

