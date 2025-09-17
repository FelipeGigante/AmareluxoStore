<h1 align="center"> StudyBuddy - Sistema de Atendimento Inteligente </h1>

<p align="center">
  <img src="https://ibb.co/kVtnZWLN" alt="StudyBuddy Banner" width="100%">
</p>

## Sobre o Projeto

Esse projeto é um sistema de atendimento inteligente desenvolvido para a Amareluxo, uma loja de roupas e acessórios que busca inovar na experiência de atendimento ao cliente. O sistema utiliza IA para automatizar respostas a perguntas frequentes, rastreamento de pedidos e gerenciamento de comunicações.

## Sobre a Amareluxo

A Amareluxo é uma loja especializada em moda e acessórios, oferecendo produtos de alta qualidade e atendimento personalizado. Com o crescimento das vendas online, surgiu a necessidade de um sistema inteligente para otimizar o atendimento ao cliente e gerenciar as operações de forma mais eficiente.

## Tecnologias Utilizadas

- Python 3.10+
- LangChain
- LangGraph
- OpenAI API
- FastAPI
- Docker

## Instalação e Configuração

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Conta OpenAI (para API key)

### Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Amareluxo.git
cd StudyBuddy
```

2. Crie o arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua-chave-api
```

### Usando Docker

1. Construa as imagens:
```bash
docker-compose build
```

2. Inicie os containers:
```bash
docker-compose up -d
```

### Instalação Manual

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Funcionalidades Principais

- **FAQ Automatizado**: Responde perguntas frequentes sobre produtos, envios e políticas
- **Rastreamento de Pedidos**: Integração com APIs de rastreio
- **Gestão de E-mails**: Automação de respostas e encaminhamento para atendimento humano
- **Sistema de Roteamento Inteligente**: Direciona queries para os agentes especializados

## Uso

```python
from AmareluxoCore.supervisor import SupervisorAgent

supervisor = SupervisorAgent()
response = supervisor.handle_message("Qual o status do meu pedido #123?")
```

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Contato

Felipe Gigante - [@felipegigante](https://www.linkedin.com/in/felipegigante/)
