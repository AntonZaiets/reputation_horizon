from datetime import datetime
from typing import Dict, Any, List
import logging

from services.google_play_service import GooglePlayService
from services.app_store_service import AppStoreService

logger = logging.getLogger(__name__)


class ReviewAggregator:
    """Aggregates reviews from multiple sources"""
    
    def __init__(
        self,
        google_play_service: GooglePlayService,
        app_store_service: AppStoreService
    ):
        self.google_play_service = google_play_service
        self.app_store_service = app_store_service
    
    async def get_all_reviews(
        self,
        time_threshold: datetime,
        country: str = "us",
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Отримати відгуки з обох джерел та об'єднати їх
        
        Returns:
            Dictionary with reviews and stats
        """
        # Отримуємо відгуки з обох джерел паралельно
        google_reviews = await self.google_play_service.get_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        apple_reviews = await self.app_store_service.get_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        # Об'єднуємо відгуки
        all_reviews = google_reviews + apple_reviews
        
        # Сортуємо за датою (новіші спочатку)
        all_reviews.sort(
            key=lambda x: x['date'],
            reverse=True
        )
        
        # Обчислюємо статистику
        stats = self._calculate_stats(all_reviews, google_reviews, apple_reviews)
        
        return {
            "reviews": all_reviews,
            "stats": stats
        }
    
    async def get_google_reviews(
        self,
        time_threshold: datetime,
        country: str = "us",
        limit: int = 100
    ) -> Dict[str, Any]:
        """Отримати тільки Google Play відгуки"""
        reviews = await self.google_play_service.get_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        stats = self._calculate_stats(reviews, reviews, [])
        
        return {
            "reviews": reviews,
            "stats": stats
        }
    
    async def get_apple_reviews(
        self,
        time_threshold: datetime,
        country: str = "us",
        limit: int = 100
    ) -> Dict[str, Any]:
        """Отримати тільки App Store відгуки"""
        reviews = await self.app_store_service.get_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        stats = self._calculate_stats(reviews, [], reviews)
        
        return {
            "reviews": reviews,
            "stats": stats
        }
    
    def _calculate_stats(
        self,
        all_reviews: List[Dict[str, Any]],
        google_reviews: List[Dict[str, Any]],
        apple_reviews: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Обчислити статистику по відгуках"""
        if not all_reviews:
            return {
                "totalReviews": 0,
                "avgRating": 0.0,
                "googlePlayReviews": 0,
                "appStoreReviews": 0,
                "positiveReviews": 0,
                "negativeReviews": 0
            }
        
        # Загальна кількість
        total_reviews = len(all_reviews)
        
        # Середній рейтинг
        total_rating = sum(review['rating'] for review in all_reviews)
        avg_rating = round(total_rating / total_reviews, 1) if total_reviews > 0 else 0.0
        
        # Кількість по джерелах
        google_count = len(google_reviews)
        apple_count = len(apple_reviews)
        
        # Позитивні (4-5 зірок) та негативні (1-2 зірки)
        positive_reviews = sum(1 for review in all_reviews if review['rating'] >= 4)
        negative_reviews = sum(1 for review in all_reviews if review['rating'] <= 2)
        
        return {
            "totalReviews": total_reviews,
            "avgRating": avg_rating,
            "googlePlayReviews": google_count,
            "appStoreReviews": apple_count,
            "positiveReviews": positive_reviews,
            "negativeReviews": negative_reviews
        }

