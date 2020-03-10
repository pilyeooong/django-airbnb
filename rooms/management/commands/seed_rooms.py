import random

from django_seed import Seed

from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand

from rooms.models import Amenity
from rooms.models import Facility
from rooms.models import HouseRule
from rooms.models import Photo
from rooms.models import Room
from rooms.models import RoomType
from users.models import User


class Command(BaseCommand):
    
    help = 'This command creates rooms'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=2, type=int, help = "How many rooms do you want to create?"
        )
    
    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        all_users = User.objects.all()
        room_types = RoomType.objects.all()
        
        seeder.add_entity(Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: random.choice(all_users),
            'room_type': lambda x: random.choice(room_types),
            'guests': lambda x: random.randint(1, 20),
            'price': lambda x: random.randint(1, 300),
            'beds': lambda x: random.randint(1, 5),
            'bedrooms': lambda x: random.randint(1, 5),
            'baths': lambda x: random.randint(1, 5),
        },)
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()
        for pk in created_clean:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f'/room_photos/{random.randint(1, 31)}.webp',
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rule.add(r)
        self.stdout.write(self.style.SUCCESS(f'{number} rooms created!'))
