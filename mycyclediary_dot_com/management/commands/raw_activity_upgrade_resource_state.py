from django.core.management.base import BaseCommand, CommandError
from mycyclediary_dot_com.apps.strava.tasks import *
from mycyclediary_dot_com.apps.strava.models import *

class Command(BaseCommand):
    help = "Finds everything in the resource_state_2 collection which hasn't resource_state_3 details fetched, and fetches it."

    def handle(self, *args, **options):
        leets = Athlete.objects.all()
        for leet in leets:
            upgrade_athlete_activity_resource_states.delay(leet)
