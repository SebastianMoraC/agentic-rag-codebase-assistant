from typing import List
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class AgentStateType(BaseModel):
    user_id: str = Field(description="The ID of the user making the query")
    query: str = Field(description="The query submitted by the user")
    messages: List[BaseMessage] = Field(default_factory=list)
    retrieval_retry_count: int = Field(default=0, description="Counter to track retrieval retries")
    user_response: str = Field(description="The response to the user's query", default="")


class RetrievalGradeType(BaseModel):
    binary_score: str = Field(description="Relevance score 'yes' or 'no'")


class ResponseEvaluationType(BaseModel):
    is_relevant: bool = Field(description="Whether the response addresses the user's question")
    needs_rewriting: bool = Field(description="Whether the query should be rewritten for better retrieval")
