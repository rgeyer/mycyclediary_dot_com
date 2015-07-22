# Create your views here.
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from stravalib.client import Client
from django.template.loader import get_template
from django.template import RequestContext
from datetime import timedelta
from mycyclediary_dot_com.settings.secrets import *

import os, time, datetime

def __conditional_sum_quantity(old, new):
    if old:
        return old + new
    else:
        return new

def __get_strava_client(request):
    client = Client()
    strava_access_token = request.session.get('strava_access_token', False)
    if strava_access_token:
        client.access_token = strava_access_token

    return client

def index(request):
    strava_access_token = request.session.get('strava_access_token', False)
    if strava_access_token:
        client = __get_strava_client(request)
        athlete = client.get_athlete()
        primary_bike_id = ''
        for bike in athlete.bikes:
            if bike.primary:
                primary_bike_id = bike.id

        gear_id = request.POST.get('bike_id', primary_bike_id)
        before = request.POST.get('before')
        after = request.POST.get('after')
        if before and after:
            before = datetime.datetime.strptime(before, '%d/%m/%Y')
            after = datetime.datetime.strptime(after, '%d/%m/%Y')
        else:
            before = datetime.datetime.today()
            after = datetime.datetime.today() - timedelta(days=7)

        page = 0
        activity_itr = client.get_activities(before,after,200)
        activities = []
        gear_ids = []
        total_distance = None
        total_time = None
        total_elevation = None
        total_avg_speed = None
        total_kjs = None
        for activity in activity_itr:
            if activity.type.lower() == 'ride':
                activities.append(activity)
                gear_ids.append(activity.gear_id)
                total_distance = __conditional_sum_quantity(total_distance, activity.distance)
                total_time = __conditional_sum_quantity(total_time, activity.moving_time)
                total_elevation = __conditional_sum_quantity(total_elevation, activity.total_elevation_gain)
                total_avg_speed = __conditional_sum_quantity(total_avg_speed, activity.average_speed)
                total_kjs = __conditional_sum_quantity(total_kjs, activity.kilojoules)

        return render_to_response('index.html',{
            'distance':total_distance,
            'time':total_time,
            'elevation':total_elevation,
            'avg_speed':total_avg_speed/len(activities),
            'kjs':total_kjs,
            'athlete':athlete,
            'gear_id':gear_id,
            'before':before.strftime('%d/%m/%Y'),
            'after':after.strftime('%d/%m/%Y')
            },
            context_instance=RequestContext(request))
    else:
        return request_auth(request)

def request_auth(request):
    client = __get_strava_client(request)
    auth_url = client.authorization_url(client_id=STRAVA_OAUTH_CLIENT_ID, redirect_uri='http://dev.mycyclediary.com/strava/authorize')

    return redirect(auth_url)


def authorize(request):
    client = __get_strava_client(request)
    code = request.GET.get('code')

    access_token = client.exchange_code_for_token(client_id=STRAVA_OAUTH_CLIENT_ID, client_secret=STRAVA_OAUTH_CLIENT_SECRET, code=code)
    request.session['strava_access_token'] = access_token

    return redirect('/strava')
