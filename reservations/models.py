from django.db import models
from core import models as core_models

# Create your models here.
class Reservation(core_models.TimeStampedModel):

    """Reservation Model Defination"""
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING,'Pending'),
        (STATUS_CONFIRMED,'Confirmed'),
        (STATUS_CANCELED,'Canceled'),
    )

    status = models.CharField(max_length = 15,choices=STATUS_CHOICES,default = STATUS_PENDING)
    event = models.ForeignKey("events.Event",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event}'