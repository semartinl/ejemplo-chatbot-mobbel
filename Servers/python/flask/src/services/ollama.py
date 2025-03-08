from typing import Dict, List
import ollama
from ollama import ChatResponse, Client
import requests
def create_context(results: List[Dict], max_results: int = 3) -> str:
    """Crea un contexto estructurado a partir de los resultados."""
    context_items = []
    for i, row in enumerate(results[:max_results], 1):
        context_items.append(
            f"{row['answer']} \n"
        )
    return "\n\n".join(context_items)



class OllamaChat:
    def __init__(self, model):
        self.model = model
        self.client = Client("http://ollama:11434")
        self.client.pull(model)
        # self.chat = self.client.create(model='example', from_=model, system="You are a virtual assistant from Mobbeel company. Dont answer any personal questions.")
        # ollama.pull(model='example', from_=model)
        
        
    def ollama_chat(self, body, collection):
        consulta = body["messages"][-1]["text"]

        print(f"Consulta: {consulta}")
        semantic_search = requests.post("http://api-mongo:5000/search", json={"query": consulta, "collection": "embedding"})

        semantic_search = semantic_search.json()
        print(f"Semantic search: {semantic_search}")
        if max(semantic_search, key=lambda x: x["score"])["score"] < 0.7:
            print("No se han encontrado resultados relacionados")
            #--------------------------------MODIFICAR ESTA RESPUESTA PARA QUE SEA MÁS AMIGABLE--------------------------------
            respuesta = "No se han encontrado resultados relacionados"
            return {"text": respuesta}
        else:
            context = create_context(semantic_search, max_results=3)
            augmented_prompt = f"""A partir de la siguiente información del contexto, ¿podrías responder a la query del usuario? Respondela unicamente si se trata de Mobbeel.
    Contexto:
    {context}
    Query:
    {consulta}"""
            respuesta:ChatResponse = self.client.chat(self.model,messages=[{'role': 'user', 'content': augmented_prompt}])
            print(f"Respuesta: {respuesta.message.content}")
        # ollama.push(model='example', to=self.model)
        return {"text": respuesta.message.content}