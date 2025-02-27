from typing import Dict, List, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from .ResponseGenerator import ResponseGenerator
from .DialogueController import DialogueController
from .SemanticSearch import SemanticSearchEnhancer
from .Chatbot import Chatbot
class ChatbotRAG:
    def __init__(self, controller,device_setup, chatbot_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", cache_dir="./models-ia/TinyLlama-1.1B-Chat-v1.0", semantic_search:SemanticSearchEnhancer = None, response_engine:ResponseGenerator = None):
        self.chatbot = Chatbot(controller=controller, device_setup=device_setup, chatbot_model=chatbot_model, cache_dir=cache_dir)
        self.semantic_search = semantic_search

    def create_context(self, results: List[Dict], max_results: int = 3) -> str:
        """Crea un contexto estructurado a partir de los resultados."""
        context_items = []
        for i, row in enumerate(results[:max_results], 1):
            context_items.append(
                f"{row['answer']} \n"
            )
        return "\n\n".join(context_items)
    @staticmethod
    def augment_prompt(self, query: str, search_results):
        context = self.create_context(search_results)
        
        # feed into an augmented prompt
        augmented_prompt = f"""A partir de la siguiente información del contexto, ¿podrías responder a la query del usuario?
Contexto:
{context}
Query: {query}"""
        return augmented_prompt
    def create_prompt_manual(self, query: str, context: str,
                     user_preferences: Optional[Dict] = None) -> str:
        """Crea un prompt estructurado para el modelo."""
        base_prompt = f"""<|system|>
*"Eres un asistente virtual experto en Mobbeel, una empresa especializada en verificación de identidad digital. Tu única función es responder, de manera precisa, amable y cortés, preguntas relacionadas con Mobbeel, sus soluciones y servicios. No debes responder preguntas que no estén relacionadas con la empresa.

Tu conocimiento se basa en información sobre Mobbeel, incluyendo:

Si un usuario hace una pregunta fuera de este ámbito, responde con amabilidad que solo puedes proporcionar información sobre Mobbeel y sus servicios. Usa un tono profesional, pero cercano. Asegúrate de que todas tus respuestas sean claras, concisas y útiles. Si no tienes la información exacta, evita inventar y, en su lugar, explica que no puedes responder con certeza.*

<|user|> 
A partir de la siguiente información del contexto, ¿podrías responder a la query del usuario?
Contexto:
{context}
Query: {query}

<|assistant|>
"""
        # formatted_prompt = self.tokenizer.apply_chat_template(conversation=base_prompt, tokenize=False, return_dict=False, add_generation_prompt=True)
        

        return base_prompt
    
    def generate_response(self, query: str, search_results: List[Dict],
                         user_preferences: Optional[Dict] = None,
                         max_length: int = 1000) -> str:
        """Genera una respuesta usando el modelo local."""
        try:
            # Crear contexto y prompt
            context = self.create_context(search_results)
            prompt = self.create_prompt_manual(query, context, user_preferences)

            # Tokenizar
            inputs = self.chatbot.tokenizer(prompt, return_tensors="pt")
            inputs = {k: v.to(self.chatbot.model.device) for k, v in inputs.items()}

            # Generar respuesta
            outputs = self.chatbot.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.chatbot.tokenizer.eos_token_id
            )

            # Decodificar y limpiar respuesta
            response = self.chatbot.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.replace(prompt, "").strip()

            return response

        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"


    def generate_response_database(self, query: str,
                         max_length: int = 1000, collection_mongo_name="answer") -> str:
        """Genera una respuesta usando el modelo local."""
    
        final_results = self.semantic_search.search_in_mongo(query=query,collection_name=collection_mongo_name)
        
        #Comprobamos que los resultados tengan relación con los documentos de la base de datos. Si no hay resultados, se devuelve un mensaje de error
        #Se comprueba si la lista de resultados está vacía, porque mongodb devuelve una lista vacía si no encuentra resultados relacionados.
        
        if max(final_results, key=lambda x: x["score"])["score"] < 0.7:
            print("No se han encontrado resultados relacionados")
            #--------------------------------MODIFICAR ESTA RESPUESTA PARA QUE SEA MÁS AMIGABLE--------------------------------
            response = "No se han encontrado resultados relacionados"
        else:
            
            # context = self.create_context(final_results)
            # prompt = self.create_prompt_manual(query, context)
            # response = self.generate_response(query, final_results)
            prompt = self.augment_prompt(self,query=query, search_results=final_results)
            response = self.chatbot.answer(user_prompt=prompt,temperature=0.7, top_p=0.9, max_length=max_length, show_prompt=True)
            # response = self.chatbot.answer(user_prompt=f"{context} \n # {query}",temperature=0.7, top_p=0.9, max_length=max_length, show_prompt=True)
            
        return response

