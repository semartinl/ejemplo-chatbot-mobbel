from flask import Response
import time
import json
from database import search_mongodb

class Custom:
    def chat(self, body, chatbot, collection_mongo):
        # Text messages are stored inside request body using the Deep Chat JSON format:
        # https://deepchat.dev/docs/connect
        print(body)
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response

        #Recogemos la consulta del usuario
        consulta = body["messages"][-1]["text"]
        print(f"Consulta: {consulta}")

        #Plasmamos la consulta en nuestro embbeding
        final_results = search_mongodb(query=consulta,collection=collection_mongo, semantic_search=chatbot.semantic_search)
        print(f"Resultados: {final_results}")

        #Comprobamos que los resultados tengan relación con los documentos de la base de datos. Si no hay resultados, se devuelve un mensaje de error
        #Se comprueba si la lista de resultados está vacía, porque mongodb devuelve una lista vacía si no encuentra resultados relacionados.
        if max(final_results, key=lambda x: x["score"])["score"] < 0.6:
            print("No se han encontrado resultados relacionados")
            #--------------------------------MODIFICAR ESTA RESPUESTA PARA QUE SEA MÁS AMIGABLE--------------------------------
            respuesta = "No se han encontrado resultados relacionados"
        else:
            #Generamos la respuesta
            respuesta = chatbot.response_engine.generate_response(consulta, final_results)
            print(f"Respuesta: {respuesta}")
        return {"text": respuesta}

    def chat_stream(self, body):
        # Text messages are stored inside request body using the Deep Chat JSON format:
        # https://deepchat.dev/docs/connect
        print(body)
        response_chunks = "This is a response from a Flask server. Thank you for your message!".split(
            " ")
        response = Response(self.send_stream(response_chunks), mimetype="text/event-stream")
        response.headers["Content-Type"] = "text/event-stream"
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    def send_stream(self, response_chunks, chunk_index=0):
        if chunk_index < len(response_chunks):
            chunk = response_chunks[chunk_index]
            yield f"data: {json.dumps({'text': f'{chunk} '})}\n\n"
            time.sleep(0.07)
            yield from self.send_stream(response_chunks, chunk_index + 1)
        else:
            yield ""

    def files(self, request):
        # Files are stored inside a files object
        # https://deepchat.dev/docs/connect
        files = request.files.getlist("files")
        if files:
            print("Files:")
            for file in files:
                print(file.filename)

            # When sending text messages along with files - they are stored inside the data form
            # https://deepchat.dev/docs/connect
            text_messages = list(request.form.items())
            if len(text_messages) > 0:
                print("Text messages:")
                # message objects are stored as strings and they will need to be parsed (JSON.parse) before processing
                for key, value in text_messages:
                    print(key, value)
        else:
            # When sending text messages without any files - they are stored inside a json
            print("Text messages:")
            print(request.json)

        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": "This is a respone from a Flask server. Thankyou for your message!"}
