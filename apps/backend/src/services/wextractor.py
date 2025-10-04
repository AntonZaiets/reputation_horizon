"""Wextractor API service for fetching app reviews."""

import logging
from datetime import datetime, timedelta
from time import sleep

import httpx

from src.config import settings
from src.models import AppReview, ReviewStats

logger = logging.getLogger(__name__)


class WextractorService:
    """Service for interacting with Wextractor API."""

    def __init__(self):
        self.api_key = settings.wextractor_api_key
        self.api_url = settings.wextractor_api_url
        self.google_app_id = settings.preply_app_id_google
        self.apple_app_id = settings.preply_app_id_apple

        if not self.api_key:
            logger.warning("WEXTRACTOR_API_KEY not set in environment")

    async def get_reviews(self, hours: int = 24) -> dict:
        """
        Fetch reviews from the last N hours.

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            Dictionary containing reviews and statistics

        Raises:
            ValueError: If API key is not configured
            httpx.HTTPError: If API request fails
        """

        if not self.api_key:
            raise ValueError("WEXTRACTOR_API_KEY not configured")

        # Calculate time threshold
        time_threshold = datetime.now() - timedelta(hours=hours)

        # Fetch from both platforms
        google_reviews = await self._fetch_google_reviews(hours)
        apple_reviews = await self._fetch_apple_reviews(hours)

        # Combine and process reviews
        all_reviews = google_reviews + apple_reviews

        # Sort by date (newest first)
        all_reviews.sort(key=lambda x: x.date, reverse=True)

        # Calculate statistics
        stats = self._calculate_stats(all_reviews, len(google_reviews), len(apple_reviews))

        return {
            "reviews": all_reviews,
            "stats": stats,
            "fetched_at": datetime.now().isoformat(),
            "time_range_hours": hours,
        }

    async def _fetch_google_reviews(self, hours: int) -> list[AppReview]:
        """
        Fetch Google Play reviews.

        Update the endpoint URL and parameters based on actual Wextractor API documentation.

        Raises:
            httpx.HTTPError: If API request fails
        """
        async with httpx.AsyncClient(timeout=30.0) as client:

            url = f"{self.api_url}/api/v1/reviews/googleplay"

            params = {
                "id": self.google_app_id,
                "auth_token": self.api_key,
                "offset": 0,
            }

            logger.info(f"Fetching Google Play reviews from {url}")
            logger.debug(f"Request params: {params}")

            response = await client.get(url, params=params)

            # Log response details for debugging
            logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"Response body: {response.text}")

            response.raise_for_status()
            data = response.json()

            # Parse response - adjust based on actual API response format
            return self._parse_google_reviews(data)

    async def _fetch_apple_reviews(self, hours: int) -> list[AppReview]:
        """
        Fetch App Store reviews.

        Update the endpoint URL and parameters based on actual Wextractor API documentation.

        Raises:
            httpx.HTTPError: If API request fails
        """
        print("here fetch apple reviews")
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.api_url}/api/v1/reviews/appstore?"

            params = {
                "id": self.apple_app_id,
                "auth_token": self.api_key,
                "offset": 0,
            }

            logger.info(f"Fetching App Store reviews from {url}")
            logger.debug(f"Request params: {params}")

            response = await client.get(url, params=params)

            # Log response details for debugging
            logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"Response body: {response.text}")

            response.raise_for_status()
            data = response.json()

            return self._parse_apple_reviews(data)

    def _parse_google_reviews(self, data: dict) -> list[AppReview]:
        """
        Parse Google Play reviews from API response.

        Adjust this based on actual Wextractor API response format.
        Expected format:
        {
            "reviews": [
                {
                    "id": "...",
                    "author": "...",
                    "rating": 5,
                    "title": "...",
                    "content": "...",
                    "date": "...",
                    "helpful_count": 10,
                    "app_version": "1.0.0"
                }
            ]
        }
        """
        reviews = []
        raw_reviews = data.get("reviews", [])

        logger.info(f"Parsing {len(raw_reviews)} Google Play reviews")

        for review in raw_reviews:
            try:
                reviews.append(
                    AppReview(
                        id=review.get("id", ""),
                        author=review.get("author", "Anonymous"),
                        rating=review.get("rating", 0),
                        title=review.get("title"),
                        content=review.get("content", ""),
                        date=review.get("date", datetime.now().isoformat()),
                        source="google",
                        helpful_count=review.get("helpful_count"),
                        app_version=review.get("app_version"),
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse review: {e}")
                logger.debug(f"Review data: {review}")
                continue

        return reviews

    def _parse_apple_reviews(self, data: dict) -> list[AppReview]:
        """
        Parse App Store reviews from API response.

        Adjust this based on actual Wextractor API response format.
        """
        reviews = []
        raw_reviews = data.get("reviews", [])

        logger.info(f"Parsing {len(raw_reviews)} App Store reviews")

        for review in raw_reviews:
            try:
                reviews.append(
                    AppReview(
                        id=review.get("id", ""),
                        author=review.get("author", "Anonymous"),
                        rating=review.get("rating", 0),
                        title=review.get("title"),
                        content=review.get("content", ""),
                        date=review.get("date", datetime.now().isoformat()),
                        source="apple",
                        helpful_count=review.get("helpful_count"),
                        app_version=review.get("app_version"),
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse review: {e}")
                logger.debug(f"Review data: {review}")
                continue

        return reviews

    def _calculate_stats(
        self, reviews: list[AppReview], google_count: int, apple_count: int
    ) -> ReviewStats:
        """Calculate review statistics."""
        if not reviews:
            return ReviewStats(
                total_reviews=0,
                average_rating=0.0,
                rating_distribution={"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
                google_reviews=0,
                apple_reviews=0,
            )

        # Calculate rating distribution
        rating_dist = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        total_rating = 0

        for review in reviews:
            rating_dist[str(review.rating)] += 1
            total_rating += review.rating

        avg_rating = round(total_rating / len(reviews), 2) if reviews else 0.0

        return ReviewStats(
            total_reviews=len(reviews),
            average_rating=avg_rating,
            rating_distribution=rating_dist,
            google_reviews=google_count,
            apple_reviews=apple_count,
        )
