import smtplib
from dotenv import load_dotenv
import os
from services.envio_email_service import EnvioEmailService
from models.models import EnvioRequest

load_dotenv()

class EnvioEmail:
    def __init__(self):
        self.remetente = os.getenv("REMETENTE")
        self.password = os.getenv("GOOGLE_PASSWORD")

    def enviar_email(self, request: EnvioRequest):
        
        request_email = EnvioRequest(
            remetente=self.remetente,
            destinatario=request.destinatario,
            assunto=request.assunto,
            mensagem=self.mensagem
        )

        envio_email = EnvioEmailService(request_email)
        mensagem = envio_email.enviar(request.mensagem_html)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.remetente, self.password)
                smtp.send_message(mensagem)
                print("Email enviado com sucesso!")
        except Exception as e:
            raise ValueError(f"Erro ao enviar email: {e}")
