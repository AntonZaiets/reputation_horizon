"""Reputation analysis API router using OpenAI."""

import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query

from src.models import ReputationAnalysisResponse
from src.services import WextractorService
from src.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reputation", tags=["reputation"])

# Initialize services
wextractor_service = WextractorService()
openai_service = OpenAIService()


@router.get("/analyze", response_model=ReputationAnalysisResponse)
async def analyze_reputation(
    hours: int = Query(
        24, ge=1, le=168, description="Number of hours to look back (max 7 days)"
    ),
    max_reviews: int = Query(
        50, ge=1, le=100, description="Maximum number of reviews to analyze"
    ),
) -> ReputationAnalysisResponse:
    """
    Analyze app reputation using AI-powered insights.

    This endpoint fetches recent reviews and performs comprehensive analysis including:
    - Sentiment analysis
    - Intent classification  
    - Topic extraction
    - Priority scoring
    - Reputation metrics

    **Parameters:**
    - **hours**: Time range in hours (1-168, default: 24)
    - **max_reviews**: Maximum reviews to analyze (1-100, default: 50)

    **Returns:**
    - Comprehensive reputation analysis with AI insights

    **Errors:**
    - 500: Analysis failed or API configuration error
    - 503: External service unavailable
    """
    try:
        logger.info(f"Starting reputation analysis for last {hours} hours, max {max_reviews} reviews")
        
        # Fetch reviews
        reviews_data = await wextractor_service.get_reviews(hours=hours)
        reviews = reviews_data["reviews"][:max_reviews]  # Limit reviews for analysis
        
        if not reviews:
            logger.warning("No reviews found for analysis")
            return ReputationAnalysisResponse(
                reviews=[],
                insights=[],
                reputation_score=openai_service._get_mock_reputation_analysis()["reputation_score"],
                priority_issues=[],
                stats=reviews_data["stats"],
                analyzed_at=reviews_data["fetched_at"],
                time_range_hours=hours
            )

        logger.info(f"Analyzing {len(reviews)} reviews with OpenAI")
        
        # Perform AI analysis
        analysis_result = await openai_service.analyze_reputation_batch(reviews)
        
        logger.info("Reputation analysis completed successfully")
        
        return ReputationAnalysisResponse(
            reviews=reviews,
            insights=analysis_result["insights"],
            reputation_score=analysis_result["reputation_score"],
            priority_issues=analysis_result["priority_issues"],
            stats=reviews_data["stats"],
            analyzed_at=reviews_data["fetched_at"],
            time_range_hours=hours
        )

    except Exception as e:
        logger.error(f"Error in reputation analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Reputation analysis failed: {str(e)}"
        )


@router.get("/insights/{review_id}")
async def get_review_insight(review_id: str):
    """
    Get detailed AI insight for a specific review.
    
    **Parameters:**
    - **review_id**: ID of the review to analyze
    
    **Returns:**
    - Detailed insight for the specific review
    """
    try:
        # This would typically fetch the review from database
        # For now, we'll return a mock response
        logger.info(f"Getting insight for review {review_id}")
        
        # In a real implementation, you would:
        # 1. Fetch the review from your database
        # 2. Analyze it with OpenAI
        # 3. Return the insight
        
        return {
            "review_id": review_id,
            "message": "Individual review insights not yet implemented",
            "note": "Use /analyze endpoint for batch analysis"
        }
        
    except Exception as e:
        logger.error(f"Error getting review insight: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get review insight: {str(e)}"
        )


@router.get("/summary")
async def get_reputation_summary(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back")
):
    """
    Get a quick reputation summary without full analysis.
    
    **Parameters:**
    - **hours**: Time range in hours (1-168, default: 24)
    
    **Returns:**
    - Quick reputation summary
    """
    try:
        logger.info(f"Getting reputation summary for last {hours} hours")
        
        # Fetch basic review data
        reviews_data = await wextractor_service.get_reviews(hours=hours)
        reviews = reviews_data["reviews"]
        
        if not reviews:
            return {
                "message": "No reviews found",
                "summary": {
                    "total_reviews": 0,
                    "average_rating": 0,
                    "sentiment_overview": "No data"
                }
            }
        
        # Calculate basic metrics
        total_reviews = len(reviews)
        avg_rating = sum(r.rating for r in reviews) / total_reviews
        
        # Simple sentiment calculation based on ratings
        positive_count = len([r for r in reviews if r.rating >= 4])
        negative_count = len([r for r in reviews if r.rating <= 2])
        
        sentiment_overview = "positive" if positive_count > negative_count else "negative" if negative_count > positive_count else "neutral"
        
        return {
            "summary": {
                "total_reviews": total_reviews,
                "average_rating": round(avg_rating, 2),
                "sentiment_overview": sentiment_overview,
                "positive_reviews": positive_count,
                "negative_reviews": negative_count,
                "neutral_reviews": total_reviews - positive_count - negative_count
            },
            "time_range_hours": hours,
            "note": "For detailed AI analysis, use /analyze endpoint"
        }
        
    except Exception as e:
        logger.error(f"Error getting reputation summary: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get reputation summary: {str(e)}"
        )
