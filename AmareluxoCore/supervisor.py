from langchain_core.messages import AIMessage 
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from states import AgentState
from agents.amareluxo_agent import AmareluxoAgent

PROMPT_ROUTER_TEMPLATE = """Você é um supervisor de IA. Sua função é analisar a pergunta do usuário e decidir o próximo passo.

Analise a pergunta e escolha uma das seguintes opções:

- 'amareluxo_agent': Escolha esta opção se a pergunta requer uma ação ou busca de informação. 
  Exemplos: "Qual a política de troca?", "Rastreie meu pedido ABCDE123", "Meu cupom não funciona", "Vocês vendem roupas plus size?".

- 'END': Escolha esta opção se a pergunta for uma saudação, um agradecimento ou uma conversa casual que não precisa de ferramentas.
  Exemplos: "Olá", "tudo bem?", "obrigado!", "ok".

Pergunta do usuário:
{pergunta}

{format_instructions}
"""

class SupervisorAgent:
    def __init__(self):
        self.router_llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.amareluxo_agent = AmareluxoAgent()
        self.supervisor_graph = self.create_supervisor_graph()

    def create_supervisor_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("router", self._route_agent)
        workflow.add_node("amareluxo_agent", self.amareluxo_agent.run_agent)
        
        workflow.set_entry_point("router")

        workflow.add_conditional_edges(
            "router",
            lambda state: state["next_agent"],
            {
                "amareluxo_agent": "amareluxo_agent",
                "END": END,
            },
        )
        
        workflow.add_edge("amareluxo_agent", END)
        return workflow.compile()

    def _route_agent(self, state):
        print("\n[Supervisor] 🔄 Iniciando roteamento da mensagem...")
        
        schemas = [
            ResponseSchema(name="next_agent", description="Escolha entre: amareluxo_agent, END.")
        ]
        parser = StructuredOutputParser.from_response_schemas(schemas)
        prompt = ChatPromptTemplate.from_template(template=PROMPT_ROUTER_TEMPLATE).partial(format_instructions=parser.get_format_instructions())

        chain = prompt | self.router_llm | parser
        
        pergunta = state["messages"][-1].content
        try:
            route_result = chain.invoke({"pergunta": pergunta})
            next_agent = route_result["next_agent"]
            
            if next_agent == "END":
                print("[Supervisor] 🎯 Mensagem roteada para: END (Resposta Direta)")
                resposta_direta = "Olá! Como posso te ajudar hoje?" if "olá" in pergunta.lower() else "De nada! Se precisar de mais alguma coisa, é só chamar."
                messages = state["messages"] + [AIMessage(content=resposta_direta)]
                return {"messages": messages, "next_agent": "END"}
                
            print(f"[Supervisor] 🎯 Mensagem roteada para: {next_agent}")
            return {"messages": state["messages"], "next_agent": next_agent}

        except Exception as e:
            print(f"[Supervisor] ⚠️ Erro no roteamento: {e}")
            error_message = "Desculpe, não consegui processar sua solicitação. Poderia tentar novamente?"
            messages = state["messages"] + [AIMessage(content=error_message)]
            return {"messages": messages, "next_agent": "END"}