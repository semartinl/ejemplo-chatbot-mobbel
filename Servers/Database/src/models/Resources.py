# Crear una clase o interfaz que utilice nuestra base de datos para recuperar información de documentos, con las siguientes propiedades:
# 1. id: string;
# 2. resourceId: mongoose.Types.ObjectId;
# 3. content: string;
# 4.  embedding: number[];
from datetime import date
from pydantic import BaseModel
class Resource(BaseModel):
    id: int
    content: str
    createdAt: str
    updatedAt: str


    
