from stravalib.client import Client
from mycyclediary_dot_com.apps.strava.mongohelper import mongohelper
import logging

class strava:

    # def _assemble_mongo_filters(self, filters):
    #     filter_dict = {}
    #     for filter in filters:
    #         filter_dict[filter['field']] = filter['query']
    #
    #     return filter_dict

    def __init__(self, access_token=None):
        self.logger = logging.getLogger(__name__)
        self.client = None
        if access_token:
            self.set_access_token(access_token)

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
        mongoh = mongohelper()
        mongo = mongoh.get_collection('raw_activities_resource_state_2')
        return mongoh.filter(mongo,filters)

    def aggregate_activities_mongo(self, filters=[], aggregate={}):
        mongoh = mongohelper()
        mongo = mongoh.get_collection('raw_activities_resource_state_2')
        return mongoh.aggregate(mongo, filters, aggregate)
