class DialogueController:

    def __init__(self, system_prompt, assistant_token="<|assistant|>"):
        self.system_prompt = system_prompt
        self.prompt = [ { "role": "system", "content": system_prompt} ]
        self.assistant_token = assistant_token

    def get_prompt(self):
        return self.prompt

    def add_user_prompt(self, user_prompt, role="user"):
        user_prompt_json = { "role": role, "content":  user_prompt}
        self.prompt.append(user_prompt_json)
        return self.prompt

    def add_assistant_prompt(self, assistant_prompt):
        assistant_prompt_exclusive = assistant_prompt.split(self.assistant_token)
        print(f"Assistant promp: {assistant_prompt_exclusive}")
        final_prompt = ""
        if len(assistant_prompt_exclusive) == 2:
            final_prompt = assistant_prompt_exclusive[1]
        self.add_user_prompt(final_prompt, role="assistant")
exported_class = DialogueController