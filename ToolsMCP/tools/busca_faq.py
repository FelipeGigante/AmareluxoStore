import json
from langchain.tools import tool
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer, util
import torch

app = FastAPI()

class BuscaFAQ:
    def __init__(self):
        self.faq_data = self.carregar_faq()
        self.model = self.load_model()
        
        # Carrega os embeddings e perguntas apenas uma vez
        self.faq_perguntas, self.faq_embeddings = self.create_embeddings()
        self.faq_map_once = self.faq_map()

    def carregar_faq(self):
        try:
            with open('KB/KB.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Erro: O arquivo KB/KB.json não foi encontrado.")
            return []

    def load_model(self):
        print("Carregando o modelo de embeddings do Hugging Face...")
        return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')

    def create_embeddings(self) -> tuple:
        if not self.model:
            raise ValueError("Modelo não carregado.")
        
        print("Criando embeddings para as perguntas do FAQ...")
        perguntas = [item['pergunta'] for item in self.faq_data]
        embeddings = self.model.encode(perguntas, convert_to_tensor=True)
        
        return perguntas, embeddings

    def faq_map(self) -> dict:
        return {item['pergunta']: item for item in self.faq_data}

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
