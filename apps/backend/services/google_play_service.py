from google_play_scraper import app as gp_app
from google_play_scraper import Sort, reviews as gp_reviews
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GooglePlayService:
    """Service for fetching reviews from Google Play Store"""
    
    # Preply app ID на Google Play
    APP_ID = "com.preply.android"
    
    def __init__(self):
        self.app_id = self.APP_ID
        
    async def get_reviews(
        self, 
        time_threshold: datetime,
        country: str = "us",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Отримати відгуки з Google Play
        
        Args:
            time_threshold: Мінімальна дата відгуку
            country: Код країни (us, ua, gb тощо)
            limit: Максимальна кількість відгуків
            
        Returns:
            List of review dictionaries
        """
        try:
            logger.info(f"Fetching Google Play reviews for {self.app_id}, country: {country}")
            
            # Отримуємо відгуки, відсортовані за новизною
            result, _ = gp_reviews(
                self.app_id,
                lang='en',
                country=country.lower(),
                sort=Sort.NEWEST,
                count=limit
            )
            
            # Фільтруємо відгуки за часом
            filtered_reviews = []
            for review in result:
                review_date = review['at']
                
                # Якщо review_date вже datetime, порівнюємо напряму
                if isinstance(review_date, datetime):
                    if review_date >= time_threshold:
                        filtered_reviews.append(self._format_review(review))
                    else:
                        # Оскільки відгуки відсортовані за новизною, можемо зупинитися
                        break
            
            logger.info(f"Found {len(filtered_reviews)} Google Play reviews from last period")
            return filtered_reviews
            
        except Exception as e:
            logger.error(f"Error fetching Google Play reviews: {str(e)}")
            # Повертаємо порожній список замість помилки
            return []
    
    def _format_review(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """Format review to standard structure"""
        return {
            "id": review.get('reviewId', ''),
            "userName": review.get('userName', 'Anonymous'),
            "rating": review.get('score', 0),
            "text": review.get('content', ''),
            "date": review.get('at').isoformat() if isinstance(review.get('at'), datetime) else str(review.get('at')),
            "source": "google",
            "version": review.get('reviewCreatedVersion'),
            "thumbsUp": review.get('thumbsUpCount', 0)
        }
    
    async def get_app_info(self, country: str = "us") -> Dict[str, Any]:
        """Get app information from Google Play"""
        try:
            result = gp_app(
                self.app_id,
                lang='en',
                country=country.lower()
            )
            return {
                "title": result.get('title'),
                "score": result.get('score'),
                "ratings": result.get('ratings'),
                "reviews": result.get('reviews'),
                "installs": result.get('installs'),
                "version": result.get('version')
            }
        except Exception as e:
            logger.error(f"Error fetching app info: {str(e)}")
            return {}

