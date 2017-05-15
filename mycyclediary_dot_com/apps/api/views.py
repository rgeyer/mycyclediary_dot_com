from django.http import HttpResponse
import logging, json

def index(request):
    return HttpResponse('Hello, API is alive!')

def strava_webhook_callback(request):
    response = HttpResponse()

    # This is a subscribe validation request
    if request.method == 'GET' and request.GET['hub.mode'] == 'subscribe':
        response.write(request.GET['hub.challenge'])

    # This is an actual callback
    if request.method == 'POST':
        logger = logging.getLogger(__name__)
        logger.debug("Got a strava callback.. {}".format(json.dumps(request)))
        response.write('Yay, thanks for the callback!')

    return response
