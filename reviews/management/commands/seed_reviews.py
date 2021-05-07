import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from events import models as event_models

class Command(BaseCommand):

    help = "This command create many review"

    def add_arguments(self,parser):
        parser.add_argument(
            "--number",type = int,default =1, help = "How many review do you want to create?"
        )

    def handle(self, *args,**options):
        number = options.get("number")
        seeder = Seed.seeder()
        user =user_models.User.objects.all()
        event = event_models.Event.objects.all()
        seeder.add_entity(review_models.Review,number,{
            "user":lambda x:random.choice(user),
            "event":lambda x:random.choice(event),
            "rating":lambda x:random.randint(0,6),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews Created!")) 