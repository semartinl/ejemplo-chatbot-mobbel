from flask import jsonify
from functions.TextProcessor import TextPreprocessor
from sklearn.metrics.pairwise import cosine_similarity
class Embedding_service:

    def search_mongodb(self,body, collection_qa, embbeding_model):
        """
        Busca documentos en MongoDB utilizando embeddings semánticos.
        
        :param query: Texto de la consulta.
        :return: Lista de documentos que coinciden con la consulta.
        """
        query = body["query"]
        # Limpiamos la query en tokens y la convertimos en un embedding
        query_preprocessed = TextPreprocessor.preprocess(query)
        query_embedding = embbeding_model.encode(query)
        query_embedding_keywords = embbeding_model.encode(query_preprocessed)

        #la siguiente consulta busca los 3 documentos más similares a la consulta.La 2 consulta es para recuperar los campos que se desean mostrar. En este caso, se muestra el campo de "answer"
        results_keywords = collection_qa.aggregate([{
        "$vectorSearch": {
        "index": "vector_index_resources",
        "path": "embedding_keywords",
        "queryVector": query_embedding_keywords.tolist(),
        "numCandidates": 150,
        "limit": 3
            }
        }, {
            "$project": {
                "_id": 0,
                "content": 1,
                "embedding_text": 1,
                "embedding_keywords": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    
        ])

        results = collection_qa.aggregate([{"$vectorSearch": {
        "index": "vector_index_resources_text",
        "path": "embedding_text",
        "queryVector": query_embedding.tolist(),
        "numCandidates": 200,
        "limit": 3
            }
        }, {
            "$project": {
                "_id": 0,
                "content": 1,
                "embedding_text": 1,
                "embedding_keywords": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    
        ])
        
        results = results.to_list()
        print(f"Distancia del coseno de la consulta: {cosine_similarity([query_embedding.tolist()], [results[0]['embedding_text']])[0]}")
        print(f"Distancia del coseno de las palabras claves: {cosine_similarity([query_embedding_keywords.tolist()], [results[0]['embedding_keywords']])[0]}")

        # print(f"Distancia del coseno de la consulta: {cosine_similarity([query_embedding.tolist()], [results[0]['embedding_text']])[0]}")
        # print(f"Distancia del coseno de las palabras claves: {cosine_similarity([query_embedding_keywords.tolist()], [results[0]['embedding_keywords']])[0]}")
        
        results_list = list(results_keywords)  # Convertimos el cursor a una lista
        if results_list:  # Verificamos que haya elementos
            print(f"Distancia del coseno de la consulta 2: {cosine_similarity([query_embedding.tolist()], [results_list[0]['embedding_text']])[0]}")
            print(f"Distancia del coseno de las palabras claves 2: {cosine_similarity([query_embedding_keywords.tolist()], [results_list[0]['embedding_keywords']])[0]}")
        else:
            print("No se encontraron resultados en MongoDB.")
        # return {"response" : results.to_list()}
        return jsonify(results)
