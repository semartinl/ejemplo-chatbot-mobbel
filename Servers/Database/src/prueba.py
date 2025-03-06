import database as dbase
from sentence_transformers import SentenceTransformer
from services.QA_Documents import QA_Documents
from services.Resource_service import Resource_service

database = dbase.conexionMongoDB()

resource_db = Resource_service()
body = {"pdf_path": "C:\\Users\\USUARIO\\Downloads\\Dossier-Mobbeel 2025.pdf"}
model = SentenceTransformer("distiluse-base-multilingual-cased-v1")

resource_db.add_resource(database=database, body=body,model_embedding=model)