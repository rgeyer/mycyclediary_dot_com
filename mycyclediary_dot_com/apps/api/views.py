from django.http import HttpResponse
import logging, json

def index(request):
    return HttpResponse('Hello, API is alive!')

def strava_webhook_callback(request):
    response = HttpResponse()
    logger = logging.getLogger(__name__)
    logger.debug("Recieved Strava Webhook API Request")

    # This is a subscribe validation request
    if request.method == 'GET':
        logger.debug("Strava webhook validation request.. {}".format(json.dumps(request.GET)))
        if 'hub.mode' in request.GET and request.GET['hub.mode'] == 'subscribe':
            obj = {
                "hub.challenge": request.GET['hub.challenge']
            }
            response.write(json.dumps(obj))
        #if request.GET['hub.mode'] == 'subscribe':

    # This is an actual callback
    if request.method == 'POST':
        logger.debug("Got a strava callback.. {}".format(json.dumps(request)))
        response.write('Yay, thanks for the callback!')

    return response
