from flask import jsonify


class Embedding_service:

    def search_mongodb(self,body, collection_qa, embbeding_model):
        """
        Busca documentos en MongoDB utilizando embeddings semánticos.
        
        :param query: Texto de la consulta.
        :return: Lista de documentos que coinciden con la consulta.
        """
        query = body["query"]
        
        query_embedding = embbeding_model.encode(query)
        #la siguiente consulta busca los 3 documentos más similares a la consulta.La 2 consulta es para recuperar los campos que se desean mostrar. En este caso, se muestra el campo de "answer"
        results = collection_qa.aggregate([{
        "$vectorSearch": {
        "index": "vector_index_resources",
        "path": "embedding",
        "queryVector": query_embedding.tolist(),
        "numCandidates": 150,
        "limit": 3
            }
        }, {
            "$project": {
                "_id": 0,
                "content": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    
        ])


        # return {"response" : results.to_list()}
        return jsonify(results.to_list())
