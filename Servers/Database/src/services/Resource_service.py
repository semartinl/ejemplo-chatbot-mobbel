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
        print(document_json)
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


            

        