from openai import OpenAI
from g4f.client import Client
from termcolor import colored
from typing import List, Optional
import os

# to solve RuntimeWarning 
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

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
    INSTANCE = {
        'G4F': 'g4f',
        'OPENAI': 'openai'
    }
        
    def __init__(self, 
                 api_key: Optional[str] = None,
                 init_messages: Optional[List[dict]] = None,
                 instance: str = 'g4f'):
        self.set_instance(api_key, instance)
        self.global_msg = init_messages or []
        self._model = 'gpt-4o-mini'
    
    @property
    def client(self) -> Optional[Client]:
        return getattr(self, '_client', None)

    @client.setter
    def client(self, value: Client):
        if not isinstance(value, (OpenAI, Client)):
            raise ValueError("client 必須是 OpenAI 或 G4F 實例")
        self._client = value
        
    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        self._model = value
        
    def check_instance(self, instance: str):
        if instance not in self.INSTANCE.values():
            supported_instances = ", ".join(self.INSTANCE.values())
            raise ValueError(f"不支援的實例，請使用以下之一: {supported_instances}")
        
    def set_instance(self, api_key: Optional[str], instance: str):
        self.check_instance(instance)
        client_classes = {
            self.INSTANCE['G4F']: Client(),
            self.INSTANCE['OPENAI']: OpenAI(api_key=api_key or os.environ.get('OPENAI_API_KEY'))
        }
        self._client = client_classes[instance]
        print(colored(f'[INFO] instance: {instance}', "light_cyan"))

    def get_openai_response(self, messages: List[dict]):
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

    def save_to_file(self, content: str, filename: str = 'output.md'):
        os.makedirs('saved_file', exist_ok=True)
        file_path = f'./saved_file/{filename}'
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(colored(f"\n[INFO] Assistant回覆已存至 {file_path}", "light_cyan"))
        except Exception as e:
            print(f"[ERROR] 無法儲存文件: {e}")

        

class ChatInterface:
    COMAND = {
        'EXIT': '--exit',
        'SAVE': '--save',
        # 'BACK': '--back',
        # 'SWITCH_MODEL' : '--model'
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
