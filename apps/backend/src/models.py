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
    source: str = Field(..., description="Source platform (google/apple/trustpilot)")
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
    trustpilot_reviews: int = Field(..., description="Number of Trustpilot reviews")


class ReviewsResponse(BaseModel):
    """Response model for reviews endpoint."""

    reviews: list[AppReview] = Field(..., description="List of reviews")
    stats: ReviewStats = Field(..., description="Review statistics")
    fetched_at: str = Field(..., description="Timestamp when reviews were fetched")
    time_range_hours: int = Field(..., description="Time range in hours")


# AI Analysis Models
class SentimentAnalysis(BaseModel):
    """Sentiment analysis result for a review."""
    
    sentiment: str = Field(..., description="Overall sentiment: positive, negative, neutral")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    emotional_tone: str = Field(..., description="Emotional tone: happy, frustrated, satisfied, disappointed, etc.")
    intensity: str = Field(..., description="Intensity level: low, medium, high")


class IntentClassification(BaseModel):
    """Intent classification for a review."""
    
    primary_intent: str = Field(..., description="Primary user intent: praise, complaint, question, suggestion, bug_report")
    secondary_intents: list[str] = Field(default=[], description="Secondary intents if any")
    urgency: str = Field(..., description="Urgency level: low, medium, high, critical")
    action_required: bool = Field(..., description="Whether this review requires action")


class TopicExtraction(BaseModel):
    """Topic extraction result for a review."""
    
    main_topics: list[str] = Field(..., description="Main topics mentioned in the review")
    subtopics: list[str] = Field(default=[], description="Subtopics and specific issues")
    keywords: list[str] = Field(..., description="Key keywords and phrases")
    categories: list[str] = Field(..., description="Categorized topics: ui_ux, performance, features, support, pricing, etc.")


class ReputationInsight(BaseModel):
    """Individual reputation insight for a review."""
    
    review_id: str = Field(..., description="ID of the analyzed review")
    sentiment: SentimentAnalysis = Field(..., description="Sentiment analysis")
    intent: IntentClassification = Field(..., description="Intent classification")
    topics: TopicExtraction = Field(..., description="Topic extraction")
    priority_score: float = Field(..., ge=0.0, le=10.0, description="Priority score for action (0-10)")
    recommended_action: str = Field(..., description="Recommended action: none, respond, investigate, escalate")


class ReputationScore(BaseModel):
    """Overall reputation score and metrics."""
    
    overall_score: float = Field(..., ge=0.0, le=10.0, description="Overall reputation score (0-10)")
    sentiment_distribution: dict[str, int] = Field(..., description="Distribution of sentiments")
    top_issues: list[str] = Field(..., description="Top issues mentioned by users")
    positive_aspects: list[str] = Field(..., description="Most praised aspects")
    improvement_areas: list[str] = Field(..., description="Areas that need improvement")
    trend: str = Field(..., description="Trend: improving, declining, stable")


class PriorityIssue(BaseModel):
    """High priority issue that requires attention."""
    
    issue: str = Field(..., description="Description of the issue")
    frequency: int = Field(..., description="How many times this issue was mentioned")
    severity: str = Field(..., description="Severity: low, medium, high, critical")
    affected_users: int = Field(..., description="Number of users affected")
    recommended_response: str = Field(..., description="Recommended response strategy")
    department: str = Field(..., description="Which department should handle: product, support, pr, engineering")


class ReputationAnalysisResponse(BaseModel):
    """Response model for reputation analysis endpoint."""
    
    reviews: list[AppReview] = Field(..., description="List of analyzed reviews")
    insights: list[ReputationInsight] = Field(..., description="AI insights for each review")
    reputation_score: ReputationScore = Field(..., description="Overall reputation analysis")
    priority_issues: list[PriorityIssue] = Field(..., description="High priority issues requiring action")
    stats: ReviewStats = Field(..., description="Review statistics")
    analyzed_at: str = Field(..., description="Timestamp when analysis was performed")
    time_range_hours: int = Field(..., description="Time range in hours")
