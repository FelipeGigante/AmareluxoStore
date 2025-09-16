import requests
from langchain_core.tools import tool
from models.openai import OpenAIModel
from utils.create_agent import AgentCreator
from AmareluxoCore.models.models import Message

PROMPT_RASTREIO_PEDIDO = """Você é um agente de logística da Amareluxo, especializado em fornecer o status de rastreamento de pedidos. 
Sua única responsabilidade é usar a ferramenta de rastreamento de pedidos para fornecer informações detalhadas sobre o andamento da entrega. Não responda a perguntas sobre outros 
tópicos e sempre peça o código de rastreamento do cliente para a ferramenta. Se a ferramenta não puder rastrear o pedido, informe o cliente sobre o status "não encontrado" e sugira que ele tente novamente mais tarde."""

class RastreioPedidoAgent:
    def __init__(self):
        self.model = OpenAIModel(model_name="gpt-4", temperature=0).get_client()
        self.prompt = PROMPT_RASTREIO_PEDIDO
        self.create_agent = AgentCreator(self.model, self.set_tools(), self.prompt).create_agent

    @tool
    def rastreio_pedido(mensagem: Message) -> str:
        """
        Rastreia um pedido usando um código de rastreamento.
        Use esta ferramenta para fornecer o status atual de um pedido.
        O input deve ser o código de rastreamento fornecido pelo cliente.
        """
        response = requests.post(
            "http://localhost:9000/rastreio_pedido",
            json={"pergunta_usuario": mensagem},
            timeout=5
        )
        return response.json()

    def set_tools(self):
        tools = [self.rastreio_pedido]
        return tools
    