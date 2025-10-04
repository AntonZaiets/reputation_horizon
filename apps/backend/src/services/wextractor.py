"""Wextractor API service for fetching app reviews."""

import logging
from datetime import datetime, timedelta

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

        Note: This is a template. Adjust the endpoint and parameters
        based on actual Wextractor API documentation.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # TODO: Update this endpoint based on actual Wextractor API docs
                # Common patterns:
                # - /api/v1/reviews/google
                # - /api/reviews?platform=google&app_id={app_id}
                url = f"{self.api_url}/reviews/google"

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                params = {
                    "app_id": self.google_app_id,
                    "hours": hours,
                    "limit": 100,  # Adjust as needed
                }

                logger.info(f"Fetching Google Play reviews from {url}")
                response = await client.get(url, headers=headers, params=params)

                if response.status_code == 404:
                    logger.warning(
                        "Wextractor API endpoint not found. Using mock data. "
                        "Update the API endpoint in src/services/wextractor.py"
                    )
                    return self._generate_mock_google_reviews()

                response.raise_for_status()
                data = response.json()

                # Parse response - adjust based on actual API response format
                return self._parse_google_reviews(data)

        except httpx.HTTPError as e:
            logger.error(f"Error fetching Google Play reviews: {e}")
            # Return mock data for development
            return self._generate_mock_google_reviews()

    async def _fetch_apple_reviews(self, hours: int) -> list[AppReview]:
        """
        Fetch App Store reviews.

        Note: This is a template. Adjust the endpoint and parameters
        based on actual Wextractor API documentation.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # TODO: Update this endpoint based on actual Wextractor API docs
                url = f"{self.api_url}/reviews/apple"

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                params = {
                    "app_id": self.apple_app_id,
                    "hours": hours,
                    "limit": 100,
                }

                logger.info(f"Fetching App Store reviews from {url}")
                response = await client.get(url, headers=headers, params=params)

                if response.status_code == 404:
                    logger.warning(
                        "Wextractor API endpoint not found. Using mock data. "
                        "Update the API endpoint in src/services/wextractor.py"
                    )
                    return self._generate_mock_apple_reviews()

                response.raise_for_status()
                data = response.json()

                return self._parse_apple_reviews(data)

        except httpx.HTTPError as e:
            logger.error(f"Error fetching App Store reviews: {e}")
            return self._generate_mock_apple_reviews()

    def _parse_google_reviews(self, data: dict) -> list[AppReview]:
        """
        Parse Google Play reviews from API response.

        TODO: Adjust this based on actual Wextractor API response format.
        """
        reviews = []
        raw_reviews = data.get("reviews", [])

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
                continue

        return reviews

    def _parse_apple_reviews(self, data: dict) -> list[AppReview]:
        """Parse App Store reviews from API response."""
        reviews = []
        raw_reviews = data.get("reviews", [])

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

    # Mock data methods for development/testing
    def _generate_mock_google_reviews(self) -> list[AppReview]:
        """Generate mock Google Play reviews for testing."""
        return [
            AppReview(
                id="google_1",
                author="John Doe",
                rating=5,
                title="Excellent app!",
                content="Great for learning languages. Highly recommend!",
                date=(datetime.now() - timedelta(hours=2)).isoformat(),
                source="google",
                helpful_count=15,
                app_version="1.2.3",
            ),
            AppReview(
                id="google_2",
                author="Jane Smith",
                rating=4,
                title="Good but could be better",
                content="Nice app, but sometimes has connection issues.",
                date=(datetime.now() - timedelta(hours=5)).isoformat(),
                source="google",
                helpful_count=8,
                app_version="1.2.3",
            ),
        ]

    def _generate_mock_apple_reviews(self) -> list[AppReview]:
        """Generate mock App Store reviews for testing."""
        return [
            AppReview(
                id="apple_1",
                author="User123",
                rating=5,
                title="Love it!",
                content="Perfect for language learning. Worth every penny.",
                date=(datetime.now() - timedelta(hours=1)).isoformat(),
                source="apple",
                helpful_count=22,
                app_version="1.2.3",
            ),
            AppReview(
                id="apple_2",
                author="LangLearner",
                rating=3,
                title="Okay",
                content="It works but the UI could be improved.",
                date=(datetime.now() - timedelta(hours=4)).isoformat(),
                source="apple",
                helpful_count=5,
                app_version="1.2.2",
            ),
        ]

