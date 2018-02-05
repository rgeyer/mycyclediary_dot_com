# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from django.template import RequestContext
from django.forms import modelform_factory
from stravalib.client import Client
from stravalib import unithelper
from datetime import timedelta
from mycyclediary_dot_com.settings.secrets import *
from mycyclediary_dot_com.apps.strava.models import Athlete, component
from mycyclediary_dot_com.apps.strava.models import bike as bike_odm
from mycyclediary_dot_com.apps.strava.strava import strava
from units import unit
from requests import * # Maybe wanna use django requests, but I'm so much more familiar with these!

import os, time, datetime, logging, json, uuid, urllib, pytz

def __get_strava_client(request):
    client = Client()
    if request.user:
        if request.user.social_auth:
            provider = request.user.social_auth.get(provider='strava')
            if provider:
                if 'access_token' in provider.extra_data.keys():
                    client.access_token = provider.extra_data['access_token']
    return client

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

    return render(request, 'strava/templates/strava_index.html', template_fields)

def component_stats(request):
    logger = logging.getLogger(__name__)
    primary_bike_id = ''
    comp_list = component.objects.filter(athlete=request.user.id)
    bikes = bike_odm.objects.filter(athlete=request.user.id)
    for bike in bikes:
     if bike.primary:
         primary_bike_id = bike.id

    component_id = request.POST.get('component_id', primary_bike_id)
    before = request.POST.get('before')
    after = request.POST.get('after')
    if before and after:
        before = datetime.datetime.strptime(before, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        after = datetime.datetime.strptime(after, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
    else:
        before = datetime.datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)
        after = before - timedelta(days=7)

    before = before.replace(tzinfo=pytz.UTC)
    after = after.replace(tzinfo=pytz.UTC)

    comp = component.objects.get(pk=component_id)
    aggs = comp.get_aggregates(end_date=before, start_date=after)

    template_fields = {
        'components': comp_list,
        'component_id':int(component_id),
        'before':before.strftime('%Y-%m-%d'),
        'after':after.strftime('%Y-%m-%d'),
        'distance': unithelper.miles(unit('m')(aggs.meters_distance)),
        'time': unithelper.hours(unit('s')(aggs.time)),
        'elevation': unithelper.meters(unit('m')(aggs.meters_elevation)),
        'avg_speed': unithelper.mph(unit('m')(aggs.meters_per_second_avg_speed)/unit('s')(1)),
        'kjs': aggs.kjs,
    }

    return render(request, 'strava/templates/strava_component_stats.html', template_fields)

def bikes(request):
    logger = logging.getLogger(__name__)
    template_fields = {
        'bikes': {},
    }

    bikes = bike_odm.objects.filter(athlete=request.user.id)
    for bike in bikes:
        template_fields["bikes"][bike.strava_id] = {
            "bike": bike,
        }

        aggs = bike.get_aggregates()

        template_fields["bikes"][bike.strava_id]["distance"] = unithelper.miles(unit('m')(aggs.meters_distance))
        template_fields["bikes"][bike.strava_id]["elevation"] = unithelper.meters(unit('m')(aggs.meters_elevation))

    return render(request, 'strava/templates/strava_bikes.html', template_fields)

def components(request):
    logger = logging.getLogger(__name__)
    components = component.objects.filter(athlete=request.user.id)
    template_fields = {
        'components': components
    }

    return render(request, 'strava/templates/components.html', template_fields)
