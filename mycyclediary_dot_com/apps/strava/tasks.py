from __future__ import absolute_import

from mycyclediary_dot_com.celery import app
from mycyclediary_dot_com.apps.strava.strava import strava
from mycyclediary_dot_com.apps.strava.models import *
from mycyclediary_dot_com.apps.strava.mongohelper import mongohelper

from django.utils import timezone

from datetime import datetime


@app.task(name='mycyclediary_dot_com.apps.strava.tasks.update_athlete')
def update_athlete(athlete):
    capture_datetime = timezone.now()
    capture_timestamp = int(capture_datetime.strftime('%s'))
    mongoh = mongohelper()
    collection = mongoh.get_collection('raw_activities')

    token = athlete.strava_api_token
    after_timestamp = None
    if athlete.last_strava_sync:
        after_timestamp = int(athlete.last_strava_sync.strftime('%s'))

    stravahelper = strava(token)
    activities = stravahelper.get_athlete_activities_api(after=after_timestamp)

    for activity in activities:
        activity['_id'] = activity['id']
        activity['capture_timestamp'] = capture_timestamp
        activity['start_date'] = datetime.strptime(activity['start_date'],'%Y-%m-%dT%H:%M:%SZ')
        activity['strava_api_version'] = 3
        collection.replace_one({'_id': activity['id']}, activity, upsert=True)

    athlete.last_strava_sync = capture_datetime

    bikes,shoes = stravahelper.get_athlete_gear_api()

    for api_bike in bikes:
        db_bike = bike()
        db_bike.strava_id = api_bike.id
        db_bike.athlete = athlete
        db_bike.primary = api_bike.primary
        db_bike.name = api_bike.name
        db_bike.description = api_bike.description
        db_bike.resource_state = api_bike.resource_state
        db_bike.brand_name = api_bike.brand_name
        db_bike.model_name = api_bike.model_name
        db_bike.frame_type = api_bike.frame_type
        db_bike.save()

    athlete.save()
