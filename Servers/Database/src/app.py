from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from sentence_transformers import SentenceTransformer
import database as dbase
app = Flask(__name__)

# this will need to be reconfigured before taking the app to production
cors = CORS(app)
# Conexión a MongoDB
database = dbase.conexionMongoDB()
# client = MongoClient("mongodb://localhost:27017/")
# db = client["chat-embbeding"]
collection = database["answer"]

# Carga del modelo de embeddings
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

def generate_embedding(text):
    return model.encode(text).tolist()

@app.route("/answers", methods=["GET"])
def get_answers():
    answers = list(collection.find())
    for answer in answers:
        answer["_id"] = str(answer["_id"])
    return jsonify(answers)

@app.route("/answers/<id>", methods=["GET"])
def get_answer(id):
    answer = collection.find_one({"_id": ObjectId(id)})
    if answer:
        answer["_id"] = str(answer["_id"])
        return jsonify(answer)
    return jsonify({"error": "Not found"}), 404

@app.route("/answers", methods=["POST"])
def create_answer():
    data = request.json
    if "question" not in data or "answer" not in data:
        return jsonify({"error": "Missing fields"}), 400
    
    embedding = generate_embedding(data["answer"])
    data["semantic_embedding"] = embedding
    result = collection.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)})

@app.route("/answers/<id>", methods=["PUT"])
def update_answer(id):
    data = request.json
    if "question" not in data or "answer" not in data:
        return jsonify({"error": "Missing fields"}), 400
    
    embedding = generate_embedding(data["answer"])
    data["semantic_embedding"] = embedding
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    
    if result.matched_count:
        return jsonify({"message": "Updated successfully"})
    return jsonify({"error": "Not found"}), 404

@app.route("/answers/<id>", methods=["DELETE"])
def delete_answer(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Deleted successfully"})
    return jsonify({"error": "Not found"}), 404

@app.route("/search", methods=["POST"])
def search_mongodb():
# def search_mongodb(query:str, collection=collection, embbeding_model=model):
    """
    Busca documentos en MongoDB utilizando embeddings semánticos.
    
    :param query: Texto de la consulta.
    :return: Lista de documentos que coinciden con la consulta.
    """
    body = request.json
    query = body["query"]

    query_embedding = model.encode(query)
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


    # return {"response" : results.to_list()}
    return jsonify(results.to_list())

if __name__ == "__main__":
    app.run(debug=True)
