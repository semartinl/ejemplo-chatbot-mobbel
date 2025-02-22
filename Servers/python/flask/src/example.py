import models.SemanticSearch as ss
import models.ResponseGenerator as rg
import pandas as pd

semantic_search = ss.SemanticSearchEnhancer()

datos_pandas = pd.read_json("datos.json")
semantic_search.prepare_data_in_mongo(datos_pandas)

print(semantic_search)

def add_answer_embedding(df: pd.DataFrame, embeddings: list):
    """
    Añade una columna 'answer_embedding' a un DataFrame con los valores proporcionados.
    
    :param df: DataFrame original.
    :param embeddings: Lista de valores de embeddings (debe coincidir en longitud con el DataFrame).
    :return: DataFrame con la nueva columna agregada.
    """
    if len(df) != len(embeddings):
        raise ValueError("La cantidad de embeddings no coincide con la cantidad de filas en el DataFrame")
    
    df["answer_embedding"] = embeddings
    return df

# Ejemplo de uso
data = {"id": [1, 2, 3,4], "text": ["Hola", "Mundo", "Pandas", "Python"]}
df = pd.DataFrame(data)
embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9],[0,0,0]]

df = add_answer_embedding(df, embeddings)
print(df)
