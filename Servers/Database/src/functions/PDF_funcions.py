__package__
from typing import List
import PyPDF2
import re
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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


# 📌 Función para dividir el texto en chunks, teniendo en cuenta un tamaño y no las palabras. Es decir, 
# corta las palabras si justo se termina en medio de una palabra. 
def split_text_size(text: str, chunk_size: int = 1024, chunk_overlap: int = 100) -> List[str]:
    """Divide el texto en fragmentos de tamaño definido con superposición opcional."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap  # Superposición entre fragmentos
    return chunks

# 📌 Función para cargar y dividir datos de un PDF
def process_pdf(file_path: str, chunk_size: int):
    """
    Procesa un archivo PDF y divide el texto en fragmentos de un tamaño dado.

    :param file_path: Ruta del archivo PDF.
    :param chunk_size: Número de palabras por fragmento.
    :return: Lista de fragmentos de texto.
    """
    text = ""

    # Leer el PDF
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "

    # Limpiar texto y dividir en palabras
    words = text.split()

    # Generar los fragmentos
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    return chunks

def load_and_split_data(file_path: str) -> List[str]:
    """Carga el PDF, extrae el texto y lo divide en fragmentos."""
    content = read_pdf(file_path)  # Usa tu función ya implementada para extraer el texto
    if "Error" in content:
        return [content]  # Si hay error, devolver el mensaje en una lista
    return split_text_size(content)


