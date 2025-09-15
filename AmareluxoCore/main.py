import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from supervisor import SupervisorAgent

@st.cache_resource
def get_supervisor():
    return SupervisorAgent()

supervisor_manager = get_supervisor()
supervisor_agent = supervisor_manager.supervisor_agent

st.title("Atendimento Amareluxo")
st.markdown("Olá! Sou o seu assistente virtual da Amareluxo. Como posso ajudar?")

pergunta_usuario = st.text_input("Sua pergunta:", key="user_input")

if pergunta_usuario:
    st.info("Buscando a resposta...")

    try:
        initial_state = {"messages": [HumanMessage(content=pergunta_usuario)]}

        final_state = list(supervisor_agent.stream(initial_state, {"recursion_limit": 10}))[-1]

        resposta_final = final_state[list(final_state.keys())[0]]['messages'][-1].content
        
        st.success(f"**Amareluxo:** {resposta_final}")

    except Exception as e:
        st.error(f"Erro ao processar a solicitação: {e}")
        st.info("Por favor, tente novamente mais tarde ou reformule a pergunta.")

st.markdown("---")
st.caption("Desenvolvido por Felipe Gigante")