import requests
from langchain_core.tools import tool
from models.openai_model import OpenAIModel
from utils.create_agent import AgentCreator

PROMPT_ENVIO_EMAIL = """Você é um agente de comunicação da Amareluxo, especializado em enviar e-mails de notificação e suporte aos clientes. 
Sua única responsabilidade é usar a ferramenta de envio de e-mails para enviar mensagens com base em solicitações específicas. 

A solicitação do cliente é: {pergunta}
"""


class EnvioEmailAgent:
    def __init__(self):
        self.model = OpenAIModel(model_name="gpt-4", temperature=0).get_client()
        self.prompt = PROMPT_ENVIO_EMAIL
        self.create_agent = AgentCreator(self.model, self.set_tools(), self.prompt).create_agent

    @tool
    def envio_email() -> str:
        """
        Envia uma mensagem de e-mail para um cliente.
        Use esta ferramenta apenas para enviar mensagens para um cliente.
        O input deve conter o e-mail do destinatário e a mensagem a ser enviada.
        """
        response = requests.post(
            "http://localhost:9000/envio_email",
            timeout=5
        )
        return response.json()

    def set_tools(self):
        tools = [self.envio_email]
        return tools
    