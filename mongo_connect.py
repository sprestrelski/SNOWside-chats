import pymongo
from pymongo import MongoClient


try:
    uri = "mongodb+srv://JoshuaShruti:servicenow@clustersn0.aquderp.mongodb.net/"
    client = MongoClient(uri, server_api=pymongo.server_api.ServerApi(
        version="1", strict=True, deprecation_errors=True))
    client.admin.command("ping")
    print("Connected successfully")
    client.close()
except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

