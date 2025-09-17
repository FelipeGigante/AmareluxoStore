import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

class RastreioPedidoService():
    
    def __init__(self):
        self.key = os.getenv("KEY_RASTREIO")
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Apikey {self.key}'
        }

    def rastrear(self, codigo_rastreio: str) -> str:
        """
        Rastreia o pedido usando o código de rastreio fornecido.
        """
        
        try:            
            if not codigo_rastreio:
                return "Código de rastreio não encontrado na pergunta."

            payload = {"code": codigo_rastreio}
            response = requests.post(
                'https://api-labs.wonca.com.br/wonca.labs.v1.LabsService/Track', 
                headers=self.headers, 
                json=payload
            )
            
            response.raise_for_status()
            data = response.json()
            tracking_data = json.loads(data['json'])
            
            if tracking_data.get('eventos'):
                latest_event = tracking_data['eventos'][0] 
                status = latest_event.get('descricaoWeb', 'Status não disponível')
                return f"Status atual: {status}"
            else:
                return "Nenhum evento de rastreio encontrado"
        
        except Exception as e:
            print(f"Erro ao rastrear o pedido: {e}")
            return "Ocorreu um erro ao rastrear o pedido. Tente novamente mais tarde."