from typing import TypedDict, List

class AgentState(TypedDict):
    question: str
    intent: str  # disease, scheme, or hybrid
    context: str
    answer: str
    success: bool