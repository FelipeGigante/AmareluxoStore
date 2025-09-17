from pydantic import BaseModel

class Pergunta(BaseModel):
    pergunta_usuario: str

class EnvioRequest(BaseModel):
    remetente: str
    destinatario: str
    assunto: str
    mensagem: str