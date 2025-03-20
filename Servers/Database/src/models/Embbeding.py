# Crear una clase o interfaz que utilice nuestra base de datos para recuperar información de documentos, con las siguientes propiedades:
# 1. id: string;
# 2. resourceId: mongoose.Types.ObjectId;
# 3. content: string;
# 4.  embedding: number[];


from typing import List
from pydantic import BaseModel
import json
class Embbeding:
    def __init__(self, id: str, resourceId: str, content: str, embedding_text: List[int], embedding_keywords:List[int]):
        self.id = id
        self.resourceId = resourceId
        self.content = content
        # self.keys_embedding = embedding
        # self.keys = 
        self.embedding_text= embedding_text
        self.embedding_keywords = embedding_keywords

    def to_json(self):
        """Convierte el objeto Embbeding a un diccionario y luego lo serializa a JSON."""
        return json.dumps(self.__dict__, indent=4)  # Usamos self.__dict__ para acceder a los atributos


    
    