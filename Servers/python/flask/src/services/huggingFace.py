from typing import Dict, List
import requests
import os
from huggingface_hub import login
# Make sure to set the HUGGING_FACE_API_KEY environment variable in a .env file (create if does not exist) - see .env.example
def loginHuggingFace ():
    env = os.getenv("HUGGING_FACE_API_KEY_MOBBEEL")
    print("Hugging Face logging")
    login(env)

def create_context(results: List[Dict], max_results: int = 3) -> str:
    """Crea un contexto estructurado a partir de los resultados."""
    context_items = []
    for i, row in enumerate(results[:max_results], 1):
        context_items.append(
            f"{row['answer']} \n"
        )
    return "\n\n".join(context_items)

def augment_prompt(query: str, search_results):
    context = create_context(search_results)
    
    # feed into an augmented prompt
    augmented_prompt = f"""A partir de la siguiente información del contexto, ¿podrías responder a la query del usuario?
Contexto:
{context}
Query: {query}"""
    return augmented_prompt
class HuggingFace:
    def conversation(self, body, semantic_search):
        env = os.getenv("HUGGING_FACE_API_KEY_MOBBEEL")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + env
        }
        # Text messages are stored inside request body using the Deep Chat JSON format:
        # https://deepchat.dev/docs/connect
        query = body["messages"][-1]["text"]


        search_result = semantic_search.search_in_mongo(query, "answer")
        prompt = augment_prompt(query, search_result)

        
        
        conversation_body = self.create_conversation_body(body["messages"])
        #HASTA AQUÍ LLEGA
        print(f"Conversación: {conversation_body}")

        prompt_body = {"inputs": prompt, "wait_for_model": True}
        response = requests.post(
            "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0", json=prompt_body, headers=headers)
        json_response = response.json()

        print(f"Respuesta a la api de hugging Face: {json_response}")
        if "error" in json_response:
            raise Exception(json_response["error"])
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": json_response[0]["generated_text"]}

    @staticmethod
    def create_conversation_body(messages):
        text = messages[-1]["text"]
        print(f"Texto: {text}")
        previous_messages = messages[:-1]
        print(f"Previosu messages {previous_messages}")
        if not text:
            return None
        print("Pasamos el if \n")
        past_user_inputs = [message["text"] for message in previous_messages if message["role"] == "user"]
        print(f"Historial del usuario: {past_user_inputs} \n")
        generated_responses = [message["text"] for message in previous_messages if message["role"] == "ai"]
        print(f"Historial del agente: {generated_responses} \n")
        respuesta = {"inputs": {"past_user_inputs": past_user_inputs, "generated_responses": generated_responses, "text": text}, "wait_for_model": True}
        print(f"Respuesta de la función create_conversatio_body: {respuesta} \n")
        return respuesta
    # You can use an example image here: https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/ui/assets/example-image.png
    def image_classification(self, files):
        headers = {
            "Authorization": "Bearer " + os.getenv("HUGGING_FACE_API_KEY")
        }
        # Files are stored inside a files object
        # https://deepchat.dev/docs/connect
        data=files[0].read()
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/vit-base-patch16-224", data=data, headers=headers)
        json_response = response.json()
        if "error" in json_response:
            raise Exception(json_response["error"])
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": json_response[0]["label"]}
    
    # You can use an example audio file here: https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/ui/assets/example-audio.m4a
    def speech_recognition(self, files):
        headers = {
            "Authorization": "Bearer " + os.getenv("HUGGING_FACE_API_KEY")
        }
        # Files are stored inside a files object
        # https://deepchat.dev/docs/connect
        data=files[0].read()
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h-lv60-self", data=data, headers=headers)
        json_response = response.json()
        if "error" in json_response:
            raise Exception(json_response["error"])
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": json_response["text"]}
