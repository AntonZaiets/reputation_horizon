from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional
import logging
from pydantic import BaseModel

from services.google_play_service import GooglePlayService
from services.app_store_service import AppStoreService
from services.review_aggregator import ReviewAggregator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Reputation Horizon API",
    description="API для моніторингу відгуків Preply з Google Play та App Store",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
google_play_service = GooglePlayService()
app_store_service = AppStoreService()
review_aggregator = ReviewAggregator(google_play_service, app_store_service)


class Review(BaseModel):
    id: str
    userName: str
    rating: int
    text: str
    date: str
    source: str
    version: Optional[str] = None
    thumbsUp: Optional[int] = None


class Stats(BaseModel):
    totalReviews: int
    avgRating: float
    googlePlayReviews: int
    appStoreReviews: int
    positiveReviews: int
    negativeReviews: int


class ReviewsResponse(BaseModel):
    reviews: List[Review]
    stats: Stats


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Reputation Horizon API",
        "version": "1.0.0",
        "endpoints": {
            "/api/reviews": "Get reviews from last 24 hours",
            "/api/reviews/google": "Get Google Play reviews only",
            "/api/reviews/apple": "Get App Store reviews only",
            "/docs": "API documentation"
        }
    }


@app.get("/api/reviews", response_model=ReviewsResponse)
async def get_reviews(
    hours: int = Query(24, description="Number of hours to look back", ge=1, le=168),
    country: str = Query("us", description="Country code (e.g., us, ua, gb)"),
    limit: int = Query(100, description="Maximum number of reviews per source", ge=1, le=500)
):
    """
    Отримати відгуки з обох магазинів за останні N годин
    
    - **hours**: кількість годин назад (за замовчуванням 24)
    - **country**: код країни (us, ua, gb, pl тощо)
    - **limit**: максимальна кількість відгуків з кожного джерела
    """
    try:
        logger.info(f"Fetching reviews for last {hours} hours, country: {country}")
        
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        result = await review_aggregator.get_all_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        logger.info(f"Successfully fetched {len(result['reviews'])} reviews")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching reviews: {str(e)}")


@app.get("/api/reviews/google", response_model=ReviewsResponse)
async def get_google_reviews(
    hours: int = Query(24, description="Number of hours to look back", ge=1, le=168),
    country: str = Query("us", description="Country code"),
    limit: int = Query(100, description="Maximum number of reviews", ge=1, le=500)
):
    """
    Отримати відгуки тільки з Google Play
    """
    try:
        logger.info(f"Fetching Google Play reviews for last {hours} hours")
        
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        result = await review_aggregator.get_google_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching Google Play reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching Google Play reviews: {str(e)}")


@app.get("/api/reviews/apple", response_model=ReviewsResponse)
async def get_apple_reviews(
    hours: int = Query(24, description="Number of hours to look back", ge=1, le=168),
    country: str = Query("us", description="Country code"),
    limit: int = Query(100, description="Maximum number of reviews", ge=1, le=500)
):
    """
    Отримати відгуки тільки з App Store
    """
    try:
        logger.info(f"Fetching App Store reviews for last {hours} hours")
        
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        result = await review_aggregator.get_apple_reviews(
            time_threshold=time_threshold,
            country=country,
            limit=limit
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching App Store reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching App Store reviews: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

