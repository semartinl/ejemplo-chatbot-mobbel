from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from sentence_transformers import SentenceTransformer
import database as dbase
from Servers.Database.src.services.QA_Documents import QA_Documents
app = Flask(__name__)

# this will need to be reconfigured before taking the app to production
cors = CORS(app)
# Conexión a MongoDB
database = dbase.conexionMongoDB()
# client = MongoClient("mongodb://localhost:27017/")
# db = client["chat-embbeding"]
collection_qa = database["answer"]

# Carga del modelo de embeddings
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

def generate_embedding(text):
    return model.encode(text).tolist()

document_bd = QA_Documents()

@app.route("/answers", methods=["GET"])
def get_answers():
    return document_bd.get_qa_documents(collection_qa)

@app.route("/answers/<id>", methods=["GET"])
def get_answer(id):
    body = request.json
    return document_bd.get_qa_document_by_id(collection_qa, id)

@app.route("/answers", methods=["POST"])
def create_answer():
    data = request.json
    return document_bd.create_qa_document(data, collection_qa, model)

@app.route("/answers/<id>", methods=["PUT"])
def update_answer(id):
    data = request.json
    return document_bd.update_qa_document(data, collection_qa, id, model)

@app.route("/answers/<id>", methods=["DELETE"])
def delete_answer(id):
    return document_bd.delete_qa_document(collection_qa, id)

@app.route("/search", methods=["POST"])
def search_mongodb():
# def search_mongodb(query:str, collection_qa=collection_qa, embbeding_model=model):
    """
    Busca documentos en MongoDB utilizando embeddings semánticos.
    
    :param query: Texto de la consulta.
    :return: Lista de documentos que coinciden con la consulta.
    """
    body = request.json
    query = body["query"]

    query_embedding = model.encode(query)
    #la siguiente consulta busca los 3 documentos más similares a la consulta.La 2 consulta es para recuperar los campos que se desean mostrar. En este caso, se muestra el campo de "answer"
    results = collection_qa.aggregate([{
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


    # return {"response" : results.to_list()}
    return jsonify(results.to_list())

if __name__ == "__main__":
    app.run(debug=True)
