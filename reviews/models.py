from django.db import models
from core import models as core_models
# Create your models here.

class Review(core_models.TimeStampedModel):
    """Review Model Defination"""

    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey("users.User",related_name="reviews",on_delete=models.CASCADE)
    event = models.ForeignKey("events.Event",related_name="reviews",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review} - {self.event}'
