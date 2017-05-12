from __future__ import absolute_import

from mycyclediary_dot_com.celery import app
from mycyclediary_dot_com.apps.strava.strava import strava
from mycyclediary_dot_com.apps.strava.models import *
from mycyclediary_dot_com.apps.strava.mongohelper import mongohelper

from django.utils import timezone

from datetime import datetime

import logging, json

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# TODO: This is deliberatly very heavy handed, and does not throttle, nor respect
# rate limiting from strava. Will have to ultimately make this smarter when/if
# this becomes a tool that anyone besides I use.
@app.task(name='mycyclediary_dot_com.apps.strava.tasks.upgrade_athlete_activity_resource_states')
def upgrade_athlete_activity_resource_states(athlete):
    mongoh = mongohelper()
    state2 = mongoh.get_collection('raw_activities_resource_state_2')
    state3 = mongoh.get_collection('raw_activities_resource_state_3')

    token = athlete.strava_api_token
    stravahelper = strava(token)

    filters = [
        {'field': 'athlete.id', 'query': athlete.strava_id},
        {'field': 'upgraded_to_resource_state_3', 'query': {'$exists': False}}
    ]
    to_upgrade = mongoh.filter(state2, filters)
    total = 0
    for activity in to_upgrade:
        total = total + 1
        logger.debug("Upgrading activity {} to resource_state 3 (Detailed view)".format(activity['_id']))
        detailed_activity = stravahelper.get_activity_api(activity['_id'])

        detailed_activity['_id'] = activity['_id']
        detailed_activity['start_date'] = activity['start_date']
        detailed_activity['strava_api_version'] = 3

        state3.replace_one({'_id': activity['_id']}, detailed_activity, upsert=True)
        state2.update_one({'_id': activity['_id']}, {'$set': {'upgraded_to_resource_state_3': True}})

    logger.debug("Found {} records for athlete {} which need to be upgraded to resource_state_3".format(total, athlete.strava_id))

@app.task(name='mycyclediary_dot_com.apps.strava.tasks.update_athlete')
def update_athlete(athlete):
    capture_datetime = timezone.now()
    capture_timestamp = int(capture_datetime.strftime('%s'))

    logger.debug("Starting update for athlete {}. Capture datetime = {} timestamp = {}".format(athlete.id, capture_datetime.strftime('%c'), capture_timestamp))

    mongoh = mongohelper()
    collection = mongoh.get_collection('raw_activities_resource_state_2')

    token = athlete.strava_api_token
    stravahelper = strava(token)
    after_timestamp = None
    if athlete.last_strava_sync:
        filters = [
            {'field': 'athlete.id', 'query': athlete.strava_id}
        ]
        max_record = stravahelper.aggregate_activities_mongo(filters, {
            '_id': None,
            'max_start_date': {'$max': '$start_date'},
        })

        record = None
        for agg in max_record:
            if not record:
                record = agg

        if record:
            after_timestamp = int(record['max_start_date'].strftime('%s'))
        else:
            after_timestamp = capture_timestamp - 604800

    lastsync = athlete.last_strava_sync.strftime('%c') if athlete.last_strava_sync else "null"

    logger.debug("After dbstring = {} timestamp = {}".format(lastsync, after_timestamp))

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
