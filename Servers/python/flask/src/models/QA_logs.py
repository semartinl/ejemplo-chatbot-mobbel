from datetime import datetime
from typing import List
import pandas as pd
import os
import json

class Score:
    def __init__(self, score: float, name: str):
        self.score = score
        self.name = name
    
    
class Log:
    def __init__(self, contexto, query, expected_answer: str = "", model_answer:str ="", scores: List[Score] = []):
        self.contexto = contexto
        self.query = query
        self.expected_answer= expected_answer
        self.model_answer = model_answer
        self.scores = scores

    def to_dict(self):
        return {
            "contexto": self.contexto,
            "query": self.query,
            "expected_answer": self.expected_answer,
            "model_answer": self.model_answer,
            "scores": [score.__dict__ for score in self.scores],
            "timestamp": datetime.now().isoformat()
        }


def append_log_to_csv(log, filename="logs.csv"):
    """
    Añade un nuevo objeto Log al archivo CSV existente. Si el archivo no existe, lo crea con encabezados.

    :param log: Objeto Log que se añadirá.
    :param filename: Nombre del archivo CSV donde se guardarán los logs.
    """
    log_dict = log.to_dict()
    df = pd.DataFrame([log_dict])

    # Verifica si el archivo ya existe para manejar el encabezado
    file_exists = os.path.isfile(filename)

    df.to_csv(filename, mode='a', index=False, header=not file_exists, columns=["contexto", "query", "expected_answer", "model_answer", "scores", "timestamp"])

    print(f"Log añadido a {filename}")

def append_log_to_json(log, filename="logs.json"):
    """
    Añade un nuevo objeto Log a un archivo JSON existente. Si el archivo no existe, lo crea.

    :param log: Objeto Log que se añadirá.
    :param filename: Nombre del archivo JSON donde se guardarán los logs.
    """
    log_dict = log.to_dict()

    # Si el archivo ya existe, cargar los datos previos
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                logs = json.load(file)
                if not isinstance(logs, list):
                    logs = []  # En caso de que el archivo tenga un formato incorrecto
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    # Agregar el nuevo log
    logs.append(log_dict)

    # Guardar nuevamente en JSON
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4, ensure_ascii=False)

    print(f"Log añadido a {filename}")

def save_logs_to_csv(logs, filename="logs.csv"):
    """
    Guarda una lista de objetos Log en un archivo CSV.

    :param logs: Lista de objetos Log.
    :param filename: Nombre del archivo CSV donde se guardarán los logs.
    """
    if not logs:
        print("No hay logs para guardar.")
        return
    
    df = pd.DataFrame([logs.to_dict()])
    print(logs.to_dict())
    # Guardar en CSV, asegurando el orden correcto de las columnas
    df.to_csv(filename, index=False, columns=["contexto", "query", "expected_answer", "model_answer", "score", "timestamp"])

    print(f"Logs guardados en {filename}")