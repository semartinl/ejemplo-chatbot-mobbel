# Crear interfaz o clase con las propiedades de 
# 1. Question
# 2. Answer
# La propiedad de embbeding se puede realizar en una tabla a parte, para que se pueda mezclar tanto con documentos directos como preguntars.

import PyPDF2
import re
from pydantic import BaseModel
class QA_documents(BaseModel):
    question:str
    answer:str




def add_document_to_mongo(database, collection_name,pdf_path, embeddings_model):
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