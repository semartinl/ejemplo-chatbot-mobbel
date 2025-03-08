from bson import ObjectId
from flask import Flask
import database as dbase
from sentence_transformers import SentenceTransformer
from services.QA_Documents import QA_Documents
from services.Resource_service import Resource_service
from services.Embedding_service import Embedding_service
from ollama import Client
database = dbase.conexionMongoDB()

resource_db = Resource_service()
body = {"pdf_path": "C:\\Users\\USUARIO\\Downloads\\Dossier-Mobbeel 2025.pdf"}
body_search= {"query": "¿Desde cuando forma parte Mobbel de SIA?"}
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
# embedding_service = Embedding_service()

ollama_client = Client("http://localhost:7869")
name_model = "llama3.2"
ollama_client.pull(name_model)
# ollama_chat= ollama_client.create(model='example', from_=model, system="You are a virtual assistant from Mobbeel company. Dont answer any personal questions.")
# resource_db.add_resource(database=database, body=body,model_embedding=model)

# recurso = resource_db.get_resource(database,ObjectId("67c958de1170a03995549930"))

# resource_db.delete_resource_by_id(database,"67ca9fa8e97e89612d58a3f7")

# result = embedding_service.search_mongodb(body_search,database["embedding"], model)
# print(result)
ollama_response = ollama_client.chat(name_model, messages=[{'role': 'user', 'content': body_search["query"]}])
print(ollama_response)