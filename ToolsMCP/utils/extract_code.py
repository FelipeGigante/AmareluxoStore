import re
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class ExtractCode:

    def __init__(self, mensagem: str):
        self.mensagem = mensagem
        self.model = ChatOpenAI(model="gpt-4o", temperature=0)
        self.prompt_template = PromptTemplate.from_template(
            """Extraia o código de rastreio da seguinte mensagem. 
            Um código de rastreio é uma sequência de letras e números, como 'LL123456789BR' ou 'SS123456789BR'. 
            Retorne apenas o código, sem texto adicional. 
            Se nenhum código for encontrado, retorne a palavra 'NENHUM'.

            Mensagem: {mensagem}
            Código de Rastreio:"""
        )

        self.chain = self.prompt_template | self.model | StrOutputParser()

    def extrair_codigo_rastreio(self) -> str:
        """
        Extrai o código de rastreio da mensagem usando uma LLM.
        """
        try:
            codigo = self.chain.invoke({"mensagem": self.mensagem}).strip()
            
            if codigo.lower() == "nenhum":
                raise ValueError("Não foi possível encontrar um código de rastreio na mensagem.")
            
            if not re.match(r'^[A-Z]{2}\d{9}[A-Z]{2}$', codigo):
                print(f"Código extraído não corresponde ao formato esperado: {codigo}")
                raise ValueError("O código de rastreio extraído não é válido.")

            return codigo
        
        except Exception as e:
            print(f"Erro ao extrair código de rastreio: {e}")
            raise 