from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from agents.duvidas_faq import DuvidasFAQAgent
from states import SupervisorState

class SupervisorAgent:

    def __init__(self):
        
        # Inicializa agents
        self.duvidas_faq_agent = DuvidasFAQAgent()
        self.supervisor_agent = self.create_supervisor_graph()

    def create_supervisor_graph(self):
        """
        Cria e compila o grafo do supervisor com os nós e transições.
        """
        workflow = StateGraph(SupervisorState)

        # Nós do grafo
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("duvidas_faq_agent", self._call_duvidas_faq)

        workflow.set_entry_point("supervisor")

        workflow.add_conditional_edges(
            "supervisor",
            lambda state: self._route_agent(state),
            {
                "duvidas_faq": "duvidas_faq_agent",
                "END": END, 
            },
        )
        
        workflow.add_edge("duvidas_faq_agent", END)
        return workflow.compile()

    def _route_agent(self, state: SupervisorState) -> str:

        pergunta = state["messages"][-1].content.lower()
        
        # TODO: adicionar logica com LLM para decidir o roteamento
        return "duvidas_faq"
    
    def _supervisor_node(self, state):
        return {"next": self._route_agent(state)}

    def _call_duvidas_faq(self, state: SupervisorState):
        agent = self.duvidas_faq_agent.create_agent()
        return agent.invoke({
            "messages": [HumanMessage(content=state["messages"][-1].content)]
        })
