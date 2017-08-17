# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from django.template import RequestContext
from django.forms import modelform_factory
from stravalib.client import Client
from stravalib import unithelper
from datetime import timedelta
from mycyclediary_dot_com.settings.secrets import *
from mycyclediary_dot_com.apps.strava.models import athlete, component
from mycyclediary_dot_com.apps.strava.models import bike as bike_odm
from mycyclediary_dot_com.apps.strava.strava import strava
from units import unit
from requests import * # Maybe wanna use django requests, but I'm so much more familiar with these!

import os, time, datetime, logging, json, uuid, urllib

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
    logger = logging.getLogger(__name__)
    template_fields = {
        'bikes': {},
        'activities': [],
    }

    stra = strava()
    filters = [
        {'field': 'athlete.id', 'query': int(request.user.strava_id)},
    ]
    activities = stra.get_activities_mongo(filters)
    for activity in activities:
        logger.debug(u"Activity inside of activities is {}. Name is {}".format(type(activity).__name__, activity['name']))
        template_fields["activities"].append(activity)

    logger.debug("request user object type is "+type(request.user).__name__)
    logger.debug("There are {} activities".format(len(template_fields['activities'])))

    return render_to_response('strava/templates/strava_index.html', template_fields, context_instance=RequestContext(request))

@login_required
def bike_stats(request):
    primary_bike_id = ''
    bikes = bike_odm.objects.filter(athlete=request.user.id)
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

    return render_to_response('strava/templates/strava_bike_stats.html', template_fields, context_instance=RequestContext(request))

@login_required
def bikes(request):
    logger = logging.getLogger(__name__)
    template_fields = {
        'bikes': {},
    }

    stra = strava()
    bikes = bike_odm.objects.filter(athlete=request.user.id)
    for bike in bikes:
        filters = [
            {'field': 'athlete.id', 'query': request.user.strava_id},
            {'field': 'gear_id', 'query': bike.strava_id},
        ]
        activities = activities = stra.get_activities_mongo(filters)
        template_fields["bikes"][bike.strava_id] = {
            "bike": bike,
        }
        distance = 0
        time = 0
        elevation = 0
        avg_speed = 0
        kjs = 0

        for activity in activities:
            if 'distance' in activity:
                distance += activity['distance']
            if 'total_elevation_gain' in activity:
                elevation += activity['total_elevation_gain']

        template_fields["bikes"][bike.strava_id]["distance"] = unithelper.miles(unit('m')(distance))
        template_fields["bikes"][bike.strava_id]["elevation"] = unithelper.meters(unit('m')(elevation))

    return render_to_response('strava/templates/strava_bikes.html', template_fields, context_instance=RequestContext(request))

@login_required
def components(request):
    logger = logging.getLogger(__name__)
    components = component.objects.filter(athlete=request.user.id)
    template_fields = {
        'components': components
    }

    return render_to_response('strava/templates/components.html', template_fields, context_instance=RequestContext(request))
