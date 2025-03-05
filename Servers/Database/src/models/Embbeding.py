# Crear una clase o interfaz que utilice nuestra base de datos para recuperar información de documentos, con las siguientes propiedades:
# 1. id: string;
# 2. resourceId: mongoose.Types.ObjectId;
# 3. content: string;
# 4.  embedding: number[];


from typing import List


class Embbeding:
    def __init__(self, id:str, resourceId:str, content:str, embedding:List[int]):
        self.id = id
        self.resourceId = resourceId
        self.content = content
        self.embedding = embedding