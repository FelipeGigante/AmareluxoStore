import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from supervisor import SupervisorAgent
import asyncio

K_MESSAGES = 10

@st.cache_resource
def get_supervisor():
    return SupervisorAgent()

supervisor = get_supervisor()
supervisor_graph = supervisor.supervisor_graph

st.title("Atendimento Amareluxo 👩‍💻")

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
        with st.spinner("Pensando..."):
            try:
                recent_history = st.session_state.messages[-K_MESSAGES:]
                
                langchain_messages = []
                for message in recent_history:
                    if message["role"] == "user":
                        langchain_messages.append(HumanMessage(content=message["content"]))
                    else:
                        langchain_messages.append(AIMessage(content=message["content"]))

                initial_state = {"messages": langchain_messages}
                final_state = asyncio.run(supervisor_graph.ainvoke(initial_state))
                
                resposta_final = final_state["messages"][-1].content
                
                st.markdown(resposta_final)
                st.session_state.messages.append({"role": "assistant", "content": resposta_final})

            except Exception as e:
                error_message = f"Erro ao processar a solicitação: '{e}'"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})