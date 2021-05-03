from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    
    """Time stamped Model"""
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # this will not allow this model to go to the database
