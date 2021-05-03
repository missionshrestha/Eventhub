from django.db import models
from core import models as core_models

# Create your models here.
class List(core_models.TimeStampedModel):
    """List Model Defination"""

    name = models.CharField(max_length = 80)
    user = models.ForeignKey('users.User',on_delete=models.CASCADE)
    event = models.ManyToManyField('events.Event',blank =True)

    def __str__(self):
        return self.name
