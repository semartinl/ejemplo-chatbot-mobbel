from requests.exceptions import ConnectionError

from services.custom import Custom

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
import database as dbase

from services.ollama import OllamaChat
import torch
import nltk
import asyncio
import pandas as pd
# ------------------ SETUP ------------------

load_dotenv()

database = dbase.conexionMongoDB()

app = Flask(__name__)

# this will need to be reconfigured before taking the app to production
cors = CORS(app)

# ------------------ EXCEPTION HANDLERS ------------------

# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500

@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500


# ------------------ OLLAMA API ------------------
ollama = OllamaChat("qwen2.5:0.5b")
@app.route("/ollama-chat", methods=["POST"])
def ollama_api_chat():
    body = request.json
    # response = asyncio.run(ollama.ollama_chat(body, database["embedding"], SEMANTIC_SEARCH.model))
    response= ollama.ollama_chat(body, database["embedding"])
    return response
# ------------------ CUSTOM API ------------------

custom = Custom()

# @app.route("/chat", methods=["POST"])
# def chat():
#     body = request.json
#     return custom.chat(body, CHATBOT, database["answer"])


@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    return custom.chat_stream(body)

@app.route("/files", methods=["POST"])
def files():
    return custom.files(request)


# ------------------ START SERVER ------------------

if __name__ == "__main__":
    # app.run(port=8080)
    app.run(host="0.0.0.0", port=8080,debug=True)
