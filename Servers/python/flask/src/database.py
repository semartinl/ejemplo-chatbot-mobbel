from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
from models.SemanticSearch import SemanticSearchEnhancer

def update_mongo_with_embeddings(database, collection_name, embeddings_model):
    """
    Actualiza los documentos en MongoDB añadiendo la propiedad 'semantic_embedding'.
    
    :param database: Objeto de la base de datos MongoDB.
    :param collection_name: Nombre de la colección en MongoDB.
    :param embeddings_model: Modelo que genera los embeddings.
    """
    collection = database[collection_name]
    documents = list(collection.find({}))
    
    for doc in documents:
        text = f"{doc.get('question', '')}"
        embedding = embeddings_model.encode(text)

        collection.update_one({"_id": doc["_id"]}, {"$set": {"semantic_embedding": embedding.tolist()}})

def search_mongodb(query:str, collection, semantic_search):
    """
    Busca documentos en MongoDB utilizando embeddings semánticos.
    
    :param query: Texto de la consulta.
    :return: Lista de documentos que coinciden con la consulta.
    """
    # collection = db["answer"]
    query_embedding = semantic_search.model.encode(query)
    #la siguiente consulta busca los 3 documentos más similares a la consulta.La 2 consulta es para recuperar los campos que se desean mostrar. En este caso, se muestra el campo de "answer"
    results = collection.aggregate([{
    "$vectorSearch": {
      "index": "vector_index",
      "path": "semantic_embedding",
      "queryVector": query_embedding.tolist(),
      "numCandidates": 3,
      "limit": 3
        }
    }, {
          "$project": {
             "_id": 0,
             "answer": 1,
             "score": {
                "$meta": "vectorSearchScore"
             }
          }
       }
  
    ])


    return list(results)
    
def conexionMongoDB():
    try:
        uri = "mongodb+srv://chatbot:Rufo2009@cluster0.yju2g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        database = client['chatbot-embbeding']
    except Exception as ex:
        print("Error durante la conexión: {}".format(ex))
    return database

# database = conexionMongoDB()

# semantic_search = SemanticSearchEnhancer()  

# busqueda = search_mongodb("¿Que soluciones ofrece Mobbeel?", database, semantic_search)

# print(list(busqueda))