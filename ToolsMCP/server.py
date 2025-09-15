from tools.busca_faq import BuscaFAQ
from fastapi import FastAPI

# import models
from models.pergunta import Pergunta

app = FastAPI()

# tools instance
faq_service = BuscaFAQ()

# set routes endpoints
@app.post("/buscar_faq")
def buscar_faq_endpoint(pergunta: Pergunta):
    return {"resposta": faq_service.buscar_faq(pergunta.pergunta_usuario)}