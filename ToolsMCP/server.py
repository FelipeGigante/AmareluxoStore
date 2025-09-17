from tools.busca_faq import BuscaFAQ
from tools.rastreio import RastreioPedido
from tools.envio_email import EnvioEmail
from services.envio_email_service import EnvioEmailService
from models.models import EnvioRequest
from fastapi import FastAPI

# import models
from models.models import Pergunta

app = FastAPI()

# tools instance
faq_service = BuscaFAQ()
envio_email = EnvioEmail()
rastreio_pedido = RastreioPedido()

# set routes endpoints
@app.post("/buscar_faq")
def buscar_faq_endpoint(pergunta: Pergunta):
    return {"resposta": faq_service.buscar_faq(pergunta.pergunta_usuario)}

@app.post("/envio_email")
def envio_email_endpoint(request: EnvioRequest):
    email_service = EnvioEmailService()
    return email_service.enviar(request)

@app.post("/rastreio_pedido")
def rastreio_pedido_endpoint(pergunta: Pergunta):
    return {"resposta": rastreio_pedido.rastrear_pedido(pergunta.pergunta_usuario)}

@app.get("/")
def root():
    return {"message": "API is running"}