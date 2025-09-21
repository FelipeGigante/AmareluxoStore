import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from strategies.strategy_interface import LLMStrategy
from dotenv import load_dotenv

load_dotenv()

class GeminiStrategy(LLMStrategy):
    def __init__(self, model_name: str = "gemini-1.5-pro-latest", temperature: float = 0.7):

        self.model_name = model_name
        self.temperature = temperature
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY não definida no ambiente.")

    def get_client(self) -> BaseChatModel:
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=self.temperature,
            convert_system_message_to_human=True 
        )