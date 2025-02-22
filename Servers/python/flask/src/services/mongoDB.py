
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://chatbot:Rufo2009@cluster0.yju2g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
def addData(db, collection, data):
    try:
        db[collection].insert_one(data)
        return {"success": "Data has been added"}
    except Exception as e:
        return {"error": str(e)}