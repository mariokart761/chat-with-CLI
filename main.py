from tools.chat_assistant import ChatAssistant, ChatInterface
import argparse

if __name__ == "__main__":
    # If you want to use your OpenAI API Key, use following line 
    # or export an envrionment variable: https://platform.openai.com/docs/quickstart .
    api_key=None
    # api_key = "your_api_key"
    
    parser = argparse.ArgumentParser(description="Chat Assistant CLI")
    parser.add_argument('-i', '--instance', type=str, choices=['openai', 'g4f'], required=True,
                        help="指定要使用的實例: 'openai' 或 'g4f'")
    args = parser.parse_args()
    
    ca = ChatAssistant(api_key=api_key, instance=args.instance) 
    ChatInterface(ca).chat_with_cli()