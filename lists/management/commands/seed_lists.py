import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from events import models as event_models

class Command(BaseCommand):

    help = "This command create many lists"

    def add_arguments(self,parser):
        parser.add_argument(
            "--number",type = int,default =1, help = "How many lists do you want to create?"
        )

    def handle(self, *args,**options):
        number = options.get("number")
        seeder = Seed.seeder()
        user =user_models.User.objects.all()
        event = event_models.Event.objects.all()
        seeder.add_entity(list_models.List,number,{
            "user":lambda x:random.choice(user),
        })
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = event[random.randint(0,5):random.randint(6,30)]
            list_model.event.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists Created!")) 