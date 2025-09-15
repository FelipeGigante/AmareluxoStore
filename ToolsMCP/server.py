# server.py (versão corrigida)
from tools.busca_faq import BuscaFAQ
from fastapi import FastAPI
from pydantic import BaseModel

class Pergunta(BaseModel):
    pergunta_usuario: str

app = FastAPI()
faq_service = BuscaFAQ()

@app.post("/buscar_faq")
def buscar_faq_endpoint(pergunta: Pergunta):
    # Agora 'pergunta' é um objeto Pydantic, e você acessa o valor com '.pergunta_usuario'
    return {"resposta": faq_service.buscar_faq(pergunta.pergunta_usuario)}