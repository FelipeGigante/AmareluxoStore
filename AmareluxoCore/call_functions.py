from states import AgentState
from langchain_core.messages import HumanMessage

from agents.duvidas_faq import DuvidasFAQAgent
from agents.envio_email import EnvioEmailAgent
from agents.rastreio_pedido import RastreioPedidoAgent

class CallFunctions:

    def __init__(self):
        self.duvidas_faq_agent_instance = DuvidasFAQAgent()
        self.envio_email_agent_instance = EnvioEmailAgent()
        self.rastreio_pedido_agent_instance = RastreioPedidoAgent()

    def _call_duvidas_faq(self, state: AgentState): 
        agent = self.duvidas_faq_agent_instance.create_agent() 
        print("[Supervisor] ✅ Agente FAQ finalizou execução")
        return agent.invoke({"messages": [HumanMessage(content=state["messages"][-1].content)]}) 
    
    def _call_envio_email(self, state: AgentState): 
        agent = self.envio_email_agent_instance.create_agent() 
        print("[Supervisor] ✅ Agente E-mail finalizou execução")
        return agent.invoke({"messages": [HumanMessage(content=state["messages"][-1].content)]}) 
    
    def _call_rastreio_pedido(self, state: AgentState): 
        agent = self.rastreio_pedido_agent_instance.create_agent() 
        print("[Supervisor] ✅ Agente Rastreio finalizou execução")
        return agent.invoke({"messages": [HumanMessage(content=state["messages"][-1].content)]})