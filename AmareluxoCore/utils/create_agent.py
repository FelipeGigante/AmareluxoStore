from langgraph.prebuilt import create_react_agent

class AgentCreator:
    def __init__(self, model, tools: list, prompt: str):
        self.model = model
        self.tools = tools
        self.prompt = prompt

    def create_agent(self):
        agent = create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=self.prompt
        )
        return agent