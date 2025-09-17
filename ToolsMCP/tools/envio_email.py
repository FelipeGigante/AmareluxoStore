import smtplib
from dotenv import load_dotenv
import os
from services.envio_email_service import EnvioEmailService
from models.models import EnvioEmail

load_dotenv()

class EnvioEmail:
    def __init__(self):
        self.remetente = os.getenv("REMETENTE")
        self.destinatario = os.getenv("DESTINATARIO")
        self.assunto = "E-mail Automático - Atendimento MCP"
        self.mensagem = "O suporte humano entrará em contato assim que obtivermos uma resposta mais precisa sobre o seu pedido.!"
        self.password = os.getenv("GOOGLE_PASSWORD")

    def enviar_email(self):
        
        request_email = EnvioEmail(
            remetente=self.remetente,
            destinatario=self.destinatario,
            assunto=self.assunto,
            mensagem=self.mensagem
        )

        envio_email = EnvioEmailService(request_email)
        mensagem = envio_email.enviar(self.mensagem)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.remetente, self.password)
                smtp.send_message(mensagem)
                print("Email enviado com sucesso!")
        except Exception as e:
            raise ValueError(f"Erro ao enviar email: {e}")

if __name__ == "__main__":
    email = EnvioEmail()
    email.enviar_email()