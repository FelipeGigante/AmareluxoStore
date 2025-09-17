from utils.extract_code import ExtractCode
from services.rastreio_service import RastreioPedidoService

class RastreioPedido:
    def __init__(self):
        self.rastreio_service = RastreioPedidoService()

    def rastrear_pedido(self, pergunta_usuario: str) -> str:
        """
        Rastreia o pedido usando o código de rastreio fornecido.
        """
        try:
            extractor = ExtractCode(pergunta_usuario)
            codigo_rastreio = extractor.extrair_codigo_rastreio()
            print(f"Código de rastreio extraído: {codigo_rastreio}")
            
            status_rastreio = self.rastreio_service.rastrear(codigo_rastreio)
            return status_rastreio
            
        except Exception as e:
            print(f"Erro ao rastrear o pedido: {e}")
            return "Ocorreu um erro ao rastrear o pedido. Tente novamente mais tarde."
