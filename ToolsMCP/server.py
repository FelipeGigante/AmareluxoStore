from fastmcp import FastMCP

from models.models import EnvioRequest
from models.models import Pergunta

from tools.busca_faq import BuscaFAQ
from tools.rastreio import RastreioPedido
from tools.envio_email import EnvioEmail
from tools.conhecimento_geral import DefaultResponse

mcp = FastMCP("Amareluxo Core")

# tools instance
faq_service = BuscaFAQ()
envio_email = EnvioEmail()
rastreio_pedido = RastreioPedido()
default_response = DefaultResponse()

# set tools 
@mcp.tool("buscar_faq")
def buscar_faq_endpoint(pergunta: Pergunta):
    """
    PRIORIDADE 1: Use esta ferramenta para responder perguntas sobre processos, políticas ou informações estruturadas da loja.
    É a escolha principal para dúvidas sobre: trocas, devoluções, prazos de entrega, métodos de pagamento, cupons de desconto e status de pedido.
    Exemplos: 'Como faço para trocar um produto?', 'Quais cartões vocês aceitam?'.
    """
    return {"resposta": faq_service.buscar_faq(pergunta.pergunta_usuario)}

@mcp.tool("envio_email")
def envio_email_endpoint(request: EnvioRequest):
    """
    Use esta ferramenta como último recurso para criar um ticket de suporte por e-mail para problemas complexos que necessitam de intervenção humana.
    """
    return envio_email.enviar_email(request)

@mcp.tool("rastreio_pedido")
def rastreio_pedido_endpoint(pergunta: Pergunta):
    """
    Use esta ferramenta exclusivamente para rastrear o status de um pedido quando um código de rastreamento for fornecido ou solicitado.
    """
    return {"resposta": rastreio_pedido.rastrear_pedido(pergunta.pergunta_usuario)}

@mcp.tool("default_response")
def conhecimento_geral_endpoint(pergunta: Pergunta):
    """
    FALLBACK: Use esta ferramenta APENAS se a pergunta do usuário NÃO se encaixar em nenhuma outra ferramenta.
    É ideal para questões abertas sobre a marca, sugestões de produtos, ou conversas gerais sobre moda.
    Exemplos: 'Vocês têm alguma iniciativa de sustentabilidade?', 'Qual o tecido dessa camisa?'.
    """
    return {"resposta": default_response.resposta_default(pergunta.pergunta_usuario)}
