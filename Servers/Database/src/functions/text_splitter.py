import pdfplumber
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
def extraer_texto_pdf_mejorado(ruta_pdf):
    """
    Extrae texto de un archivo PDF manteniendo los espacios correctamente.
    
    :param ruta_pdf: Ruta del archivo PDF
    :return: Texto extraído con espacios corregidos
    """
    texto_completo = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            text_page = pagina.extract_text()
            text_page = text_page.replace("\n", " ")
            texto_completo.append(text_page)  # Agregar un salto de línea entre páginas

    return texto_completo

palabras_evitar = ["www.mobbeel.com", "slide", "page", "copyright", "address", "phone", "email", "contenido", "tabla de"]

def extraer_texto_con_pdfplumber(pdf_path):
    """
    Extrae texto de un PDF eliminando contenido irrelevante como portada, tabla de contenido y pies de página.
    """
    texto_extraido = []
    with pdfplumber.open(pdf_path) as pdf:
        for num_pagina, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()
            
            if texto:
                # Filtrar contenido irrelevante como URLs, contacto, copyright
                lineas = texto.split("\n")
                lineas_filtradas = [
                    linea for linea in lineas if not any(
                        excl in linea.lower() for excl in palabras_evitar
                    )
                ]
                
                # Excluir portada y tabla de contenido (primeras 2 páginas)
                if num_pagina > 1:
                    texto_extraido.append("\n".join(lineas_filtradas))
    
    return "\n\n".join(texto_extraido)

def extraer_palabras_chunks(texto: str, max_length: int = 1000, contexto:int = 100) -> list:
    """Divide el texto en chunks de un tamaño máximo de "max_length" palabras.

    :param texto: Texto a dividir.
    :param max_length: Longitud máxima de los chunks.
    :param contexto: Longitud de contexto para dividir el texto.
    """
    chunks = []
    palabras = texto.split()
    chunk = ""
    for palabra in palabras:
        if len(chunk) + len(palabra) < max_length:
            
            chunk += palabra + " "
        else:
            chunks.append(chunk.replace("\n", " ").strip())
            chunk = palabra + " "
    chunks.append(chunk.strip())

    return chunks

def extraer_frases_chunks(texto: str, max_length: int = 1000, contexto:int = 100) -> list:
    """Divide el texto en chunks de un tamaño máximo. Aun falta por implementar el contexto.
    
    :param texto: Texto a dividir.
    :param max_length: Longitud máxima de los chunks.
    :param contexto: Longitud de contexto para dividir el texto.
    """
    chunks = []
    frases = texto.split(".")
    chunk = ""
    for frase in frases:
        if len(chunk) + len(frase) < max_length:
            
            chunk += frase + "."
        else:
            chunks.append(chunk.replace("\n"," ").strip())
            chunk = frase + "."
    chunks.append(chunk.strip())

    return chunks

def extract_keywords(text: str) -> str:
    """Extrae palabras clave del texto."""
    # Tokenización y eliminación de stopwords
    stop_words = set(stopwords.words('spanish'))
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word not in stop_words]
    return ' '.join(keywords)
# split_text = extraer_texto_con_pdfplumber("C:\\Users\\USUARIO\\Desktop\\Sergio\\Docs-trabajo\\Dossier-Mobbeel 2025.pdf")


# print(extraer_frases_chunks(split_text, max_length=1000)[-3:-1])