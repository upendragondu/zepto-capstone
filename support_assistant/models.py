from typing import TypedDict
from pydantic import BaseModel


class AgentState(TypedDict, total=False):
    question: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float