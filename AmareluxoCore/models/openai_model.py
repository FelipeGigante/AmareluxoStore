import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class OpenAIModel:
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.api_key,
            temperature=self.temperature
        )

    def get_client(self):
        return self.client