import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservation_models
from events import models as event_models

class Command(BaseCommand):

    help = "This command create many reservations"

    def add_arguments(self,parser):
        parser.add_argument(
            "--number",type = int,default =1, help = "How many reservations do you want to create?"
        )

    def handle(self, *args,**options):
        number = options.get("number")
        seeder = Seed.seeder()
        event = event_models.Event.objects.all()
        seeder.add_entity(reservation_models.Reservation,number,{
            "status":lambda x:random.choice(["pending","confirmed","canceled"]),
            "event":lambda x:random.choice(event),
        })
        seeder.execute()
        
        self.stdout.write(self.style.SUCCESS(f"{number} reservations Created!")) 