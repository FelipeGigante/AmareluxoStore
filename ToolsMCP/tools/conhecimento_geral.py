from strategies.openai_strategy import OpenAIStrategy
from langchain.prompts import ChatPromptTemplate
from client import LLMClient
from models.models import Pergunta

class DefaultResponse:
    def __init__(self):
        openai_strategy = OpenAIStrategy(model_name="gpt-4o", temperature=0)
        self.client = LLMClient(strategy=openai_strategy).get_model()

    def resposta_default(self, mensagem: Pergunta) -> str:
        """
        Gera uma resposta usando o LLM com um prompt focado na persona da Amareluxo.
        """

        prompt_template = ChatPromptTemplate.from_template(
            """Você é um assistente especialista da loja de roupas Amareluxo. 
            Sua principal função é responder a perguntas gerais sobre a loja, seus produtos e o universo da moda de forma amigável, prestativa e concisa.

            **Instruções Importantes:**
            - Seja sempre cordial e use o nome da loja (Amareluxo) quando apropriado.
            - Se você não souber uma informação específica (como o preço exato de um produto ou um prazo de devolução), seja honesto e sugira que o cliente verifique no site ou contate o suporte para detalhes precisos. Não invente informações.
            - Evite responder a perguntas que não tenham nenhuma relação com a loja Amareluxo, moda ou e-commerce.

            A pergunta do cliente é:
            "{pergunta_cliente}"
            """
        )

        chain = prompt_template | self.client
        response = chain.invoke({"pergunta_cliente": mensagem.pergunta})
        
        return response.content
    