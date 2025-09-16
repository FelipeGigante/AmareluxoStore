from sentence_transformers import util
from services.busca_faq_service import BuscaFAQService

class BuscaFAQ:
    def __init__(self):
        self.busca_service = BuscaFAQService()
        self.faq_data = self.busca_service.carregar_faq()
        
        # Carrega os embeddings e perguntas apenas uma vez
        self.faq_perguntas, self.faq_embeddings = self.busca_service.create_embeddings()
        self.faq_map_once = self.busca_service.faq_map()

    def buscar_faq(self, pergunta_usuario: str) -> str:
        """
        Busca a resposta para uma pergunta no banco de dados de FAQ do e-commerce Amareluxo,
        usando busca de similaridade vetorial com embeddings.
        """
        faq_perguntas = self.faq_perguntas
        faq_embeddings = self.faq_embeddings
        model = self.model
        faq_map = self.faq_map_once
        
        try:
            pergunta_embedding = model.encode(pergunta_usuario, convert_to_tensor=True)
            cos_scores = util.cos_sim(pergunta_embedding, faq_embeddings)[0]
            melhor_match_index = cos_scores.argmax()

            score = cos_scores[melhor_match_index].item()
            
            if score > 0.6:
                melhor_pergunta = faq_perguntas[melhor_match_index]
                return faq_map[melhor_pergunta]['resposta']
            else:
                return "Não consegui encontrar uma resposta para sua pergunta. Por favor, reformule ou entre em contato com o nosso suporte."

        except Exception as e:
            print(f"Erro ao buscar no FAQ: {e}")
            return "Ocorreu um erro ao buscar a resposta. Tente novamente mais tarde."
