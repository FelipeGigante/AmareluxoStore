from strategies.strategy_interface import LLMStrategy
from langchain_core.language_models.chat_models import BaseChatModel

class LLMClient:
    def __init__(self, strategy: LLMStrategy):
        self._strategy = strategy

    def get_model(self) -> BaseChatModel:
        """
        Delega a criação do cliente para o objeto de estratégia.
        """
        return self._strategy.get_client()