from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from agents.duvidas_faq import DuvidasFAQAgent
from agents.envio_email import EnvioEmailAgent
from agents.rastreio_pedido import RastreioPedidoAgent
from models.openai import OpenAIModel
from states import AgentState
from models.output import RouteOutput
    
class SupervisorAgent:
    def __init__(self):
        self.model = OpenAIModel(model_name="gpt-4o", temperature=0).get_client()
        self.router_llm = ChatOpenAI(model="gpt-4o", temperature=0)

        self.duvidas_faq_agent_instance = DuvidasFAQAgent()
        self.envio_email_agent_instance = EnvioEmailAgent()
        self.rastreio_pedido_agent_instance = RastreioPedidoAgent()

        self.supervisor_agent = self.create_supervisor_graph()

    def create_supervisor_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("router", self._route_agent)
        workflow.add_node("duvidas_faq_agent", self._call_duvidas_faq)
        workflow.add_node("envio_email_agent", self._call_envio_email)
        workflow.add_node("rastreio_pedido_agent", self._call_rastreio_pedido)
        
        workflow.set_entry_point("router")

        workflow.add_conditional_edges(
            "router",
            self._route_logic,
            {
                "duvidas_faq": "duvidas_faq_agent",
                "envio_email": "envio_email_agent",
                "rastreio_pedido": "rastreio_pedido_agent",
                "END": END,
            },
        )
        
        workflow.add_edge("duvidas_faq_agent", END)
        workflow.add_edge("envio_email_agent", END)
        workflow.add_edge("rastreio_pedido_agent", END)

        return workflow.compile()

    def _route_logic(self, state):
        return state["next_agent"]

    def _route_agent(self, state):
        prompt = PromptTemplate.from_template("""Você é um roteador de mensagens, seu trabalho é decidir qual agente é mais adequado para a pergunta do usuário.
            A sua decisão deve ser baseada nos seguintes agentes disponíveis:

            - duvidas_faq: para responder perguntas frequentes sobre a empresa, como prazos, trocas, devoluções e pagamentos.
            - envio_email: para enviar e-mails para o suporte humano quando solicitado o atendimento humano pelo usuário.
            - rastreio_pedido: para fornecer o status de rastreamento de um pedido.
            - END: se a pergunta não for relevante para nenhum dos agentes.

            A pergunta do usuário é: "{pergunta}"
            Retorne apenas o nome do agente em formato JSON, com a chave "next_agent".""")

        chain = prompt | self.router_llm.with_structured_output(schema=RouteOutput)
        
        pergunta = state["messages"][-1].content
        try:
            route_result = chain.invoke({"pergunta": pergunta})
            return {"next_agent": route_result["next_agent"], "messages": state["messages"]}
        except Exception as e:
            return {"next_agent": "END", "messages": state["messages"]}

    def _call_duvidas_faq(self, state: AgentState):
        agent = self.duvidas_faq_agent_instance.create_agent()
        pergunta = state["messages"][-1].content
        return agent.invoke({"pergunta": pergunta})

    def _call_envio_email(self, state: AgentState):
        agent = self.envio_email_agent_instance.create_agent()
        pergunta = state["messages"][-1].content
        return agent.invoke({"pergunta": pergunta})
    
    def _call_rastreio_pedido(self, state: AgentState):
        agent = self.rastreio_pedido_agent_instance.create_agent()
        pergunta = state["messages"][-1].content
        return agent.invoke({"pergunta": pergunta})