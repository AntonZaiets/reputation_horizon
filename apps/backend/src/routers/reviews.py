"""Reviews API router for fetching app reviews via Wextractor."""

import logging

from fastapi import APIRouter, HTTPException, Query

from src.models import ReviewsResponse
from src.services import WextractorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

# Initialize service
wextractor_service = WextractorService()


@router.get("", response_model=ReviewsResponse)
async def get_preply_reviews(
    hours: int = Query(
        24, ge=1, le=168, description="Number of hours to look back (max 7 days)"
    ),
) -> ReviewsResponse:
    """
    Get Preply app reviews from the last N hours.

    Fetches reviews from both Google Play and App Store using Wextractor API.

    **Parameters:**
    - **hours**: Time range in hours (1-168, default: 24)

    **Returns:**
    - List of reviews with statistics

    **Note:** This endpoint currently uses mock data for development.
    Update the API endpoints in `src/services/wextractor.py` once you have
    the actual Wextractor API documentation.
    """
    try:
        logger.info(f"Fetching reviews for the last {hours} hours")

        result = await wextractor_service.get_reviews(hours=hours)

        return ReviewsResponse(**result)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch reviews: {str(e)}")


@router.get("/google", response_model=ReviewsResponse)
async def get_google_reviews(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
) -> ReviewsResponse:
    """
    Get only Google Play reviews.

    **Future enhancement:** Currently returns all reviews but filtered by source.
    Can be optimized to call only Google Play API.
    """
    try:
        result = await wextractor_service.get_reviews(hours=hours)

        # Filter only Google reviews
        google_reviews = [r for r in result["reviews"] if r.source == "google"]

        result["reviews"] = google_reviews
        result["stats"].apple_reviews = 0
        result["stats"].total_reviews = len(google_reviews)

        return ReviewsResponse(**result)

    except Exception as e:
        logger.error(f"Error fetching Google reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/apple", response_model=ReviewsResponse)
async def get_apple_reviews(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
) -> ReviewsResponse:
    """
    Get only App Store reviews.

    **Future enhancement:** Currently returns all reviews but filtered by source.
    Can be optimized to call only App Store API.
    """
    try:
        result = await wextractor_service.get_reviews(hours=hours)

        # Filter only Apple reviews
        apple_reviews = [r for r in result["reviews"] if r.source == "apple"]

        result["reviews"] = apple_reviews
        result["stats"].google_reviews = 0
        result["stats"].total_reviews = len(apple_reviews)

        return ReviewsResponse(**result)

    except Exception as e:
        logger.error(f"Error fetching Apple reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))

