import os
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from strategies.strategy_interface import LLMStrategy
from dotenv import load_dotenv

load_dotenv()

class OpenAIStrategy(LLMStrategy):
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não definida no ambiente.")

    def get_client(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.api_key,
            temperature=self.temperature
        )