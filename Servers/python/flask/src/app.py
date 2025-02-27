from requests.exceptions import ConnectionError
from services.huggingFace import HuggingFace
from services.stabilityAI import StabilityAI
from services.custom import Custom
from services.openAI import OpenAI
from services.cohere import Cohere
from flask import Flask, request
from dotenv import load_dotenv
from flask_cors import CORS
import database as dbase
from models.ChatbotRAG import ChatbotRAG
from models.DialogueController import DialogueController
from models.ResponseGenerator import ResponseGenerator
from models.SemanticSearch import SemanticSearchEnhancer
from services.huggingFace import loginHuggingFace
import torch
import nltk
import pandas as pd
# ------------------ SETUP ------------------

load_dotenv()

database = dbase.conexionMongoDB()


# loginHuggingFace()
# CHATBOT_MODEL = os.getenv("CHATBOT_MODEL")
device = ("cuda" if torch.cuda.is_available() else "cpu")
SYSTEM_PROMPT = """*Eres un asistente virtual experto en Mobbeel, una empresa especializada en verificación de identidad digital. Tu única función es responder, de manera precisa, amable y cortés, preguntas relacionadas con Mobbeel, sus soluciones y servicios. No debes responder preguntas que no estén relacionadas con la empresa.
Tu conocimiento se basa en información sobre Mobbeel.

Si un usuario hace una pregunta fuera de este ámbito, responde con amabilidad que solo puedes proporcionar información sobre Mobbeel y sus servicios. Usa un tono profesional, pero cercano. Asegúrate de que todas tus respuestas sean claras, concisas y útiles. Si no tienes la información exacta, evita inventar y, en su lugar, explica que no puedes responder con certeza.*"""
CONTROLLER = DialogueController(assistant_token="<|assistant|>", system_prompt=SYSTEM_PROMPT)

# Descarga de recursos necesarios
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
SEMANTIC_SEARCH = SemanticSearchEnhancer(database=database)


RESPONSE_ENGINE = ResponseGenerator()
CHATBOT = ChatbotRAG(controller=CONTROLLER, device_setup=device,response_engine=RESPONSE_ENGINE, semantic_search=SEMANTIC_SEARCH)

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

# ------------------ CUSTOM API ------------------

custom = Custom()

@app.route("/chat", methods=["POST"])
def chat():
    body = request.json
    return custom.chat(body, CHATBOT, database["answer"])


@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    return custom.chat_stream(body)

@app.route("/files", methods=["POST"])
def files():
    return custom.files(request)

# ------------------ OPENAI API ------------------

open_ai = OpenAI()

@app.route("/openai-chat", methods=["POST"])
def openai_chat():
    body = request.json
    return open_ai.chat(body)

@app.route("/openai-chat-stream", methods=["POST"])
def openai_chat_stream():
    body = request.json
    return open_ai.chat_stream(body)

@app.route("/openai-image", methods=["POST"])
def openai_image():
    files = request.files.getlist("files")
    return open_ai.image_variation(files)

# ------------------ HUGGING FACE API ------------------

huggingFace = HuggingFace()

@app.route("/huggingface-conversation", methods=["POST"])
def hugging_face_conversation():
    body = request.json
    return huggingFace.conversation(body, SEMANTIC_SEARCH)

@app.route("/huggingface-image", methods=["POST"])
def hugging_face_image_classification():
    files = request.files.getlist("files")
    return huggingFace.image_classification(files)

@app.route("/huggingface-speech", methods=["POST"])
def hugging_face_speech_recognition():
    files = request.files.getlist("files")
    return huggingFace.speech_recognition(files)

# ------------------ STABILITY AI API ------------------

stability_ai = StabilityAI()

@app.route("/stability-text-to-image", methods=["POST"])
def stabilityai_text_to_image():
    body = request.json
    return stability_ai.text_to_image(body)

@app.route("/stability-image-to-image", methods=["POST"])
def stabilityai_image_to_image():
    return stability_ai.image_to_image(request)

@app.route("/stability-image-upscale", methods=["POST"])
def stabilityai_image_to_image_upscale():
    files = request.files.getlist("files")
    return stability_ai.image_to_image_upscale(files)

# ------------------ COHERE API ------------------

cohere = Cohere()

@app.route("/cohere-chat", methods=["POST"])
def cohere_chat():
    body = request.json
    return cohere.chat(body)

@app.route("/cohere-generate", methods=["POST"])
def cohere_generate_text():
    body = request.json
    return cohere.generate_text(body)

@app.route("/cohere-summarize", methods=["POST"])
def cohere_summarize_text():
    body = request.json
    return cohere.summarize_text(body)

# ------------------ START SERVER ------------------

if __name__ == "__main__":
    app.run(port=8080)
