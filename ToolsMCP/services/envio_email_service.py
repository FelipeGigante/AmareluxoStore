from models.models import EnvioEmail
from email.message import EmailMessage

class EnvioEmailService():

    def __init__(self, email_data: EnvioEmail):
        self.mensagem = EmailMessage()
        self.email_data = email_data

    def enviar(self, content: str):
        self.mensagem['From'] = self.email_data.remetente
        self.mensagem['To'] = self.email_data.destinatario
        self.mensagem['Subject'] = self.email_data.assunto
        self.mensagem.set_content(content)
        
        return self.mensagem