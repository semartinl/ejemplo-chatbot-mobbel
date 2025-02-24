import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
class Chatbot:

    def __init__(self, controller, device_setup, chatbot_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", cache_dir="./models-ia/TinyLlama-1.1B-Chat-v1.0"):
        self.tokenizer = AutoTokenizer.from_pretrained(chatbot_model)
        self.model = AutoModelForCausalLM.from_pretrained(
            chatbot_model,
            torch_dtype = torch.float32 if device_setup == "mps" else (torch.float16 if torch.cuda.is_available() else torch.float32),
            cache_dir=cache_dir,
            local_files_only=False
        ).to(device_setup)
        self.model_device = device_setup
        self.dialogue_controller = controller

    def __run_prompt(self, prompt, do_sample, temperature, top_p, max_length, show_prompt):
        formatted_prompt = self.tokenizer.apply_chat_template(conversation=prompt, tokenize=False, return_dict=False, add_generation_prompt=True)
        
        # Tokenizar
        inputs = self.tokenizer(formatted_prompt, max_length=max_length, truncation=True, return_tensors="pt")
        inputs = {k: v.to(self.model_device) for k, v in inputs.items()}

        # Muestra infomacion de log
        if show_prompt:
          print(formatted_prompt)
          print("--- Token size: ---")
          [print("\t", k, ": ", len(v[0])) for k, v in inputs.items()]
          print("-------------------")

        # Generar respuesta
        outputs = self.model.generate(
            **inputs,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Decodificar y limpiar respuesta
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)



    def answer(self, user_prompt, do_sample=True, temperature=0.1, top_p=0.9, max_length=2047, show_prompt=False):
        # Actualiza el prompt
        prompt = self.dialogue_controller.add_user_prompt(user_prompt)
        print("Prompt: ",
              prompt)
        # Resolver prompt
        answer = self.__run_prompt(prompt, do_sample, temperature, top_p, max_length, show_prompt)
        # Actualiza el prompt con la respuesta del asistente
        self.dialogue_controller.add_assistant_prompt(answer)
        return answer
    
