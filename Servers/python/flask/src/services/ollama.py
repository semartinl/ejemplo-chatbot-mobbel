from typing import Dict, List
from flask import jsonify
from models.QA_logs import Log, save_logs_to_csv, append_log_to_json, Score
import pandas as pd
import ollama
import asyncio
from ollama import ChatResponse, Client
import requests
def create_context_resource(results: List[Dict], max_results: int = 3) -> str:
    """Crea un contexto estructurado a partir de los resultados."""
    context_items = []
    for i, row in enumerate(results[:max_results], 1):
        context_items.append(
            f"{row['content']} \n"
        )
    return "\n\n".join(context_items)



class OllamaChat:
    def __init__(self, model):
        self.model = model
        self.client = Client("http://localhost:11434")
        # self.client = Client("http://ollama:11434")
        self.client.pull(model)
        # self.chat = self.client.create(model='example', from_=model, system="You are a virtual assistant from Mobbeel company. Dont answer any personal questions.")
        # ollama.pull(model='example', from_=model)
        
        
    def ollama_chat(self, body, collection):
        consulta = body["messages"][-1]["text"]

        print(f"Consulta: {consulta}")
        semantic_search = requests.post("http://localhost:5000/search", json={"query": consulta, "collection": "embedding"})
        
        semantic_search = semantic_search.json()
        # print(f"Semantic search: {semantic_search}")
        if max(semantic_search, key=lambda x: x["score"])["score"] < 0.5:
            print("No se han encontrado resultados relacionados")
            #--------------------------------MODIFICAR ESTA RESPUESTA PARA QUE SEA MÁS AMIGABLE--------------------------------
            respuesta = "No se han encontrado resultados relacionados"
            return {"text": respuesta}
        else:
            context = create_context_resource(semantic_search, max_results=3)
            augmented_prompt = f"""A partir de la siguiente información del contexto, ¿podrías responder a la query del usuario?
    Contexto:
    {context}
    Query:
    {consulta}"""
            respuesta:ChatResponse = self.client.chat(self.model,messages=[{'role': 'user', 'content': augmented_prompt}])
            print(f"Respuesta: {respuesta.message.content}")

        list_scores = []
        for result in semantic_search:
            list_scores.append(Score(score=result["score"], name="Vector Search Score"))
        log = Log(contexto=context, query=consulta, model_answer=respuesta.message.content, scores=list_scores)

        # Guardar log en CSV
        # save_logs_to_csv(log, filename="logs.csv")

        # Guardar log en JSON
        append_log_to_json(log, filename="logs.json")
        

        
        # ollama.push(model='example', to=self.model)
        return {"text": respuesta.message.content}