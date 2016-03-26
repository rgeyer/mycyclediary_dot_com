# Create your views here.
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from stravalib.client import Client
from stravalib import unithelper
from django.template.loader import get_template
from django.template import RequestContext
from datetime import timedelta
from mycyclediary_dot_com.settings.secrets import *
from mycyclediary_dot_com.apps.strava.models import athlete
from django.contrib.auth.decorators import login_required
from mycyclediary_dot_com.apps.strava.strava import strava
from units import unit

import os, time, datetime, logging

def __conditional_sum_quantity(old, new):
    if old:
        return old + new
    else:
        return new

def __get_strava_client(request):
    client = Client()
    if request.user:
        if request.user.social_auth:
            provider = request.user.social_auth.get(provider='strava')
            if provider:
                if 'access_token' in provider.extra_data.keys():
                    client.access_token = provider.extra_data['access_token']
    return client

@login_required
def index(request):
    primary_bike_id = ''
    bikes = request.user.gear_set.all()
    for bike in bikes:
        if bike.primary:
            primary_bike_id = bike.strava_id

    gear_id = request.POST.get('gear_id', primary_bike_id)
    before = request.POST.get('before')
    after = request.POST.get('after')
    if before and after:
        before = datetime.datetime.strptime(before, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        after = datetime.datetime.strptime(after, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
    else:
        before = datetime.datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)
        after = before - timedelta(days=7)

    stra = strava()
    filters = [
        {'field': 'athlete.id', 'query': request.user.strava_id},
        {'field': 'start_date', 'query': {'$lt': before, '$gte': after}},
        {'field': 'gear_id', 'query': gear_id},
    ]
    activities = stra.aggregate_activities_mongo(filters, {
        '_id': None,
        'distance': {'$sum': '$distance'},
        'elapsed_time': {'$sum': '$moving_time'},
        'elevation': {'$sum': '$total_elevation_gain'},
        'average_speed': {'$avg': '$average_speed'},
        'kilojoules': {'$sum': '$kilojoules'},
    })

    template_fields = {
        'bikes': bikes,
        'gear_id':gear_id,
        'before':before.strftime('%Y-%m-%d'),
        'after':after.strftime('%Y-%m-%d'),
        'distance': unithelper.miles(unit('m')(0)),
        'time': unithelper.hours(unit('s')(0)),
        'elevation': unithelper.meters(unit('m')(0)),
        'avg_speed': unithelper.mph(unit('m')(0)/unit('s')(1)),
        'kjs': 0,
    }
    activity = None
    for agg in activities:
        if not activity:
            activity = agg

    if activity:
        merge_dict = template_fields.copy()
        merge_dict.update({
            'distance': unithelper.miles(unit('m')(activity['distance'])),
            'time': unithelper.hours(unit('s')(activity['elapsed_time'])),
            'elevation': unithelper.meters(unit('m')(activity['elevation'])),
            'avg_speed': unithelper.mph(unit('m')(activity['average_speed'])/unit('s')(1)),
            'kjs': activity['kilojoules'],
        })
        template_fields = merge_dict

    return render_to_response('strava/templates/strava_index.html', template_fields, context_instance=RequestContext(request))
