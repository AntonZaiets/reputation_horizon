from app_store_scraper import AppStore
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AppStoreService:
    """Service for fetching reviews from Apple App Store"""
    
    # Preply app info на App Store
    APP_NAME = "preply"
    APP_ID = "1400521332"
    
    def __init__(self):
        self.app_name = self.APP_NAME
        self.app_id = self.APP_ID
        
    async def get_reviews(
        self,
        time_threshold: datetime,
        country: str = "us",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Отримати відгуки з App Store
        
        Args:
            time_threshold: Мінімальна дата відгуку
            country: Код країни (us, ua, gb тощо)
            limit: Максимальна кількість відгуків
            
        Returns:
            List of review dictionaries
        """
        try:
            logger.info(f"Fetching App Store reviews for {self.app_name}, country: {country}")
            
            # Створюємо об'єкт AppStore
            app = AppStore(
                country=country.lower(),
                app_name=self.app_name,
                app_id=self.app_id
            )
            
            # Отримуємо відгуки
            app.review(how_many=limit)
            
            # Фільтруємо відгуки за часом
            filtered_reviews = []
            for review in app.reviews:
                review_date = review.get('date')
                
                # Конвертуємо дату якщо потрібно
                if isinstance(review_date, datetime):
                    if review_date >= time_threshold:
                        filtered_reviews.append(self._format_review(review))
                elif isinstance(review_date, str):
                    try:
                        parsed_date = datetime.fromisoformat(review_date.replace('Z', '+00:00'))
                        if parsed_date >= time_threshold:
                            filtered_reviews.append(self._format_review(review))
                    except:
                        # Якщо не можемо розпарсити дату, додаємо відгук
                        filtered_reviews.append(self._format_review(review))
            
            logger.info(f"Found {len(filtered_reviews)} App Store reviews from last period")
            return filtered_reviews
            
        except Exception as e:
            logger.error(f"Error fetching App Store reviews: {str(e)}")
            # Повертаємо порожній список замість помилки
            return []
    
    def _format_review(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """Format review to standard structure"""
        review_date = review.get('date')
        
        # Форматуємо дату
        if isinstance(review_date, datetime):
            date_str = review_date.isoformat()
        elif isinstance(review_date, str):
            date_str = review_date
        else:
            date_str = datetime.now().isoformat()
        
        return {
            "id": review.get('reviewId', '') or review.get('review_id', ''),
            "userName": review.get('userName', 'Anonymous') or review.get('review', {}).get('author', {}).get('name', 'Anonymous'),
            "rating": review.get('rating', 0),
            "text": review.get('review', '') or review.get('title', ''),
            "date": date_str,
            "source": "apple",
            "version": review.get('version'),
            "thumbsUp": None  # App Store не має thumbsUp
        }

