import requests
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from models.openai import OpenAIModel

class DuvidasFAQAgent:
    def __init__(self):
        self.model = OpenAIModel(model_name="gpt-4", temperature=0).get_client()

    @tool
    def clima(city: str) -> str:
        response = requests.post(
            "http://localhost:9000/clima",
            json={"cidade": city},
            timeout=5
        )
        return response.json()["previsao"]

    @tool
    def horario(city: str) -> str:
        response = requests.post(
            "http://localhost:9000/horario",
            json={"cidade": city},
            timeout=5
        )
        return response.json()["hora"]

    def set_tools(self):
        tools = [self.clima(), self.horario()]
        return tools
    
    def create_agent(self):
        agent = create_react_agent(
            model=self.model,
            tools=self.set_tools(),
            prompt=(
                "Você é um agente de suporte especializado no e-commerce de roupas Amareluxo. "
                "Seu principal objetivo é ajudar os clientes a encontrar informações sobre seus pedidos, produtos e políticas da loja. "
                "Utilize exclusivamente as ferramentas fornecidas, que acessam a nossa base de dados de FAQ, para encontrar as respostas. "
                "Se a pergunta do cliente não puder ser respondida com as informações do FAQ, informe-o de maneira cordial que a resposta "
                "não está disponível no momento e sugira entrar em contato com o suporte humano."
            )
        )

        return agent

if __name__ == "__main__":
    agent = DuvidasFAQAgent().create_agent()
    result = agent.invoke({
        "messages": [
            HumanMessage(
                content="Qual a previsão do tempo e a hora local para Curitiba?")
        ]
    })
    print(result['messages'][-1].content)