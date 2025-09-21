from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

class LLMStrategy(ABC):
    """
    A interface que define o contrato para todas as estratégias de LLM.
    Qualquer classe de LLM deve implementar o método get_client.
    """
    @abstractmethod
    def get_client(self) -> BaseChatModel:
        """
        Deve retornar uma instância de um cliente de chat model compatível com LangChain.
        """
        pass