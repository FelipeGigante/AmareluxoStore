import requests
from langchain_core.tools import tool
from strategies.openai_strategy import OpenAIStrategy
from llm_client import LLMClient
from utils.create_agent import AgentCreator

PROMPT_RASTREIO_PEDIDO = """Você é um agente de logística da Amareluxo, especializado em fornecer o status de rastreamento de pedidos. 

A solicitação do cliente é: {pergunta}

Sua única responsabilidade é usar a ferramenta de rastreamento de pedidos para fornecer informações detalhadas sobre o andamento da entrega. 
Sempre extraia o código de rastreamento da solicitação e consulte a ferramenta. 
Se não houver código válido, peça educadamente que o cliente forneça.
"""

class RastreioPedidoAgent:
    def __init__(self):
        openai_strategy = OpenAIStrategy(model_name="gpt-4o", temperature=0)
        self.model = LLMClient(strategy=openai_strategy).get_model()
        self.prompt = PROMPT_RASTREIO_PEDIDO
        self.create_agent = AgentCreator(self.model, self.set_tools(), self.prompt).create_agent

    @tool
    def rastreio_pedido(codigo: str) -> str:
        """
        Rastreia um pedido usando um código de rastreamento.
        Use esta ferramenta para fornecer o status atual de um pedido.
        O input deve ser o código de rastreamento fornecido pelo cliente.
        """
        response = requests.post(
            "http://localhost:9000/rastreio_pedido",
            json={"pergunta_usuario": codigo},
            timeout=5
        )
        return response.json()

    def set_tools(self):
        tools = [self.rastreio_pedido]
        return tools
    