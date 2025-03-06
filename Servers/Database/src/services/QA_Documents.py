import PyPDF2
import re

from bson import ObjectId
from flask import jsonify
from functions.PDF_funcions import read_pdf, extract_questions_and_answers
class QA_Documents:
    def get_qa_documents(self, collection):
        answers = list(collection.find())
        for answer in answers:
            answer["_id"] = str(answer["_id"])
        return jsonify(answers)
    def get_qa_document_by_id(self, body, collection, id):
        answer = collection.find_one({"_id": ObjectId(id)})
        if answer:
            answer["_id"] = str(answer["_id"])
            return jsonify(answer)
        return jsonify({"error": "Not found"}), 404
    
    def create_qa_document(self, body, collection, model_embedding):
        if "question" not in body or "answer" not in body:
            return jsonify({"error": "Missing fields"}), 400
        
        embedding = model_embedding.encode(body["answer"]).tolist()
        body["semantic_embedding"] = embedding
        result = collection.insert_one(body)
        return jsonify({"_id": str(result.inserted_id)})
    
    def update_qa_document(self, body, collection, id, model_embedding):
        if "question" not in body or "answer" not in body:
            return jsonify({"error": "Missing fields"}), 400
        
        embedding = model_embedding.encode(body["answer"]).tolist()
        body["semantic_embedding"] = embedding
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": body})
        
        if result.matched_count:
            return jsonify({"message": "Updated successfully"})
        return jsonify({"error": "Not found"}), 404
    
    def delete_qa_document(self, collection, id):
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Deleted successfully"})
        return jsonify({"error": "Not found"}), 404
    
    
    def add_document_to_mongo(self,database, collection_name,pdf_path, embeddings_model):
        """
        Añade un documento a MongoDB con su respectivo embedding semántico.
        El documento debe de tener una estructura similar a la siguiente:
        
        1. Pregunta 1?
        Respuesta 1
        
        2. Pregunta 2?
        Respuesta 2
        
        ..."""
        collection = database[collection_name]

        datos = extract_questions_and_answers(pdf_path)
        print(datos)

        for data in datos:
            question = data["question"]
            answer = data["answer"]

            embedding = embeddings_model.encode(question)
            document = {"question": question, "answer":answer, "semantic_embedding": embedding.tolist()}
            print(f"Insertando documento: {document}")
            collection.insert_one(document)