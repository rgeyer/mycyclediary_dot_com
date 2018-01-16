from django.core.management.base import BaseCommand, CommandError
from mycyclediary_dot_com.settings.secrets import *
from mycyclediary_dot_com.apps.strava.models import *
from requests import * # Maybe wanna use django requests, but I'm so much more familiar with these!
from mycyclediary_dot_com.libs.http_helper import *

import urllib, uuid, logging, json, os

class Command(BaseCommand):
    help = 'Manages the strava webhook'

    def add_arguments(self, parser):
        parser.add_argument('action')

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)

        action = options['action']
        if action == 'list':
            body = {
                "client_id": SOCIAL_AUTH_STRAVA_KEY,
                "client_secret": SOCIAL_AUTH_STRAVA_SECRET
            }
            uri = "https://api.strava.com/api/v3/push_subscriptions?{}".format(urllib.urlencode(body))
            session = Session()
            webhook_response = session.get(uri)
            # TODO: Error handling, and other smart stuff
            HttpHelper.print_request(webhook_response, logger)
            print(json.dumps(json.loads(webhook_response.text), sort_keys=True, indent=4, separators=(',', ': ')))
        if action == 'register':
            uuid_hex = uuid.uuid1().hex

            ### Request a subscription from the API
            uri = "https://api.strava.com/api/v3/push_subscriptions"
            body = {
                "client_id": SOCIAL_AUTH_STRAVA_KEY,
                "client_secret": SOCIAL_AUTH_STRAVA_SECRET,
                "object_type": "activity",
                "aspect_type": "create",
                "callback_url":"https://{}/api/strava/webhook/".format(os.environ.get('VIRTUAL_HOST', 'localhost')),
                "verify_token": uuid_hex,
            }
            headers = {"content-type": "application/x-www-form-urlencoded"}
            session = Session()
            webhook_response = session.post(uri, headers=headers, data=urllib.urlencode(body))
            # TODO: Error handling, and other smart stuff
            HttpHelper.print_request(webhook_response, logger)
            print(json.dumps(json.loads(webhook_response.text), sort_keys=True, indent=4, separators=(',', ': ')))
