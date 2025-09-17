from langchain_core.messages import HumanMessage, AIMessage 
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from call_functions import CallFunctions
from models.openai_model import OpenAIModel
from states import AgentState

PROMPT_ROUTER_TEMPLATE = """Você é um supervisor especialista em rotear a pergunta de um cliente para o agente correto.
Analise a pergunta do usuário e as descrições dos agentes para decidir qual agente é o mais adequado.
Se nenhuma das opções for apropriada, escolha 'END'.

Pergunta do usuário:
{pergunta}

{format_instructions}
"""

class SupervisorAgent:
    def __init__(self):
        self.model = OpenAIModel(model_name="gpt-4o", temperature=0).get_client()
        self.router_llm = ChatOpenAI(model="gpt-4o", temperature=0)

        self.call_functions = CallFunctions()

        self.supervisor_agent = self.create_supervisor_graph()

    def create_supervisor_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("router", self._route_agent)
        workflow.add_node("duvidas_faq_agent", self.call_functions._call_duvidas_faq)
        workflow.add_node("envio_email_agent", self.call_functions._call_envio_email)
        workflow.add_node("rastreio_pedido_agent", self.call_functions._call_rastreio_pedido)
        
        workflow.set_entry_point("router")

        workflow.add_conditional_edges(
            "router",
            lambda state: state["next_agent"],
            {
                "duvidas_faq_agent": "duvidas_faq_agent",
                "envio_email_agent": "envio_email_agent",
                "rastreio_pedido_agent": "rastreio_pedido_agent",
                "END": END,
            },
        )
        
        workflow.add_edge("duvidas_faq_agent", END)
        workflow.add_edge("envio_email_agent", END)
        workflow.add_edge("rastreio_pedido_agent", END)

        return workflow.compile()

    def _route_agent(self, state):
        print("\n[Supervisor] 🔄 Iniciando roteamento da mensagem...")
        
        schemas = [
            ResponseSchema(name="next_agent", description="Escolha entre: duvidas_faq_agent, envio_email_agent, rastreio_pedido_agent. Analise a pergunta do usuário com o máximo de critério e selecione a opção que se encaixa perfeitamente.")
        ]
        parser = StructuredOutputParser.from_response_schemas(schemas)
        prompt = ChatPromptTemplate.from_template(template=PROMPT_ROUTER_TEMPLATE).partial(format_instructions=parser.get_format_instructions())

        llm = self.router_llm
        chain = prompt | llm | parser
        
        pergunta = state["messages"][-1].content
        try:
            route_result = chain.invoke({"pergunta": pergunta})
            next_agent = route_result["next_agent"]
            print(f"[Supervisor] 🎯 Mensagem roteada para: {route_result['next_agent']}")
            return {"messages": state["messages"], "next_agent": next_agent}
        except Exception as e:
            print(f"[Supervisor] ⚠️ Erro no roteamento: {e}")
            error_message = "Desculpe, não consegui entender sua solicitação. Por favor, tente novamente de forma mais específica."
            return {"messages": [AIMessage(content=error_message)], "next_agent": END}
    