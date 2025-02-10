import requests
import os

# Make sure to set the HUGGING_FACE_API_KEY environment variable in a .env file (create if does not exist) - see .env.example

class HuggingFace:
    def conversation(self, body):
        env = os.getenv("HUGGING_FACE_API_KEY")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + env
        }
        # Text messages are stored inside request body using the Deep Chat JSON format:
        # https://deepchat.dev/docs/connect
        conversation_body = self.create_conversation_body(body["messages"])
        #HASTA AQUÍ LLEGA
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill", json={"inputs": conversation_body["inputs"]["text"],  "wait_for_model": True}, headers=headers)
        json_response = response.json()

        print(f"Respuesta a la api de hugging Face: {json_response}")
        if "error" in json_response:
            raise Exception(json_response["error"])
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": json_response[0]["generated_text"]}

    @staticmethod
    def create_conversation_body(messages):
        text = messages[-1]["text"]
        print(f"Texto: {text}")
        previous_messages = messages[:-1]
        print(f"Previosu messages {previous_messages}")
        if not text:
            return None
        print("Pasamos el if \n")
        past_user_inputs = [message["text"] for message in previous_messages if message["role"] == "user"]
        print(f"Historial del usuario: {past_user_inputs} \n")
        generated_responses = [message["text"] for message in previous_messages if message["role"] == "ai"]
        print(f"Historial del agente: {generated_responses} \n")
        respuesta = {"inputs": {"past_user_inputs": past_user_inputs, "generated_responses": generated_responses, "text": text}, "wait_for_model": True}
        print(f"Respuesta de la función create_conversatio_body: {respuesta} \n")
        return respuesta
    # You can use an example image here: https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/ui/assets/example-image.png
    def image_classification(self, files):
        headers = {
            "Authorization": "Bearer " + os.getenv("HUGGING_FACE_API_KEY")
        }
        # Files are stored inside a files object
        # https://deepchat.dev/docs/connect
        data=files[0].read()
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/vit-base-patch16-224", data=data, headers=headers)
        json_response = response.json()
        if "error" in json_response:
            raise Exception(json_response["error"])
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": json_response[0]["label"]}
    
    # You can use an example audio file here: https://github.com/OvidijusParsiunas/deep-chat/blob/main/example-servers/ui/assets/example-audio.m4a
    def speech_recognition(self, files):
        headers = {
            "Authorization": "Bearer " + os.getenv("HUGGING_FACE_API_KEY")
        }
        # Files are stored inside a files object
        # https://deepchat.dev/docs/connect
        data=files[0].read()
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/wav2vec2-large-960h-lv60-self", data=data, headers=headers)
        json_response = response.json()
        if "error" in json_response:
            raise Exception(json_response["error"])
        # Sends response back to Deep Chat using the Response format:
        # https://deepchat.dev/docs/connect/#Response
        return {"text": json_response["text"]}
