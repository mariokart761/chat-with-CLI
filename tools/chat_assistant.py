from openai import OpenAI
from g4f.client import Client
import os
from termcolor import colored

class ChatAssistant:
    """
    api_key:
        建議設置api_key為環境變數:
        Windows : `setx OPENAI_API_KEY "your_api_key_here"`
        MacOS/Linux : `export OPENAI_API_KEY="your_api_key_here"`
        
    model:
        官方文檔：https://platform.openai.com/docs/models
        
    initial_messages:
        可預先配置一些prompt
        e.g. `initial_messages=[{"role": "system", "content": "You are an IT expert."}]`
    """
    
    def __init__(self, api_key: str = None, init_messages: list = None):
        self._client = OpenAI(api_key=api_key or os.environ.get('OPENAI_API_KEY'))
        self.global_msg = init_messages or []
        self._model = 'gpt-4o-mini'
        
    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        if not isinstance(value, OpenAI) and not isinstance(value, Client):
            raise ValueError("client 必須是 OpenAI 或 G4F 實例")
        self._client = value
        
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    def get_openai_response(self, messages: list):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response

    def get_ast_msg(self, user_msg: str) -> str:
        self.global_msg.append({"role": "user", "content": user_msg})
        gpt_response = self.get_openai_response(self.global_msg)
        ast_msg = gpt_response.choices[0].message.content
        self.global_msg.append({"role": "assistant", "content": ast_msg})
        
        return ast_msg

    def save_to_file(self, content, filename: str = 'output.md'):
        if not os.path.exists('saved_file'):
            os.makedirs('saved_file')
        with open(f'./saved_file/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        print(colored(f"\n[INFO] Assistant回覆已存至 ./saved_file/{filename}","light_cyan"))
        

class ChatInterface:
    COMAND = {
        "EXIT": "--exit",
        "SAVE": "--save",
        # "BACK": "--back",
        # "SWITCH_MODEL" : "--model"
    }

    def __init__(self, assistant: 'ChatAssistant'):
        self.assistant = assistant
        self.assistant_response = None

    def chat_with_cli(self):
        while True:
            user_input = input(colored("\nYou: \n", "blue"))
            if user_input.lower() == self.COMAND["EXIT"]:
                break
            elif user_input.lower().startswith(self.COMAND["SAVE"]):
                if self.assistant_response:
                    filename = user_input.split(" ")[1] if len(user_input.split(" ")) > 1 else "output.md"
                    self.assistant.save_to_file(content=self.assistant_response, filename=filename)
                else:
                    print(colored("[INFO] 尚未有Assistant回覆可供儲存", "red"))
                continue

            self.assistant_response = self.assistant.get_ast_msg(user_input)
            print(colored("\nAssistant: \n", "green") + self.assistant_response)
