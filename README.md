<div align="center">
  <img src="https://i.ibb.co/ymrT2bzH/amareluxo.png" alt="amareluxo" border="0" width="30%" height="30%">
  <h1>Sistema de Atendimento Inteligente Amareluxo</h1>
  <p>Um assistente de IA avançado para e-commerce, orquestrado com LangGraph e servido via Streamlit e FastMCP.</p>
  
  <p>
    <img alt="Status" src="https://img.shields.io/badge/status-ativo-brightgreen">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue">
    <img alt="License" src="https://img.shields.io/badge/licen%C3%A7a-MIT-purple">
  </p>
</div>

## 🎯 Sobre o Projeto

Este projeto implementa um sistema de atendimento inteligente para a **Amareluxo**, uma loja de roupas e acessórios. O objetivo é criar uma experiência de suporte ao cliente fluida e eficiente, utilizando uma arquitetura de agentes de IA para automatizar tarefas como responder a perguntas frequentes, rastrear pedidos e escalar problemas complexos para atendimento humano.

## ✨ Funcionalidades Principais

- **🤖 Agente de FAQ Automatizado**: Responde a dúvidas sobre políticas da loja, pagamentos e envios.
- **🚚 Rastreamento de Pedidos**: Permite que o cliente consulte o status de sua entrega em tempo real.
- **📧 Abertura de Tickets de Suporte**: Encaminha problemas complexos para a equipe de suporte humano via e-mail.
- **🧠 Conhecimento Geral**: Responde a perguntas abertas sobre a marca, produtos e moda.
- **🧭 Roteamento Inteligente**: Um supervisor em LangGraph analisa e direciona cada pergunta para o fluxo correto.

## 🏗️ Arquitetura

O sistema é desacoplado em dois serviços principais que se comunicam via rede Docker:

1.  **Backend de Ferramentas (`ToolsMCP`)**: Um servidor `FastMCP` que expõe a lógica de negócios (acesso ao banco de dados, consulta a APIs externas) como ferramentas de IA.
2.  **Frontend e Orquestração (`AmareluxoCore`)**: Uma interface `Streamlit` onde o usuário interage. O backend da interface usa `LangGraph` para orquestrar o `MCPAgent`, que consome as ferramentas do servidor `FastMCP`.

## 🚀 Tecnologias Utilizadas

| Categoria              | Tecnologia                   | Descrição                                                                    |
| :--------------------- | :--------------------------- | :--------------------------------------------------------------------------- |
| **Orquestração de IA** | `LangChain` / `LangGraph`    | Para criar e conectar os agentes de IA em um grafo de estados.               |
| **Modelos de Linguagem**| `OpenAI GPT-4o` / `Google Gemini` | Modelos usados para roteamento e geração de respostas.                       |
| **Servidor de Ferramentas** | `FastMCP`                    | Para expor as funções Python como ferramentas de IA de forma eficiente.      |
| **Cliente de Ferramentas** | `mcp-use`                    | Para consumir as ferramentas do `FastMCP` de maneira simplificada no agente. |
| **Interface do Usuário**| `Streamlit`                  | Para criar a interface de chat interativa.                                   |
| **Containerização** | `Docker` / `Docker Compose`  | Para criar e gerenciar os ambientes isolados da aplicação e do servidor.   |

## 🏁 Começando

A maneira recomendada para executar o projeto é usando Docker.

### Pré-requisitos

- **Git**: Para clonar o repositório.
- **Docker e Docker Compose**: Para construir e orquestrar os contêineres.
- **Chaves de API**:
  - `OPENAI_API_KEY`: Para os modelos da OpenAI.
  - `GOOGLE_API_KEY`: Para os modelos do Google Gemini.

### 1. Configuração do Ambiente

Primeiro, clone o repositório e configure as variáveis de ambiente.

1.  **Clone o projeto:**
    ```bash
    git clone [https://github.com/FelipeGigante/AmareluxoStore.git](https://github.com/FelipeGigante/AmareluxoStore.git)
    cd AmareluxoStore
    ```

2.  **Crie o arquivo `.env`**: Crie um arquivo chamado `.env` na raiz do projeto, copiando o exemplo abaixo. Este arquivo será usado por ambos os contêineres.

    ```env
    # Chaves para os modelos de linguagem
    OPENAI_API_KEY="sk-..."
    GOOGLE_API_KEY="..."

    # URL que o cliente (Streamlit/LangGraph) usará para encontrar o servidor de ferramentas
    # IMPORTANTE: Dentro do Docker, um contêiner se refere a outro pelo nome do serviço.
    MCP_SERVER_URL="http://api:9000/mcp"
    ```

### 2. Executando com Docker

Com o Docker e o arquivo `.env` prontos, você pode iniciar a aplicação com dois comandos.

1.  **Construa as imagens Docker:**
    ```bash
    docker-compose build
    ```

2.  **Inicie os serviços em modo detached (-d):**
    ```bash
    docker-compose up -d
    ```

A aplicação estará disponível em:
- **🖥️ Interface de Chat**: `http://localhost:8501`
- **⚙️ API de Ferramentas**: `http://localhost:9000` (você pode acessar a documentação gerada pelo FastMCP aqui)

Para parar os serviços, execute:
```bash
docker-compose down
```

## 📁 Estrutura do Projeto
```bash
.
├── AmareluxoCore/       # Contém a aplicação Streamlit, o Supervisor e o Agente.
│   ├── main.py
│   ├── supervisor.py
│   ├── amareluxo_agent.py
│   └── ...
├── ToolsMCP/            # Contém o servidor FastMCP e a definição das ferramentas.
│   ├── server.py
│   ├── tools/
│   └── ...
├── .env                 # (Você precisa criar) Armazena as chaves de API.
├── docker-compose.yml   # Orquestra os contêineres.
└── README.md
```

## 🤝 Contribuindo

1.  Faça um Fork do projeto.
2.  Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4.  Push para a Branch (`git push origin feature/AmazingFeature`).
5.  Abra um Pull Request.

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 👨‍💻 Contato

**Felipe Gigante** - [LinkedIn](https://www.linkedin.com/in/felipegigante/) - [GitHub](https://github.com/FelipeGigante)
