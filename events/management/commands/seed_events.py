import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from events import models as event_models
from users import models as user_models

class Command(BaseCommand):

    help = "This command create many events"

    def add_arguments(self,parser):
        parser.add_argument(
            "--number",type = int,default =1, help = "How many events do you want to create?"
        )
    
    def handle(self, *args,**options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        event_types = event_models.EventType.objects.all()
        seeder.add_entity(event_models.Event,number,{
            "name": lambda x: seeder.faker.address(),
            "organizer": lambda x:random.choice(all_users),
            "event_type": lambda x: random.choice(event_types),
            "price":lambda x:random.randint(0,500),
         },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        for pk in created_clean:
            event = event_models.Event.objects.get(pk=pk)
            for i in range(3,random.randint(10,15)):
                event_models.Photo.objects.create(
                    caption = seeder.faker.sentence(),
                    event = event,
                    file = f'event_photos/{random.randint(1,30)}.png',
                )
        self.stdout.write(self.style.SUCCESS(f"{number} Users Created!"))