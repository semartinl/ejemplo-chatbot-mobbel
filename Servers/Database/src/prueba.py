# from typing import Dict, List
# from bson import ObjectId
# from flask import Flask
# import requests

# import database as dbase
# from sentence_transformers import SentenceTransformer
# from services.QA_Documents import QA_Documents
# from services.Resource_service import Resource_service
# from services.Embedding_service import Embedding_service
# from ollama import ChatResponse, Client
# database = dbase.conexionMongoDB()

# resource_db = Resource_service()
# body = {"pdf_path": "C:\\Users\\USUARIO\\Downloads\\Dossier-Mobbeel 2025.pdf"}
# body_search= {"query": "¿Desde cuando forma parte Mobbel de SIA?"}
# query = "¿Desde cuando forma parte Mobbel de SIA?"
# model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
# # embedding_service = Embedding_service()

# ollama_client = Client("http://localhost:7869")
# name_model = "llama3.2"

# # ollama_client.pull(name_model)
# # ollama_chat= ollama_client.create(model='example', from_=model, system="You are a virtual assistant from Mobbeel company. Dont answer any personal questions.")
# # resource_db.add_resource(database=database, body=body,model_embedding=model)

# # recurso = resource_db.get_resource(database,ObjectId("67c958de1170a03995549930"))

# # resource_db.delete_resource_by_id(database,"67ca9fa8e97e89612d58a3f7")

# # result = embedding_service.search_mongodb(body_search,database["embedding"], model)
# # print(result)
# # ollama_response = ollama_client.chat(name_model, messages=[{'role': 'user', 'content': body_search["query"]}])
# # print(ollama_response)
# def create_context_resource(results: List[Dict], max_results: int = 3) -> str:
#     """Crea un contexto estructurado a partir de los resultados."""
#     context_items = []
#     for i, row in enumerate(results[:max_results], 1):
#         context_items.append(
#             f"{row['content']} \n"
#         )
#     return "\n\n".join(context_items)

# def ollama_chat(query, collection, model):
#     consulta = query
#     print(f"Consulta: {consulta}")
#     semantic_search = requests.post("http://localhost:5000/search", json={"query": consulta, "collection": "embedding"})
#     # async with httpx.AsyncClient() as client:
#     #     semantic_search = await client.post(
#     #         "http://api-mongo:5000/search", 
#     #         json={"query": consulta, "collection": "embedding"}
#     #     )

#     while(not semantic_search.ok):
#         print("Esperando respuesta de la consulta...")
        
    

#     #---------------------------------------------------
    
#     semantic_search = semantic_search.json()
#     print(f"Semantic search: {semantic_search}")
#     if max(semantic_search, key=lambda x: x["score"])["score"] < 0.5:
#         print("No se han encontrado resultados relacionados")
#         #--------------------------------MODIFICAR ESTA RESPUESTA PARA QUE SEA MÁS AMIGABLE--------------------------------
#         respuesta = "No se han encontrado resultados relacionados"
#         return {"text": respuesta}
#     else:
#         context = create_context_resource(semantic_search, max_results=3)
#         augmented_prompt = f"""A partir de la siguiente información del contexto, ¿podrías responder a la query del usuario? Respondela unicamente si se trata de Mobbeel.
# Contexto:
# {context}
# Query:
# {consulta}"""
#         respuesta:ChatResponse = ollama_client.chat(name_model,messages=[{'role': 'user', 'content': augmented_prompt}])
#         print(f"Respuesta: {respuesta.message.content}")
#     # ollama.push(model='example', to=self.model)
#     return {"text": respuesta.message.content}

# respuesta = ollama_chat(query, None,None)
# print(respuesta)