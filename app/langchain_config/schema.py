from typing import Literal
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from typing import Annotated


class OverallState(MessagesState):
    question: str
    type: Annotated[str, Field(description="Type of the question")]
    graph_search_data: list[dict]
    vector_search_data: list[dict]
    hybrid_search_data: list[dict]
    answer: str


class GuardrailsOutput(BaseModel):
    decision: Literal[
        "vector_search", "graph_search", "hybrid_search", "non_legal_questions"
    ] = Field(
        ..., description="Decision on whether the question is related to law or not"
    )
