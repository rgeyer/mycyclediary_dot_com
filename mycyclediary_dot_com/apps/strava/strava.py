from stravalib.client import Client
from stravalib import unithelper
from units import unit
from mycyclediary_dot_com.apps.strava.mongohelper import mongohelper
from mycyclediary_dot_com.apps.core.data import bike_stats
import logging

class strava:
    """A utility class for communicating with the Strava API, as well as some
    as well as fetching raw Strava activities from the MongoDB.

    Todo:
        * Probably break out the mongo bits to a more appropriate library.
    """


    def __init__(self, access_token=None, mongodb=None):
        self.logger = logging.getLogger(__name__)
        self.client = None
        if access_token:
            self.set_access_token(access_token)

        self.__mongoh = mongohelper(mongodb)

    def set_access_token(self, access_token):
        self.client = Client(access_token=access_token)

    def get_client(self):
        if not self.client:
            raise Exception("Client not initialized, please provide an access_token using strava.set_access_token()")

        return self.client

    def get_athlete_gear_api(self):
        client = self.get_client()
        athlete = client.get_athlete()
        return athlete.bikes, athlete.shoes

    def get_activity_api(self, activity_id):
        client = self.get_client()
        return client.protocol.get('/activities/{}'.format(activity_id))

    def get_athlete_activities_api(self, before=None, after=None, per_page=200):
        client = self.get_client()

        just_keep_looping = True
        activities = []
        params = {'per_page': per_page}
        if after:
            params['after'] = after

        if before:
            params['before'] = before

        while just_keep_looping:
            self.logger.debug("Requesting with "+str(params))
            activity_batch = client.protocol.get('/athlete/activities', **params)
            self.logger.debug("Activity request batch response is "+type(activity_batch).__name__)
            activities.extend(activity_batch)
            self.logger.debug("Got "+str(len(activity_batch))+" in this batch, and the total activities are "+str(len(activities)))

            if not 'page' in params:
                params['page'] = 2
            else:
                params['page'] = params['page']+1

            self.logger.debug("Before checking keep looping")

            just_keep_looping = (len(activity_batch) == per_page)
            self.logger.debug("Just keep looping value is {}".format(just_keep_looping))

        return activities

    def get_activities_mongo(self, filters=[]):
        mongo = self.__mongoh.get_collection('raw_activities_resource_state_2')
        return self.__mongoh.filter(mongo,filters)

    def aggregate_activities_mongo(self, filters=[], aggregate={}):
        mongo = self.__mongoh.get_collection('raw_activities_resource_state_2')
        return self.__mongoh.aggregate(mongo, filters, aggregate)

    def get_bike_stats(self, athlete_id, bike_id, start_date=None, end_date=None):
        """Returns aggregated usage info about a given bike.

        Args:
            athlete_id (int): The ODM primary key of the athlete
            bike_id (str): The Strava "gear_id"
            start_date(:obj:`datetime`, optional): Beginning of a date range to
                search for activities.
            end_date(:obj:`datetime`, optional): End of a date range to search
                for activities

        Returns:
            An `mycyclediary_dot_com.apps.core.data.bike_stats` object
        """

        retval = bike_stats()

        filters = [
            {'field': 'athlete.id', 'query': athlete_id},
            {'field': 'gear_id', 'query': bike_id},
        ]
        if end_date == None and start_date != None:
            filters.append({'field': 'start_date', 'query': {'$gte': start_date}})
        elif end_date != None and start_date == None:
            filters.append({'field': 'start_date', 'query': {'$lt': end_date}})
        elif end_date != None and start_date != None:
            filters.append({'field': 'start_date', 'query': {'$lt': end_date, '$gte': start_date}})

        activities = self.aggregate_activities_mongo(filters, {
            '_id': None,
            'distance': {'$sum': '$distance'},
            'elapsed_time': {'$sum': '$moving_time'},
            'elevation': {'$sum': '$total_elevation_gain'},
            'average_speed': {'$avg': '$average_speed'},
            'kilojoules': {'$sum': '$kilojoules'},
            'records': {'$sum': 1},
        })

        activity = None
        for agg in activities:
            if not activity:
                activity = agg

        if activity != None:
            retval.meters_distance = activity['distance']
            retval.time = activity['elapsed_time']
            retval.meters_elevation = activity['elevation']
            retval.meters_per_second_avg_speed = activity['average_speed']
            retval.kjs = activity['kilojoules']
            retval.records = activity['records']

        return retval
