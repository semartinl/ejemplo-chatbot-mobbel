from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List, Dict, Optional
import bitsandbytes as bnb
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import re


class ResponseGenerator:
    """
    Generador de respuestas usando un modelo local pequeño.
    """
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0", cache_dir="./models-ia/TinyLlama-1.1B-Chat-v1.0"):
        """
        Inicializa el generador con un modelo local.
        Args:
            model_name: Nombre del modelo de HuggingFace a usar.
                       Por defecto usa TinyLlama que es ligero pero efectivo.
        """
        print(f"Cargando modelo {model_name}...")
        # config_quantization = bnb.BitsAndBytesConfig(
        #         load_in_4bit=True # Se utiliza la cuantización de 4 bits
        #     )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # usar precisión media para memoria
            cache_dir=cache_dir,
            local_files_only=False,
            device_map="auto" , # automáticamente usa GPU si está disponible
            # quantization_config=config_quantization
        )
        print("Modelo cargado correctamente.")

    def create_context(self, results: List[Dict], max_results: int = 3) -> str:
        """Crea un contexto estructurado a partir de los resultados."""
        context_items = []
        for i, row in enumerate(results[:max_results], 1):
            context_items.append(
                f"{row['answer']} \n"
            )
        return "\n\n".join(context_items)

    def create_prompt(self, query: str, context: str,
                     user_preferences: Optional[Dict] = None) -> str:
        """Crea un prompt estructurado para el modelo."""
        base_prompt = f"""<|system|>
*"Eres un asistente virtual experto en Mobbeel, una empresa especializada en verificación de identidad digital. Tu única función es responder, de manera precisa, amable y cortés, preguntas relacionadas con Mobbeel, sus soluciones y servicios. No debes responder preguntas que no estén relacionadas con la empresa.

Tu conocimiento se basa en información sobre Mobbeel, incluyendo:

Onboarding digital (eKYC/AML).
Firma biométrica.
Autenticación biométrica.
Cumplimiento normativo (KYC, AML, eIDAS, GDPR, etc.).
Prevención del fraude mediante biometría y detección de amenazas.
automatización de procesos.
Integración flexible a través de SDKs, APIs y gateway web.
Certificaciones de seguridad y cumplimiento legal.

Si un usuario hace una pregunta fuera de este ámbito, responde con amabilidad que solo puedes proporcionar información sobre Mobbeel y sus servicios. Usa un tono profesional, pero cercano. Asegúrate de que todas tus respuestas sean claras, concisas y útiles. Si no tienes la información exacta, evita inventar y, en su lugar, explica que no puedes responder con certeza.*

Contexto:
{context}

<|user|>
{query}

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
            prompt = self.create_prompt(query, context, user_preferences)

            # Tokenizar
            inputs = self.tokenizer(prompt, return_tensors="pt")
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

            # Generar respuesta
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

            # Decodificar y limpiar respuesta
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.replace(prompt, "").strip()

            return response

        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"

    def generate_specialized_response(self, query: str, search_results: List[Dict],
                                    response_type: str) -> str:
        """Genera respuestas especializadas según el tipo."""
        try:
            context = self.create_context(search_results)

            type_instructions = {
                'recommendation': """
                Genera una recomendación personalizada de estas películas.
                Explica por qué cada película podría ser interesante.
                """,
                'analysis': """
                Proporciona un análisis detallado de las películas mencionadas.
                Incluye elementos narrativos y temas principales.
                """,
                'comparison': """
                Compara las películas mencionadas, destacando similitudes
                y diferencias en género, estilo y temas.
                """
            }

            prompt = f"""<|system|>
{type_instructions.get(response_type, type_instructions['recommendation'])}

Contexto:
{context}

<|user|>
{query}

<|assistant|>
"""

            return self.generate_response(prompt, search_results)

        except Exception as e:
            return f"Error al generar respuesta especializada: {str(e)}"

