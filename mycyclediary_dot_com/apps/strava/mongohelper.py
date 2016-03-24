from pymongo import MongoClient
import os

class mongohelper:
    def get_db(self):
        mongo_client = MongoClient(os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_ADDR'], int(os.environ['CYCLEDIARYMONGO1_PORT_27017_TCP_PORT']))
        db = mongo_client.mycyclediary_dot_com_mongodb
        return db

    def get_collection(self, collection_name):
        collection = self.get_db()[collection_name]
        return collection
