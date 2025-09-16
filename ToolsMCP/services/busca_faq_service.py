import json
from sentence_transformers import SentenceTransformer
import torch

class BuscaFAQService:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')

    def carregar_faq(self):
        try:
            with open('KB/KB.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Erro: O arquivo KB/KB.json não foi encontrado.")
            return []

    def create_embeddings(self) -> tuple:
        if not self.model:
            raise ValueError("Modelo não carregado.")
        
        print("Criando embeddings para as perguntas do FAQ...")
        perguntas = [item['pergunta'] for item in self.faq_data]
        embeddings = self.model.encode(perguntas, convert_to_tensor=True)
        
        return perguntas, embeddings

    def faq_map(self) -> dict:
        return {item['pergunta']: item for item in self.faq_data}