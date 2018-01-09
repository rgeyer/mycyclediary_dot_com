from pymongo import MongoClient
import os, logging

class mongohelper:
    def __init__(self, mongodb=None):
        if not mongodb:
            mongo_client = MongoClient(os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_ADDR'], int(os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_PORT']))
            mongodb = mongo_client.mycyclediary_dot_com_mongodb
        self.__mongodb = mongodb

    def _assemble_mongo_filters(self, filters):
        filter_dict = {}
        for filter in filters:
            filter_dict[filter['field']] = filter['query']

        return filter_dict

    def set_mongodb(self, mongodb):
        self.__mongodb = mongodb

    def get_mongodb(self):
        return self.__mongodb

    def get_collection(self, collection_name):
        collection = self.get_mongodb()[collection_name]
        return collection

    def filter(self, collection, filters=[]):
        mongo_filters = self._assemble_mongo_filters(filters)
        logger = logging.getLogger(__name__)
        logger.debug("Querying mongo with filterset {}".format(mongo_filters))
        return collection.find(mongo_filters)

    def aggregate(self, collection, filters=[], aggregate={}):
        filter_dict = self._assemble_mongo_filters(filters)
        return collection.aggregate([{'$match': filter_dict}, {'$group': aggregate}])
