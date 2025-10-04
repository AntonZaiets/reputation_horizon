"""Pydantic models for request/response validation."""

from datetime import datetime

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


# Review-related models
class AppReview(BaseModel):
    """A single app review."""

    id: str = Field(..., description="Review ID")
    author: str = Field(..., description="Review author name")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    title: str | None = Field(None, description="Review title")
    content: str = Field(..., description="Review text content")
    date: str = Field(..., description="Review date")
    source: str = Field(..., description="Source platform (google/apple)")
    helpful_count: int | None = Field(None, description="Number of helpful votes")
    app_version: str | None = Field(None, description="App version reviewed")


class ReviewStats(BaseModel):
    """Statistics for reviews."""

    total_reviews: int = Field(..., description="Total number of reviews")
    average_rating: float = Field(..., ge=0, le=5, description="Average rating")
    rating_distribution: dict[str, int] = Field(
        ..., description="Distribution of ratings (1-5 stars)"
    )
    google_reviews: int = Field(..., description="Number of Google Play reviews")
    apple_reviews: int = Field(..., description="Number of App Store reviews")


class ReviewsResponse(BaseModel):
    """Response model for reviews endpoint."""

    reviews: list[AppReview] = Field(..., description="List of reviews")
    stats: ReviewStats = Field(..., description="Review statistics")
    fetched_at: str = Field(..., description="Timestamp when reviews were fetched")
    time_range_hours: int = Field(..., description="Time range in hours")
