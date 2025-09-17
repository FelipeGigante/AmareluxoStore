from pydantic import BaseModel

class RouteOutput(BaseModel):
    next_agent: str