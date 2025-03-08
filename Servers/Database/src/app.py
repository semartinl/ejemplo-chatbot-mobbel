from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from sentence_transformers import SentenceTransformer
import database as dbase
from services.QA_Documents import QA_Documents
from services.Resource_service import Resource_service
from services.Embedding_service import Embedding_service
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

@app.route("/qa_documents", methods=["POST"])
def add_document():
    body = request.json
    pdf_path = body["pdf_path"]
    document_bd.add_document_to_mongo(database, "answer", pdf_path, model)
    return jsonify({"message": "Document added successfully"})

#--------------------- RESOURCES------------------------------

resource_service = Resource_service()
@app.route("/resources", methods=["POST"])
def add_resource():
    body = request.json
    print(body)
    resource_service.add_resource(database=database, body=body, model_embedding=model)
    return jsonify({"message": "Document added successfully"})

# Rutas de la API
@app.route("/resource/<resource_id>", methods=["GET"])
def get_resource_route(resource_id):
    return resource_service.get_resource(database,resource_id)

@app.route("/resources", methods=["GET"])
def get_all_resources_route():
    return resource_service.get_all_resources(database)

@app.route("/resource/<resource_id>", methods=["PUT"])
def update_resource_route(resource_id):
    body = request.json
    return resource_service.update_resource(database,resource_id, body)

@app.route("/resource/<resource_id>", methods=["DELETE"])
def delete_resource_route(resource_id):
    return resource_service.delete_resource_by_id(database,resource_id)

@app.route("/resources", methods=["DELETE"])
def delete_all_resources_route():
    return resource_service.delete_all_resource(database)

# -------------------------------EMBEDDING SEARCH -----------------------------------

embedding_service = Embedding_service()

@app.route("/search", methods=["POST"])
def search_mongodb():
    body = request.json

    return embedding_service.search_mongodb(body,database["embedding"],model)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
