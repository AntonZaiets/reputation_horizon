"""Service for managing review data with caching."""

import logging
from typing import Optional

from src.models import ReviewsResponse
from src.services.cache import CacheService
from src.services.wextractor import WextractorService

logger = logging.getLogger(__name__)


class ReviewService:
    """Service for managing review data with caching capabilities."""

    def __init__(self):
        """Initialize the review service with caching."""
        self.wextractor_service = WextractorService()
        self.cache_service = CacheService()
        
        # Cache configuration
        self.default_cache_duration_hours = 24
        self.max_cache_age_hours = 24

    async def get_reviews(
        self,
        hours: int = 24,
        source_filter: Optional[str] = None,
        cached: bool = True,
        force_refresh: bool = False,
        max_pages: int = 20
    ) -> ReviewsResponse:
        """
        Get reviews with optional caching.
        
        Args:
            hours: Number of hours to look back
            source_filter: Optional source filter ('google' or 'apple')
            cached: Whether to use cached data (default: True)
            force_refresh: Force refresh even if cache exists
            max_pages: Maximum number of Trustpilot pages to fetch
            
        Returns:
            ReviewsResponse with reviews and statistics
        """
        try:
            # Try cache first if enabled and not forcing refresh
            if cached and not force_refresh:
                cached_response = self.cache_service.get_cached_reviews(
                    hours=hours,
                    source_filter=source_filter,
                    max_age_hours=self.max_cache_age_hours
                )
                
                if cached_response:
                    logger.info(f"Served {len(cached_response.reviews)} reviews from cache")
                    return cached_response

            # Fetch fresh data from Wextractor
            logger.info(f"Fetching fresh reviews for {hours} hours from Wextractor API")
            fresh_response = await self.wextractor_service.get_reviews(hours=hours, max_pages=max_pages)
            
            # Apply source filter if specified
            if source_filter:
                filtered_reviews = [
                    r for r in fresh_response["reviews"] 
                    if r.source == source_filter
                ]
                fresh_response["reviews"] = filtered_reviews
                
                # Update stats
                fresh_response["stats"].google_reviews = (
                    len([r for r in filtered_reviews if r.source == "google"])
                )
                fresh_response["stats"].apple_reviews = (
                    len([r for r in filtered_reviews if r.source == "apple"])
                )
                fresh_response["stats"].total_reviews = len(filtered_reviews)

            # Create response object
            response = ReviewsResponse(**fresh_response)
            
            # Cache the response if caching is enabled
            if cached:
                try:
                    self.cache_service.cache_reviews(
                        reviews_response=response,
                        hours=hours,
                        source_filter=source_filter,
                        cache_duration_hours=self.default_cache_duration_hours
                    )
                    logger.info(f"Cached {len(response.reviews)} reviews")
                except Exception as e:
                    logger.warning(f"Failed to cache reviews: {e}")
                    # Don't fail the request if caching fails

            return response

        except Exception as e:
            logger.error(f"Error in get_reviews: {e}")
            raise

    async def get_google_reviews(
        self,
        hours: int = 24,
        cached: bool = True,
        force_refresh: bool = False,
        max_pages: int = 20
    ) -> ReviewsResponse:
        """Get Google Play reviews with caching."""
        return await self.get_reviews(
            hours=hours,
            source_filter="google",
            cached=cached,
            force_refresh=force_refresh,
            max_pages=max_pages
        )

    async def get_apple_reviews(
        self,
        hours: int = 24,
        cached: bool = True,
        force_refresh: bool = False,
        max_pages: int = 20
    ) -> ReviewsResponse:
        """Get App Store reviews with caching."""
        return await self.get_reviews(
            hours=hours,
            source_filter="apple",
            cached=cached,
            force_refresh=force_refresh,
            max_pages=max_pages
        )

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        return self.cache_service.get_cache_stats()

    def clear_cache(self, cache_key: Optional[str] = None) -> None:
        """Clear cache entries."""
        self.cache_service.clear_cache(cache_key)

    def cleanup_expired_cache(self) -> None:
        """Clean up expired cache entries."""
        self.cache_service._cleanup_expired_cache()
