import streamlit as st
import requests

st.title("Atendimento Amareluxo")

pergunta_usuario = st.text_input("Olá! O que você gostaria de saber sobre a Amareluxo?")

if pergunta_usuario:
    st.info("Buscando sua resposta...")
    
    try:
        response = requests.post(
            "http://api:9000/buscar_faq",
            json={"pergunta_usuario": pergunta_usuario}
        )
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            resposta_api = response.json().get("resposta")
            st.success(f"**Amareluxo:** {resposta_api}")
        else:
            st.error("Não foi possível obter a resposta da API. Tente novamente.")
            st.error(f"Detalhes do erro: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com o servidor de busca: {e}")

st.markdown("---")
st.caption("Desenvolvido para o projeto pessoal de estudo de LangGraph.")