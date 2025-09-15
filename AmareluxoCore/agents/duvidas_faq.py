import requests
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from models.openai import OpenAIModel
from utils.create_agent import AgentCreator

PROMPT_DUVIDAS_FAQ = """Você é um agente de suporte especializado no e-commerce de roupas Amareluxo.
    Seu principal objetivo é ajudar os clientes a encontrar informações sobre seus pedidos, produtos e políticas da loja. 
    Utilize exclusivamente as ferramentas fornecidas, que acessam a nossa base de dados de FAQ, para encontrar as respostas. 
    Se a pergunta do cliente não puder ser respondida com as informações do FAQ, informe-o de maneira cordial que a resposta 
    não está disponível no momento e sugira entrar em contato com o suporte humano."""


class DuvidasFAQAgent:
    def __init__(self):
        self.model = OpenAIModel(model_name="gpt-4", temperature=0).get_client()
        self.prompt = PROMPT_DUVIDAS_FAQ
        self.create_agent = AgentCreator(self.model, self.set_tools(), self.prompt).create_agent

    @tool
    def buscar_faq(pergunta: str) -> str:
        """
        Busca a resposta para uma pergunta no banco de dados de FAQ do e-commerce Amareluxo.
        Use esta ferramenta para responder perguntas sobre pedidos, prazos de entrega,
        rastreamento, trocas, devoluções e métodos de pagamento.
        O input deve ser a pergunta do usuário.
        """
        response = requests.post(
            "http://localhost:9000/buscar_faq",
            json={"pergunta_usuario": pergunta},
            timeout=5
        )
        return response.json()

    def set_tools(self):
        tools = [self.buscar_faq]
        return tools
    

if __name__ == "__main__":
    agent = DuvidasFAQAgent().create_agent()
    result = agent.invoke({
        "messages": [
            HumanMessage(
                content="Quanto tempo demora para chegar meus pedidos?")
        ]
    })
    print(result['messages'][-1].content)