import PyPDF2
import re

from bson import ObjectId
from flask import jsonify

class QA_Documents:
    def get_qa_documents(self, collection):
        answers = list(collection.find())
        for answer in answers:
            answer["_id"] = str(answer["_id"])
        return jsonify(answers)
    def get_qa_document_by_id(self, body, collection, id):
        answer = collection.find_one({"_id": ObjectId(id)})
        if answer:
            answer["_id"] = str(answer["_id"])
            return jsonify(answer)
        return jsonify({"error": "Not found"}), 404
    
    def create_qa_document(self, body, collection, model_embedding):
        if "question" not in body or "answer" not in body:
            return jsonify({"error": "Missing fields"}), 400
        
        embedding = model_embedding.encode(body["answer"]).tolist()
        body["semantic_embedding"] = embedding
        result = collection.insert_one(body)
        return jsonify({"_id": str(result.inserted_id)})
    
    def update_qa_document(self, body, collection, id, model_embedding):
        if "question" not in body or "answer" not in body:
            return jsonify({"error": "Missing fields"}), 400
        
        embedding = model_embedding.encode(body["answer"]).tolist()
        body["semantic_embedding"] = embedding
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": body})
        
        if result.matched_count:
            return jsonify({"message": "Updated successfully"})
        return jsonify({"error": "Not found"}), 404
    
    def delete_qa_document(self, collection, id):
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Deleted successfully"})
        return jsonify({"error": "Not found"}), 404
    
    def read_pdf(file_path: str) -> str:
        """Lee un archivo PDF y devuelve su contenido formateado."""
        text = []
        
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text_page = page.extract_text()
                    text_page = text_page.replace("\n", "")
                    text.append(text_page)
                    # text.append(page.extract_text() or "")  # Extraer texto de cada página
        except Exception as e:
            return f"Error al leer el PDF: {str(e)}"
        
        return "\n".join(text).strip()

    def extract_questions_and_answers(pdf_path):
        questions_answers = []
        
        with open(f"./{pdf_path}", "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        # Expresión regular para capturar preguntas numeradas y sus respuestas
        pattern = re.compile(r"(\d+)\.\s?(.*?)\?\s*(.*?)(?=\n\d+\.| \Z)", re.S)
        
        matches = pattern.findall(text)
        
        for match in matches:
            question_number, question_text, answer_text = match
            question_text = question_text.strip()
            question_text = question_text.replace("\n", "")

            answer_text = answer_text.strip()
            answer_text = answer_text.replace("\n", "")
            
            questions_answers.append({"question": question_text.strip(), "answer": answer_text})
        
        return questions_answers
    
    def add_document_to_mongo(self,database, collection_name,pdf_path, embeddings_model):
        """
        Añade un documento a MongoDB con su respectivo embedding semántico.
        El documento debe de tener una estructura similar a la siguiente:
        
        1. Pregunta 1?
        Respuesta 1
        
        2. Pregunta 2?
        Respuesta 2
        
        ..."""
        collection = database[collection_name]

        datos = self.extract_questions_and_answers(pdf_path)
        print(datos)

        for data in datos:
            question = data["question"]
            answer = data["answer"]

            embedding = embeddings_model.encode(question)
            document = {"question": question, "answer":answer, "semantic_embedding": embedding.tolist()}
            print(f"Insertando documento: {document}")
            collection.insert_one(document)

    texto = read_pdf("Preguntas_cuestionario_resumidas.pdf")
    print(texto)