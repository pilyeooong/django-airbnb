from django.core.management.base import BaseCommand
from rooms.models import Facility

class Command(BaseCommand):
    
    help = 'This command creates facilities'
    
    """
    def add_arguments(self, parse):
        parser.add_argument(
            '--times', help = "blah blah (help text)"
        )
    """
    
    def handle(self, *args, **options):
        facilities = [
            'Private entrance',
            'Paid parking on premises',
            'Elevator',
            'Parking',
            'Gym',
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f'{len(facilities)} facilities created!'))
