from pymongo import MongoClient
import os

class mongohelper:
    def _assemble_mongo_filters(self, filters):
        filter_dict = {}
        for filter in filters:
            filter_dict[filter['field']] = filter['query']

        return filter_dict

    def get_db(self):
        mongo_client = MongoClient(os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_ADDR'], int(os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_PORT']))
        db = mongo_client.mycyclediary_dot_com_mongodb
        return db

    def get_collection(self, collection_name):
        collection = self.get_db()[collection_name]
        return collection

    def filter(self, collection, filters=[]):
        mongo_filters = self._assemble_mongo_filters(filters)
        return collection.find(mongo_filters)

    def aggregate(self, collection, filters=[], aggregate={}):
        filter_dict = self._assemble_mongo_filters(filters)
        return collection.aggregate([{'$match': filter_dict}, {'$group': aggregate}])
