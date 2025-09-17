import streamlit as st
from langchain_core.messages import HumanMessage
from supervisor import SupervisorAgent

@st.cache_resource
def get_supervisor():
    return SupervisorAgent()

supervisor_manager = get_supervisor()
supervisor_agent = supervisor_manager.supervisor_agent

st.title("Atendimento Amareluxo")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sua pergunta:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando a resposta..."):
            try:
                initial_state = {"messages": [HumanMessage(content=prompt)]}
                
                final_state = supervisor_agent.invoke(initial_state)
                
                resposta_final = final_state["messages"][-1].content
                
                st.markdown(resposta_final)
                st.session_state.messages.append({"role": "assistant", "content": resposta_final})

            except Exception as e:
                error_message = f"Erro ao processar a solicitação: {e}"
                st.error(error_message)
                st.info("Por favor, tente novamente mais tarde ou reformule a pergunta.")
                st.session_state.messages.append({"role": "assistant", "content": error_message})

st.markdown("---")