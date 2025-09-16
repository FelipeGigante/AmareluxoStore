from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]

class DuvidasFAQState(TypedDict):
    messages: List[BaseMessage]
    resposta: str

class SupervisorState(TypedDict):
    supervisor: AgentState
    duvidas_faq: DuvidasFAQState