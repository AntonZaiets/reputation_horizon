"""Reviews API router for fetching app reviews via Wextractor with caching and Trustpilot support."""

import logging
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from src.models import ReviewsResponse
from src.services.review_service import ReviewService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

# Initialize service
review_service = ReviewService()


@router.get("", response_model=ReviewsResponse)
async def get_preply_reviews(
    hours: int = Query(
        24, ge=1, le=168, description="Number of hours to look back (max 7 days)"
    ),
    cached: bool = Query(True, description="Whether to use cached data if available"),
    force_refresh: bool = Query(False, description="Force refresh data even if cache exists"),
    max_pages: int = Query(
        20, ge=1, le=50, description="Maximum number of Trustpilot pages to fetch (1-50, default: 20)"
    ),
) -> ReviewsResponse:
    """
    Get Preply app reviews from the last N hours.

    Fetches reviews from Google Play, App Store, and Trustpilot using Wextractor API.
    Supports caching for improved performance.

    **Parameters:**
    - **hours**: Time range in hours (1–168, default: 24)
    - **cached**: Use cached data if available (default: True)
    - **force_refresh**: Force refresh even if cache exists (default: False)
    - **max_pages**: Number of Trustpilot pages to fetch (1–50)

    **Returns:**
    - List of reviews with statistics
    - `cached` field indicates if data was served from cache
    """
    try:
        logger.info(
            f"Fetching reviews for the last {hours} hours "
            f"(cached={cached}, force_refresh={force_refresh}, trustpilot_pages={max_pages})"
        )

        result = await review_service.get_reviews(
            hours=hours,
            cached=cached,
            force_refresh=force_refresh,
            max_pages=max_pages,
        )

        return result

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Configuration error: {str(e)}. Check WEXTRACTOR_API_KEY in .env file.",
        )
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Wextractor API: {e}")
        status_code = e.response.status_code
        detail = f"Wextractor API error ({status_code}): {e.response.text}"

        if status_code == 404:
            detail = (
                "Wextractor API endpoint not found. "
                "Please verify the API URL and endpoint in src/services/wextractor.py"
            )
        elif status_code == 401:
            detail = "Invalid Wextractor API key. Check WEXTRACTOR_API_KEY in .env file."

        raise HTTPException(status_code=status_code, detail=detail)
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(
            status_code=503, detail=f"Failed to connect to Wextractor API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching reviews: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/google", response_model=ReviewsResponse)
async def get_google_reviews(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
    cached: bool = Query(True, description="Whether to use cached data if available"),
    force_refresh: bool = Query(False, description="Force refresh data even if cache exists"),
) -> ReviewsResponse:
    """Get only Google Play reviews with caching support."""
    try:
        logger.info(f"Fetching Google Play reviews for {hours} hours (cached={cached})")

        result = await review_service.get_google_reviews(
            hours=hours, cached=cached, force_refresh=force_refresh
        )

        return result

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching Google reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/apple", response_model=ReviewsResponse)
async def get_apple_reviews(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
    cached: bool = Query(True, description="Whether to use cached data if available"),
    force_refresh: bool = Query(False, description="Force refresh data even if cache exists"),
) -> ReviewsResponse:
    """Get only App Store reviews with caching support."""
    try:
        logger.info(f"Fetching App Store reviews for {hours} hours (cached={cached})")

        result = await review_service.get_apple_reviews(
            hours=hours, cached=cached, force_refresh=force_refresh
        )

        return result

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching Apple reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trustpilot", response_model=ReviewsResponse)
async def get_trustpilot_reviews(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
    max_pages: int = Query(20, ge=1, le=50, description="Maximum number of pages to fetch"),
    cached: bool = Query(True, description="Whether to use cached data if available"),
    force_refresh: bool = Query(False, description="Force refresh data even if cache exists"),
) -> ReviewsResponse:
    """Get only Trustpilot reviews with caching support."""
    try:
        logger.info(f"Fetching Trustpilot reviews for {hours} hours (cached={cached})")

        result = await review_service.get_trustpilot_reviews(
            hours=hours,
            max_pages=max_pages,
            cached=cached,
            force_refresh=force_refresh,
        )

        return result

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching Trustpilot reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    try:
        stats = review_service.get_cache_stats()
        
        # Also show cache contents for debugging
        review_service.cache_service.debug_cache_contents()
        
        return {
            "cache_stats": stats,
            "message": "Cache statistics retrieved successfully",
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cache")
async def clear_cache(cache_key: Optional[str] = Query(None, description="Specific cache key to clear")):
    """Clear cache entries."""
    try:
        review_service.clear_cache(cache_key)

        if cache_key:
            message = f"Cache cleared for key: {cache_key}"
        else:
            message = "All cache cleared successfully"

        return {"message": message}
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/cleanup")
async def cleanup_expired_cache():
    """Clean up expired cache entries."""
    try:
        review_service.cleanup_expired_cache()
        return {"message": "Expired cache entries cleaned up successfully"}
    except Exception as e:
        logger.error(f"Error cleaning up cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/test")
async def test_cache(hours: int = Query(24, description="Hours to test cache for")):
    """
    Test cache functionality.
    
    This endpoint will:
    1. Try to get cached data
    2. Show cache status
    3. Not make external API calls if cache exists
    """
    try:
        logger.info(f"🧪 Testing cache for {hours} hours")
        
        # Try to get cached data
        cached_response = review_service.cache_service.get_cached_reviews(
            hours=hours,
            max_age_hours=24
        )
        
        if cached_response:
            logger.info(f"✅ Cache test PASSED: Found {len(cached_response.reviews)} cached reviews")
            return {
                "status": "cache_hit",
                "reviews_count": len(cached_response.reviews),
                "cached": True,
                "message": f"Cache working! Found {len(cached_response.reviews)} reviews"
            }
        else:
            logger.info(f"❌ Cache test FAILED: No cached data found")
            return {
                "status": "cache_miss", 
                "reviews_count": 0,
                "cached": False,
                "message": "No cached data found"
            }
            
    except Exception as e:
        logger.error(f"Error testing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))
