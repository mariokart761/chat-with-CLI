from tools.chat_assistant import ChatAssistant, ChatInterface
from g4f.client import Client
import argparse

def main(instance, api_key):
    ca = ChatAssistant(api_key=api_key)
    if instance == 'g4f':
        ca.client = Client()
    elif instance == 'openai':
        pass
    else:
        raise ValueError("不支援的實例，請使用 'openai' 或 'g4f'")
    
    return ca

if __name__ == "__main__":
    # If you want to use your OpenAI API Key, use following line 
    # or export an envrionment variable: https://platform.openai.com/docs/quickstart .
    api_key=None
    # api_key = "your_api_key"
    
    parser = argparse.ArgumentParser(description="Chat Assistant CLI")
    parser.add_argument('-i', '--instance', type=str, choices=['openai', 'g4f'], required=True,
                        help="指定要使用的實例: 'openai' 或 'g4f'")
    args = parser.parse_args()
    
    ca = main(args.instance, api_key) 
    chat_interface = ChatInterface(ca)
    chat_interface.chat_with_cli()