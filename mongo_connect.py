import config
import pymongo
from pymongo import MongoClient

def insert(data):
    try:
        # connecting
        uri = config.mongo_uri
        client = MongoClient(uri, server_api=pymongo.server_api.ServerApi(
            version="1", strict=True, deprecation_errors=True))
        client.admin.command("ping")

        # inserting data
        database = client["user_data"]
        collection = database["content"]

        collection.insert_one(data)

        items = collection.find( {} )

        f = open("intros.csv", "a")
        
        for item in items:
            f.write("\n" + item['user_id']+","+item['message'])
            

        client.close()
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)