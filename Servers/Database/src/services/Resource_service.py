from bson import ObjectId
from flask import jsonify
from functions.PDF_funcions import load_and_split_data, read_pdf
from models.Resources import Resource
from models.Embbeding import Embbeding
from datetime import date
from pydantic import BaseModel
class Resource_service:
    def add_resource(self, database, body, model_embedding):
        pdf_path = body["pdf_path"]
        text_pdf = read_pdf(pdf_path)
        document = Resource(id=1, content=text_pdf, createdAt=date.today().isoformat(),updatedAt=date.today().isoformat())
        document_json = document.model_dump()
        
        resource_collection = database["resource"]
        embedding_collection = database["embedding"]
        result = resource_collection.insert_one(document_json)
        
        

        chunks = load_and_split_data(pdf_path)

        for text in chunks:
            embed_text = model_embedding.encode(text).tolist()
            embedding_class = Embbeding(
            id=1,
            resourceId=result.inserted_id,
            content=text,
            embedding=embed_text
        )
            embedding_json = embedding_class.__dict__
            embedding_collection.insert_one(embedding_json)
        
        return jsonify({"_id": str(result.inserted_id)})

    def get_resource(self, database, resource_id):
        resource_collection = database["resource"]
        # Obtener un recurso por ID
        resource = resource_collection.find_one({"_id": resource_id})
        # resource = resource_collection.find_one({"_id": ObjectId(resource_id)})
        print(f"Resource: {resource}")
        if resource:
            resource["_id"] = str(resource["_id"])
            return jsonify(resource)
        return jsonify({"error": "Resource not found"}), 404

    # Obtener todos los recursos
    def get_all_resources(self, database):
        resource_collection = database["resource"]
        resources = list(resource_collection.find())
        for resource in resources:
            resource["_id"] = str(resource["_id"])
        return jsonify(resources)

    # Actualizar un recurso por ID
    def update_resource(self, database, resource_id, body):
        resource_collection = database["resource"]
        existing_resource = resource_collection.find_one({"_id": ObjectId(resource_id)})
        if not existing_resource:
            return jsonify({"error": "Resource not found"}), 404
        
        updated_content = body.get("content", existing_resource["content"])
        updated_resource = {
            "$set": {
                "content": updated_content,
                "updatedAt": date.today().isoformat()
            }
        }
        resource_collection.update_one({"_id": ObjectId(resource_id)}, updated_resource)
        return jsonify({"message": "Resource updated successfully"})

    # Eliminar un recurso por ID
    def delete_resource_by_id(self, database, resource_id):
        resource_collection = database["resource"]
        embedding_collection = database["embedding"]
        result = resource_collection.delete_one({"_id": ObjectId(resource_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Resource not found"}), 404
        embedding_collection.delete_many({"resourceId": ObjectId(resource_id)})
        return jsonify({"message": "Resource deleted successfully"})
    
    def delete_all_resource(self, database):
        resource_collection = database["resource"]
        embedding_collection = database["embedding"]
        resource_collection.delete_many({})
        embedding_collection.delete_many({})
        return jsonify({"message": "All resources and embeddings deleted successfully"})

        