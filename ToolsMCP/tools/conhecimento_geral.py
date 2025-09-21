from strategies.openai_strategy import OpenAIStrategy
from langchain.prompts import ChatPromptTemplate
from client import LLMClient

class DefaultResponse:
    def __init__(self):
        openai_strategy = OpenAIStrategy(model_name="gpt-4o", temperature=0)
        self.client = LLMClient(strategy=openai_strategy).get_model()

    def resposta_default(self, mensagem: str) -> str:
        """
        Gera uma resposta usando o LLM com um prompt focado na persona da Amareluxo.
        """

        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "Você é um assistente especialista da loja Amareluxo. Responda a pergunta do cliente de forma direta, útil e prestativa. "
                "Não inclua saudações como 'Olá!' ou 'Oi'."),
                ("user", "{pergunta_cliente}"),
            ]
        )
        
        chain = prompt_template | self.client
        response = chain.invoke({"pergunta_cliente": mensagem})
        
        return response.content
    