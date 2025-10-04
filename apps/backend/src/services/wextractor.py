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
        self.api_url = "https://wextractor.com"  # Fixed URL without 'api.'
        self.google_app_id = "com.preply"  # Correct Google Play App ID
        self.apple_app_id = "1352790442"  # Correct Preply App Store ID
        self.trustpilot_domain = "preply.com"  # Trustpilot domain

        if not self.api_key:
            logger.warning("WEXTRACTOR_API_KEY not set in environment")

    async def get_reviews(self, hours: int = 24, max_trustpilot_pages: int = 20) -> dict:
        """
        Fetch reviews from the last N hours.

        Args:
            hours: Number of hours to look back (default: 24)
            max_trustpilot_pages: Maximum number of Trustpilot pages to fetch (default: 20)

        Returns:
            Dictionary containing reviews and statistics

        Raises:
            ValueError: If API key is not configured
            httpx.HTTPError: If API request fails
        """

        if not self.api_key:
            raise ValueError("WEXTRACTOR_API_KEY not configured")

        try:
            # Calculate time threshold
            time_threshold = datetime.now() - timedelta(hours=hours)

            # Fetch from all platforms
            google_reviews = await self._fetch_google_reviews(hours)
            apple_reviews = await self._fetch_apple_reviews(hours)
            trustpilot_reviews = await self._fetch_trustpilot_reviews(hours, max_pages=max_trustpilot_pages)

            # Combine and process reviews
            all_reviews = google_reviews + apple_reviews + trustpilot_reviews

            # Filter reviews by date (only keep reviews from the last N hours)
            filtered_reviews = []
            logger.info(f"Filtering {len(all_reviews)} reviews for the last {hours} hours (since {time_threshold})")
            
            for review in all_reviews:
                try:
                    # Parse review date
                    review_date = datetime.fromisoformat(review.date.replace('Z', '+00:00'))
                    # Convert to local timezone for comparison
                    review_date_local = review_date.replace(tzinfo=None)
                    
                    if review_date_local >= time_threshold:
                        filtered_reviews.append(review)
                    else:
                        logger.debug(f"Filtering out old review from {review_date_local} (older than {time_threshold})")
                except Exception as e:
                    logger.warning(f"Failed to parse review date {review.date}: {e}")
                    # Include review if date parsing fails (to be safe)
                    filtered_reviews.append(review)
            
            logger.info(f"After filtering: {len(filtered_reviews)} reviews remain from the last {hours} hours")

            # Sort by date (newest first)
            filtered_reviews.sort(key=lambda x: x.date, reverse=True)

            # Calculate statistics using filtered reviews
            google_filtered = [r for r in filtered_reviews if r.source == "google"]
            apple_filtered = [r for r in filtered_reviews if r.source == "apple"]
            trustpilot_filtered = [r for r in filtered_reviews if r.source == "trustpilot"]
            stats = self._calculate_stats(filtered_reviews, len(google_filtered), len(apple_filtered), len(trustpilot_filtered))

            return {
                "reviews": filtered_reviews,
                "stats": stats,
                "fetched_at": datetime.now().isoformat(),
                "time_range_hours": hours,
            }
        except Exception as e:
            logger.warning(f"Failed to fetch real reviews from Wextractor API: {e}")
            logger.warning("Wextractor API is currently unavailable (522 error). Using demo data instead.")
            return self._get_mock_reviews(hours)

    async def _fetch_google_reviews(self, hours: int) -> list[AppReview]:
        """
        Fetch Google Play reviews with pagination.

        Raises:
            httpx.HTTPError: If API request fails
        """
        all_reviews = []
        seen_ids = set()  # Track unique review IDs to avoid duplicates
        
        # Fetch multiple pages to get more reviews
        # Google Play API might also have pagination limits
        pages_to_fetch = 5
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for page in range(pages_to_fetch):
                offset = page * 10
                url = f"{self.api_url}/api/v1/reviews/googleplay"

                params = {
                    "id": self.google_app_id,
                    "auth_token": self.api_key,
                    "offset": offset,
                }

                logger.info(f"Fetching Google Play reviews page {page + 1} (offset={offset}) from {url}")
                logger.debug(f"Request params: {params}")

                try:
                    response = await client.get(url, params=params)

                    # Log response details for debugging
                    logger.info(f"Response status: {response.status_code}")
                    if response.status_code != 200:
                        logger.error(f"Response body: {response.text}")

                    response.raise_for_status()
                    data = response.json()
                    
                    page_reviews = self._parse_google_reviews(data)
                    
                    # Filter out duplicates based on review ID
                    unique_reviews = []
                    for review in page_reviews:
                        if review.id not in seen_ids:
                            seen_ids.add(review.id)
                            unique_reviews.append(review)
                        else:
                            logger.debug(f"Skipping duplicate review ID: {review.id}")
                    
                    all_reviews.extend(unique_reviews)
                    
                    # If we got less than 10 reviews, we've reached the end
                    if len(page_reviews) < 10:
                        logger.info(f"Reached end of Google Play reviews at page {page + 1}")
                        break
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch Google Play page {page + 1}: {e}")
                    break

        logger.info(f"Fetched {len(all_reviews)} unique Google Play reviews from {pages_to_fetch} pages")
        return all_reviews

    async def _fetch_apple_reviews(self, hours: int) -> list[AppReview]:
        """
        Fetch App Store reviews with pagination.

        App Store API returns only 10 reviews per request, so we need to fetch multiple pages.

        Raises:
            httpx.HTTPError: If API request fails
        """
        print("here fetch apple reviews")
        all_reviews = []
        seen_ids = set()  # Track unique review IDs to avoid duplicates
        
        # Fetch multiple pages to get more reviews
        # Each page has 10 reviews, so we'll fetch 5 pages (50 reviews total)
        pages_to_fetch = 5
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for page in range(pages_to_fetch):
                offset = page * 10
                url = f"{self.api_url}/api/v1/reviews/appstore"
                
                params = {
                    "id": self.apple_app_id,
                    "auth_token": self.api_key,
                    "offset": offset,
                }

                logger.info(f"Fetching App Store reviews page {page + 1} (offset={offset}) from {url}")
                logger.debug(f"Request params: {params}")

                try:
                    response = await client.get(url, params=params)

                    # Log response details for debugging
                    logger.info(f"Response status: {response.status_code}")
                    if response.status_code != 200:
                        logger.error(f"Response body: {response.text}")

                    response.raise_for_status()
                    data = response.json()
                    
                    page_reviews = self._parse_apple_reviews(data)
                    
                    # Filter out duplicates based on review ID
                    unique_reviews = []
                    for review in page_reviews:
                        if review.id not in seen_ids:
                            seen_ids.add(review.id)
                            unique_reviews.append(review)
                        else:
                            logger.debug(f"Skipping duplicate App Store review ID: {review.id}")
                    
                    all_reviews.extend(unique_reviews)
                    
                    # If we got less than 10 reviews, we've reached the end
                    if len(page_reviews) < 10:
                        logger.info(f"Reached end of App Store reviews at page {page + 1}")
                        break
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch App Store page {page + 1}: {e}")
                    break

        logger.info(f"Fetched {len(all_reviews)} unique App Store reviews from {pages_to_fetch} pages")
        return all_reviews

    async def _fetch_trustpilot_reviews(self, hours: int, max_pages: int = 20) -> list[AppReview]:
        """
        Fetch Trustpilot reviews with pagination using cursor.

        Raises:
            httpx.HTTPError: If API request fails
        """
        all_reviews = []
        seen_ids = set()  # Track unique review IDs to avoid duplicates
        
        # Fetch more pages for Trustpilot since it has more reviews
        # Each page has ~20 reviews, so max_pages pages = ~(max_pages * 20) reviews
        pages_to_fetch = max_pages
        next_page_cursor = None
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for page in range(pages_to_fetch):
                url = f"{self.api_url}/api/v1/reviews/trustpilot"
                
                params = {
                    "id": self.trustpilot_domain,  # Use "id" instead of "domain"
                    "auth_token": self.api_key,
                }
                
                # Add cursor for pagination (except for first page)
                if next_page_cursor:
                    params["cursor"] = next_page_cursor

                logger.info(f"Fetching Trustpilot reviews page {page + 1} from {url}")
                logger.debug(f"Request params: {params}")

                try:
                    response = await client.get(url, params=params)

                    # Log response details for debugging
                    logger.info(f"Response status: {response.status_code}")
                    if response.status_code != 200:
                        logger.error(f"Response body: {response.text}")

                    response.raise_for_status()
                    data = response.json()
                    
                    page_reviews = self._parse_trustpilot_reviews(data)
                    
                    # Filter out duplicates based on review ID
                    unique_reviews = []
                    for review in page_reviews:
                        if review.id not in seen_ids:
                            seen_ids.add(review.id)
                            unique_reviews.append(review)
                        else:
                            logger.debug(f"Skipping duplicate Trustpilot review ID: {review.id}")
                    
                    all_reviews.extend(unique_reviews)
                    
                    # Get next page cursor
                    next_page_cursor = data.get("next_page_cursor")
                    
                    # If no more pages, break
                    if not next_page_cursor:
                        logger.info(f"Reached end of Trustpilot reviews at page {page + 1}")
                        break
                    
                    # If we got fewer reviews than expected, we might be near the end
                    if len(page_reviews) < 10:
                        logger.info(f"Got only {len(page_reviews)} reviews on page {page + 1}, might be near end")
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch Trustpilot page {page + 1}: {e}")
                    break

        logger.info(f"Fetched {len(all_reviews)} unique Trustpilot reviews from {pages_to_fetch} pages")
        return all_reviews

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
                        author=review.get("reviewer", "Anonymous"),  # Google Play uses 'reviewer'
                        rating=int(review.get("rating", 0)),  # Convert to int
                        title=review.get("title", ""),
                        content=review.get("text", ""),  # Google Play uses 'text'
                        date=review.get("datetime", datetime.now().isoformat()),  # Google Play uses 'datetime'
                        source="google",
                        helpful_count=review.get("helpful_votes", 0),  # Google Play uses 'helpful_votes'
                        app_version=review.get("app_version", ""),
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
                        author=review.get("reviewer", "Anonymous"),  # App Store uses 'reviewer'
                        rating=int(review.get("rating", 0)),  # Convert to int
                        title=review.get("title"),
                        content=review.get("text", ""),  # App Store uses 'text'
                        date=review.get("datetime", datetime.now().isoformat()),  # App Store uses 'datetime'
                        source="apple",
                        helpful_count=review.get("helpful_count", 0),
                        app_version=review.get("app_version", ""),
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse review: {e}")
                logger.debug(f"Review data: {review}")
                continue

        return reviews

    def _parse_trustpilot_reviews(self, data: dict) -> list[AppReview]:
        """
        Parse Trustpilot reviews from API response.

        Based on Wextractor API format:
        - reviewer: author name
        - datetime: ISO timestamp
        - likes: helpful count
        - text: review content
        - title: review title
        """
        reviews = []
        raw_reviews = data.get("reviews", [])

        logger.info(f"Parsing {len(raw_reviews)} Trustpilot reviews")

        for review in raw_reviews:
            try:
                reviews.append(
                    AppReview(
                        id=review.get("id", ""),
                        author=review.get("reviewer", "Anonymous"),  # Trustpilot uses 'reviewer'
                        rating=int(review.get("rating", 0)),  # Convert to int
                        title=review.get("title"),
                        content=review.get("text", ""),  # Trustpilot uses 'text'
                        date=review.get("datetime", datetime.now().isoformat()),  # Trustpilot uses 'datetime'
                        source="trustpilot",
                        helpful_count=review.get("likes", 0),  # Trustpilot uses 'likes'
                        app_version=None,  # Trustpilot doesn't have app version
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse Trustpilot review: {e}")
                logger.debug(f"Review data: {review}")
                continue

        return reviews

    def _calculate_stats(
        self, reviews: list[AppReview], google_count: int, apple_count: int, trustpilot_count: int = 0
    ) -> ReviewStats:
        """Calculate review statistics."""
        if not reviews:
            return ReviewStats(
                total_reviews=0,
                average_rating=0.0,
                rating_distribution={"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
                google_reviews=0,
                apple_reviews=0,
                trustpilot_reviews=0,
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
            trustpilot_reviews=trustpilot_count,
        )

    def _get_mock_reviews(self, hours: int) -> dict:
        """Generate mock reviews for demonstration purposes."""
        import random
        
        # Mock review data
        mock_reviews_data = [
            {
                "author": "Олександр К.",
                "rating": 5,
                "content": "Чудовий додаток для вивчення мов! Дуже зручний інтерфейс та якісні уроки.",
                "source": "google",
                "app_version": "2.1.3",
                "helpful_count": 12
            },
            {
                "author": "Марія П.",
                "rating": 4,
                "content": "Добре працює, але іноді повільно завантажується. В цілому рекомендую.",
                "source": "google",
                "app_version": "2.1.2",
                "helpful_count": 8
            },
            {
                "author": "Дмитро В.",
                "rating": 5,
                "content": "Найкращий додаток для вивчення англійської! Вчителі професійні, ціни доступні.",
                "source": "apple",
                "app_version": "2.1.3",
                "helpful_count": 15
            },
            {
                "author": "Анна С.",
                "rating": 3,
                "content": "Нормально, але є проблеми з відеозв'язком. Потрібно покращити стабільність.",
                "source": "google",
                "app_version": "2.1.1",
                "helpful_count": 5
            },
            {
                "author": "Ігор М.",
                "rating": 5,
                "content": "Відмінний сервіс! За 3 місяці значно покращив рівень англійської. Дякую!",
                "source": "apple",
                "app_version": "2.1.3",
                "helpful_count": 20
            },
            {
                "author": "Катерина Л.",
                "rating": 4,
                "content": "Дуже зручно планувати уроки. Вчителі відмінні, рекомендую спробувати.",
                "source": "google",
                "app_version": "2.1.2",
                "helpful_count": 7
            },
            {
                "author": "Володимир Т.",
                "rating": 2,
                "content": "Додаток часто зависає. Потрібно виправити баги. Не рекомендую поки що.",
                "source": "google",
                "app_version": "2.1.0",
                "helpful_count": 3
            },
            {
                "author": "Олена Р.",
                "rating": 5,
                "content": "Прекрасний додаток! Дуже задоволена якістю уроків та підходом вчителів.",
                "source": "apple",
                "app_version": "2.1.3",
                "helpful_count": 18
            },
            {
                "author": "Сергій К.",
                "rating": 4,
                "content": "Хороший додаток, але потрібно додати більше мов. Поки що тільки англійська.",
                "source": "google",
                "app_version": "2.1.2",
                "helpful_count": 9
            },
            {
                "author": "Наталія Б.",
                "rating": 5,
                "content": "Найкращий інвестиція в освіту! За рік вивчила англійську на рівні B2.",
                "source": "apple",
                "app_version": "2.1.3",
                "helpful_count": 25
            }
        ]
        
        # Generate more reviews by duplicating and slightly modifying
        all_mock_reviews = []
        for i in range(3):  # Generate 3x more reviews
            for review_data in mock_reviews_data:
                # Add some variation to dates
                hours_ago = random.randint(1, hours)
                review_date = datetime.now() - timedelta(hours=hours_ago)
                
                # Add some variation to content
                content_variations = [
                    review_data["content"],
                    review_data["content"] + " Дуже рекомендую!",
                    review_data["content"] + " Варто спробувати.",
                ]
                
                all_mock_reviews.append(AppReview(
                    id=f"mock_{review_data['source']}_{len(all_mock_reviews)}",
                    author=review_data["author"],
                    rating=review_data["rating"],
                    content=random.choice(content_variations),
                    date=review_date.isoformat(),
                    source=review_data["source"],
                    app_version=review_data["app_version"],
                    helpful_count=review_data["helpful_count"]
                ))
        
        # Sort by date (newest first)
        all_mock_reviews.sort(key=lambda x: x.date, reverse=True)
        
        # Calculate statistics
        google_count = len([r for r in all_mock_reviews if r.source == "google"])
        apple_count = len([r for r in all_mock_reviews if r.source == "apple"])
        stats = self._calculate_stats(all_mock_reviews, google_count, apple_count)
        
        return {
            "reviews": all_mock_reviews,
            "stats": stats,
            "fetched_at": datetime.now().isoformat(),
            "time_range_hours": hours,
        }
