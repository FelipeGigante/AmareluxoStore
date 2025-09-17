from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, List

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]