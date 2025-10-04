"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(..., description="Role of the message sender (user/assistant/system)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., description="User's message to the LLM", min_length=1)
    conversation_id: str | None = Field(None, description="Optional conversation ID for context")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="LLM's response")
    conversation_id: str = Field(..., description="Conversation ID for tracking")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    message: str
    llm_provider: str

