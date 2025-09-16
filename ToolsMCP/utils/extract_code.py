import openai

def extrair_codigo_rastreio(mensagem: str) -> str:
    """
    Extrair o código de rastreio da mensagem.

    Args:
        mensagem (str): A mensagem de texto que pode conter um código de rastreio.

    """
    prompt = (
        f"""Extraia o código de rastreio da seguinte mensagem. 
        Um código de rastreio é uma sequência de letras e números, como 'LL123456789BR' ou 'SS123456789BR'. 
        Retorne apenas o código, sem texto adicional. 
        Se nenhum código for encontrado, retorne a palavra 'NENHUM'.\n\n
        Mensagem: {mensagem}\n\n"
        Código de Rastreio:"""
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=30,
            temperature=0,
            stop=["\n"]
        )
        
        codigo = response.choices[0].text.strip()
        
        if codigo.lower() == "nenhum":
            return ValueError("Não foi possível encontrar um código de rastreio na mensagem.")
        
        return codigo
    
    except openai.error.OpenAIError as e:
        return f"Erro na chamada da API da OpenAI: {e}"