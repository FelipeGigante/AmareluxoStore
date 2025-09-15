import json
from langchain.tools import tool
from sentence_transformers import SentenceTransformer, util
from KB import KB


class BuscaFAQ:
    def __init__(self):
        self.faq_data = self.carregar_faq()
        self.model = None

    def carregar_faq(self):
        with open('KB/KB.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_model(self):
        print("Carregando o modelo de embeddings do Hugging Face...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        return self.model

    def create_embeddings(self) -> dict:
        if not self.model:
            raise ValueError("Modelo não carregado.")
        
        print("Criando embeddings para as perguntas do FAQ...")
        perguntas = [item['pergunta'] for item in self.faq_data]
        embeddings = self.model.encode(perguntas, convert_to_tensor=True)

        response = {
            "faq_perguntas": perguntas,
            "embeddings": embeddings
        }

        return response

    def faq_map(self):
        return {item['pergunta']: item for item in self.faq_data}

    @tool
    def buscar_faq(self, pergunta_usuario: str) -> str:
        """
        Busca a resposta para uma pergunta no banco de dados de FAQ do e-commerce Amareluxo,
        usando busca de similaridade vetorial com embeddings.
        """
        try:
            faq_embeddings = self.create_embeddings()["embeddings"]
            faq_perguntas = self.create_embeddings()["faq_perguntas"]
            
            pergunta_embedding = self.model.encode(pergunta_usuario, convert_to_tensor=True)
            cos_scores = util.cos_sim(pergunta_embedding, faq_embeddings)[0]
            melhor_match_index = cos_scores.argmax()

            score = cos_scores[melhor_match_index].item()
            
            if score > 0.6:
                melhor_pergunta = faq_perguntas[melhor_match_index]   
                return self.faq_map[melhor_pergunta]['resposta']
            else:
                return "Não consegui encontrar uma resposta para sua pergunta. Por favor, reformule ou entre em contato com o nosso suporte."

        except Exception as e:
            print(f"Erro ao buscar no FAQ: {e}")
            return "Ocorreu um erro ao buscar a resposta. Tente novamente mais tarde."
