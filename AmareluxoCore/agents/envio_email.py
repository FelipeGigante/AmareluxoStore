import requests
from langchain_core.tools import tool
from strategies.openai_strategy import OpenAIStrategy
from client import LLMClient
from utils.create_agent import AgentCreator
from dotenv import load_dotenv
import os

load_dotenv()


# PROMPT MUITO MAIS DETALHADO
PROMPT_ENVIO_EMAIL = """Você é um agente de suporte da Amareluxo.
Sua principal função é abrir um ticket de suporte por e-mail quando um cliente tem um problema que não pode ser resolvido por outras ferramentas.

Para fazer isso, você DEVE seguir estes passos:
1.  Entenda o problema do cliente a partir da conversa.
2.  SE o e-mail do cliente não for fornecido na conversa, você DEVE perguntar educadamente: "Para qual e-mail podemos enviar a confirmação e registrar seu ticket de suporte?".
3.  Quando tiver a descrição do problema E o e-mail do cliente, utilize a ferramenta `enviar_email_suporte`.

Não use a ferramenta sem ter o e-mail do cliente.

A solicitação do cliente é: {pergunta}
"""

class EnvioEmailAgent:
    def __init__(self):
        openai_strategy = OpenAIStrategy(model_name="gpt-4o", temperature=0)
        self.model = LLMClient(strategy=openai_strategy).get_model()
        self.prompt = PROMPT_ENVIO_EMAIL
        self.create_agent = AgentCreator(self.model, self.set_tools(), self.prompt).create_agent

    @tool
    def enviar_email_suporte(mensagem_usuario: str, email_cliente: str) -> str:
        """
        Formata e envia um e-mail para o suporte da Amareluxo com o problema do cliente.
        Use esta ferramenta DEPOIS de obter o e-mail do cliente.
        O input 'mensagem_usuario' deve ser um resumo claro do problema do cliente.
        O input 'email_cliente' deve ser o endereço de e-mail fornecido pelo cliente.
        """
        
        email_suporte = os.getenv("EMAIL_SUPORTE")
        
        assunto = f"Novo Ticket de Suporte - Cliente: {email_cliente}"
        
        mensagem_html = f"""
        <html>
        <body>
            <h2>Novo Pedido de Suporte Recebido</h2>
            <p><strong>Cliente:</strong> {email_cliente}</p>
            <hr>
            <h3>Descrição do Problema:</h3>
            <p><em>"{mensagem_usuario}"</em></p>
            <hr>
            <p>Por favor, entre em contato com o cliente para resolver a questão.</p>
            <p><em>- Enviado automaticamente pelo Assistente Amareluxo</em></p>
        </body>
        </html>
        """

        try:
            response = requests.post(
                "http://localhost:9000/envio_email",
                json={
                    "destinatario": email_suporte,
                    "assunto": assunto,
                    "mensagem_html": mensagem_html
                },
                timeout=10
            )
            
            return "E-mail de suporte enviado com sucesso! Nossa equipe entrará em contato em breve."
        except Exception as e:
            return f"Ocorreu um erro ao tentar enviar o e-mail: {e}"

    def set_tools(self):
        tools = [self.enviar_email_suporte]
        return tools