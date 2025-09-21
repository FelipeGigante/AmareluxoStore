import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from mcp_use import MCPAgent, MCPClient

load_dotenv()

class AmareluxoAgent:
    """
    Agente especialista que se conecta ao servidor MCP para utilizar as ferramentas
    da Amareluxo (FAQ, Rastreio, E-mail).
    """
    def __init__(self):
        config = {
            "mcpServers": {
                "http": {
                    "url": os.getenv("MCP_SERVER_URL")
                }
            }
        }
        client = MCPClient.from_dict(config)
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.agent_executor = MCPAgent(llm=llm, client=client, max_steps=15)
        print("[Agente] 📞 Agente Amareluxo inicializado e pronto.")

    async def run_agent(self, state: dict) -> dict:
        
        pergunta = state["messages"][-1].content
        result = await self.agent_executor.run(pergunta)
        
        print(f"[Agente] ✅ Resposta do Agente: {result}")

        messages = state["messages"] + [AIMessage(content=result)]
        return {"messages": messages}