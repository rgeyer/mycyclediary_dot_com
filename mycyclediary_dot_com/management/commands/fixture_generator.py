from django.core.management.base import BaseCommand, CommandError
from mycyclediary_dot_com.apps.strava.models import *
from stravalib import unithelper
from datetime import timedelta
from units import unit

import logging, json, datetime

class Command(BaseCommand):
    help = 'Generates some mongoimport-able fixtures for testing'

    def handle(self, *args, **options):
        # "start_date_local": "2017-10-08T23:59:59Z"
        # "moving_time": 1800
        # "kilojoules": 1000
        # "distance": 16093.44 # 10 miles
        # "total_elevation_gain": 500
        logger = logging.getLogger(__name__)
        athlete_count = input("Enter Desired Number of Athletes:")
        gear_count = input("Enter Desired Number of Bikes per Athlete:")
        activity_count = input("Enter Desired Activity Count per Bike per Athlete:")
        distance = input("Enter Distance Per Activity (Miles):")
        elapsed_time = input("Enter Time Per Activity (Seconds):")
        elevation = input("Enter Elevation Gain Per Activity (Meters):")
        kjs = input("Enter kilojoules Per Activity:")
        start_date = datetime.datetime.strptime('2017-10-18T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ') - timedelta(days=int(activity_count))

        f = open("mycyclediary_dot_com/fixtures/mongo/{}.json".format(start_date.isoformat()), "w")

        activity_id = 0

        for athlete_id in range(int(athlete_count)):
            for gear_id in range(int(gear_count)):
                for i in range(int(activity_count)):
                    distance_unit = unithelper.meters(unit('mi')(int(distance)))
                    activity_date = start_date + timedelta(days=i)
                    dict_activity = {
                       "_id": activity_id,
                       "start_date_local":activity_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "id":activity_id,
                       "gear_id":str(gear_id),
                       "elapsed_time":int(elapsed_time),
                       "type":"Ride",
                       "start_date":{
                          "$date":activity_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                       },
                       "moving_time":int(elapsed_time),
                       "strava_api_version":3,
                       "distance":distance_unit.num,
                       "name":"Generated activity {}".format(activity_id),
                       "total_elevation_gain":int(elevation),
                       "athlete":{
                          "resource_state":1,
                          "id":athlete_id
                       },
                       "average_speed": distance_unit.num/int(elapsed_time),
                       "kilojoules": int(kjs)
                    }

                    json_str = json.dumps(dict_activity, sort_keys=True, indent=4, separators=(',', ': '))

                    f.write(json.dumps(dict_activity)+",\n")

                    print(json_str)
                    activity_id = activity_id+1

        f.close()
