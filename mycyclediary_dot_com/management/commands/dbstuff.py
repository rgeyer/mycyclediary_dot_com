from django.core.management.base import BaseCommand, CommandError
from mycyclediary_dot_com.apps.strava.tasks import *
from mycyclediary_dot_com.apps.strava.models import *

class Command(BaseCommand):
    help = 'Does DB Stuff'

    def handle(self, *args, **options):
        leets = athlete.objects.all()
        for leet in leets:
            update_athlete.delay(leet)
