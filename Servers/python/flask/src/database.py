from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi

def conexionMongoDB():
    try:
        uri = "mongodb+srv://chatbot:Rufo2009@cluster0.yju2g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        database = client['MedifliContent']
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    return database
