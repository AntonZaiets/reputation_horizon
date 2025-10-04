"""DuckDB-based caching service for review data."""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb

from src.models import AppReview, ReviewStats, ReviewsResponse

logger = logging.getLogger(__name__)


class CacheService:
    """Service for caching review data in DuckDB."""

    def __init__(self, db_path: str = "data/reviews_cache.db"):
        """Initialize the cache service with DuckDB."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database connection with error handling
        self.conn = None
        try:
            self.conn = duckdb.connect(str(self.db_path))
            self._create_tables()
            logger.info(f"DuckDB cache initialized at {self.db_path}")
        except Exception as e:
            logger.warning(f"Failed to initialize DuckDB cache: {e}. Cache will be disabled.")
            self.conn = None

    def _create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        create_reviews_table = """
        CREATE TABLE IF NOT EXISTS reviews (
            id VARCHAR PRIMARY KEY,
            author VARCHAR,
            rating INTEGER,
            title VARCHAR,
            content VARCHAR,
            date VARCHAR,
            source VARCHAR,
            helpful_count INTEGER,
            app_version VARCHAR,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        create_cache_metadata_table = """
        CREATE TABLE IF NOT EXISTS cache_metadata (
            cache_key VARCHAR PRIMARY KEY,
            hours INTEGER,
            google_count INTEGER,
            apple_count INTEGER,
            total_count INTEGER,
            avg_rating REAL,
            rating_distribution VARCHAR,
            fetched_at TIMESTAMP,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
        """
        
        self.conn.execute(create_reviews_table)
        self.conn.execute(create_cache_metadata_table)
        
        # Create indexes for better performance
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(date)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_reviews_source ON reviews(source)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache_metadata(expires_at)")

    def _generate_cache_key(self, hours: int, source_filter: Optional[str] = None) -> str:
        """Generate a cache key for the given parameters."""
        base_key = f"reviews_{hours}h"
        if source_filter:
            base_key += f"_{source_filter}"
        return base_key

    def _is_cache_valid(self, cache_key: str, max_age_hours: int = 1) -> bool:
        """Check if cached data is still valid."""
        query = """
        SELECT expires_at FROM cache_metadata 
        WHERE cache_key = ? AND expires_at > CURRENT_TIMESTAMP
        """
        result = self.conn.execute(query, [cache_key]).fetchone()
        
        if result:
            logger.debug(f"Cache hit for key: {cache_key}, expires at: {result[0]}")
            return True
        else:
            logger.debug(f"Cache miss for key: {cache_key} (expired or not found)")
            return False

    def _cleanup_expired_cache(self) -> None:
        """Remove expired cache entries."""
        if not self.conn:
            logger.debug("DuckDB cache not available, cannot cleanup cache")
            return
            
        try:
            cleanup_query = """
            DELETE FROM cache_metadata WHERE expires_at <= CURRENT_TIMESTAMP
            """
            self.conn.execute(cleanup_query)
            
            # Also clean up orphaned reviews (not referenced by any cache entry)
            orphan_cleanup = """
            DELETE FROM reviews 
            WHERE id NOT IN (
                SELECT DISTINCT r.id 
                FROM reviews r 
                JOIN cache_metadata c ON r.cached_at >= c.cached_at - INTERVAL '1 hour'
            )
            """
            self.conn.execute(orphan_cleanup)
            
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")

    def get_cached_reviews(
        self, 
        hours: int, 
        source_filter: Optional[str] = None,
        max_age_hours: int = 1
    ) -> Optional[ReviewsResponse]:
        """
        Retrieve cached reviews if available and valid.
        
        Args:
            hours: Number of hours to look back
            source_filter: Optional source filter ('google' or 'apple')
            max_age_hours: Maximum age of cached data in hours
            
        Returns:
            Cached ReviewsResponse or None if not available/valid
        """
        if not self.conn:
            logger.debug("DuckDB cache not available, skipping cache lookup")
            return None
            
        try:
            cache_key = self._generate_cache_key(hours, source_filter)
            logger.info(f"🔍 Looking up cache for key: {cache_key}")
            
            # Check if cache is valid
            if not self._is_cache_valid(cache_key, max_age_hours):
                logger.info(f"❌ Cache validation failed for key: {cache_key}")
                return None
            
            logger.info(f"✅ Cache validation passed for key: {cache_key}")

            # Get cache metadata
            metadata_query = """
            SELECT google_count, apple_count, total_count, avg_rating, 
                   rating_distribution, fetched_at
            FROM cache_metadata WHERE cache_key = ?
            """
            metadata = self.conn.execute(metadata_query, [cache_key]).fetchone()
            
            if not metadata:
                logger.info(f"❌ No metadata found for cache key: {cache_key}")
                return None

            logger.info(f"📊 Found metadata for cache key: {cache_key}")

            # Get reviews
            reviews_query = """
            SELECT id, author, rating, title, content, date, source, 
                   helpful_count, app_version
            FROM reviews 
            WHERE cached_at >= (
                SELECT cached_at FROM cache_metadata WHERE cache_key = ?
            )
            """
            
            if source_filter:
                reviews_query += f" AND source = '{source_filter}'"
            
            reviews_query += " ORDER BY date DESC"
            
            reviews_data = self.conn.execute(reviews_query, [cache_key]).fetchall()
            
            if not reviews_data:
                logger.info(f"❌ No reviews found for cache key: {cache_key}")
                return None
            
            logger.info(f"📝 Found {len(reviews_data)} reviews for cache key: {cache_key}")

            # Convert to AppReview objects
            reviews = []
            for row in reviews_data:
                reviews.append(AppReview(
                    id=row[0],
                    author=row[1],
                    rating=row[2],
                    title=row[3],
                    content=row[4],
                    date=row[5],
                    source=row[6],
                    helpful_count=row[7],
                    app_version=row[8]
                ))

            # Create stats
            stats = ReviewStats(
                total_reviews=metadata[2],
                average_rating=metadata[3],
                rating_distribution=json.loads(metadata[4]),
                google_reviews=metadata[0],
                apple_reviews=metadata[1]
            )

            logger.info(f"Cache hit for key: {cache_key}, {len(reviews)} reviews")
            
            response = ReviewsResponse(
                reviews=reviews,
                stats=stats,
                fetched_at=metadata[5].isoformat(),
                time_range_hours=hours,
                cached=True
            )
            
            logger.debug(f"Returning cached response with {len(response.reviews)} reviews")
            return response

        except Exception as e:
            logger.error(f"Error retrieving cached reviews: {e}")
            return None

    def cache_reviews(
        self, 
        reviews_response: ReviewsResponse, 
        hours: int,
        source_filter: Optional[str] = None,
        cache_duration_hours: int = 1
    ) -> None:
        """
        Cache reviews data.
        
        Args:
            reviews_response: ReviewsResponse to cache
            hours: Number of hours the data represents
            source_filter: Optional source filter
            cache_duration_hours: How long to keep the cache
        """
        if not self.conn:
            logger.debug("DuckDB cache not available, skipping cache storage")
            return
            
        try:
            cache_key = self._generate_cache_key(hours, source_filter)
            expires_at = datetime.now() + timedelta(hours=cache_duration_hours)
            
            logger.debug(f"Caching {len(reviews_response.reviews)} reviews with key: {cache_key}, expires at: {expires_at}")
            
            # Start transaction
            self.conn.begin()
            
            try:
                # Clear existing cache for this key
                self.conn.execute("DELETE FROM cache_metadata WHERE cache_key = ?", [cache_key])
                
                # Insert cache metadata
                metadata_query = """
                INSERT INTO cache_metadata 
                (cache_key, hours, google_count, apple_count, total_count, 
                 avg_rating, rating_distribution, fetched_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                self.conn.execute(metadata_query, [
                    cache_key,
                    hours,
                    reviews_response.stats.google_reviews,
                    reviews_response.stats.apple_reviews,
                    reviews_response.stats.total_reviews,
                    reviews_response.stats.average_rating,
                    json.dumps(reviews_response.stats.rating_distribution),
                    datetime.fromisoformat(reviews_response.fetched_at),
                    expires_at
                ])
                
                # Insert reviews
                reviews_query = """
                INSERT OR REPLACE INTO reviews 
                (id, author, rating, title, content, date, source, helpful_count, app_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                for review in reviews_response.reviews:
                    self.conn.execute(reviews_query, [
                        review.id,
                        review.author,
                        review.rating,
                        review.title,
                        review.content,
                        review.date,
                        review.source,
                        review.helpful_count,
                        review.app_version
                    ])
                
                # Commit transaction
                self.conn.commit()
                
                logger.info(f"Cached {len(reviews_response.reviews)} reviews for key: {cache_key}")
                
            except Exception as e:
                self.conn.rollback()
                raise e
                
        except Exception as e:
            logger.error(f"Error caching reviews: {e}")
            raise e

    def debug_cache_contents(self) -> None:
        """Debug method to show what's in the cache."""
        if not self.conn:
            logger.debug("DuckDB cache not available")
            return
            
        try:
            query = """
            SELECT cache_key, expires_at, total_count, cached_at 
            FROM cache_metadata 
            ORDER BY cached_at DESC
            """
            results = self.conn.execute(query).fetchall()
            
            logger.debug("=== CACHE CONTENTS ===")
            for row in results:
                logger.debug(f"Key: {row[0]}, Expires: {row[1]}, Count: {row[2]}, Cached: {row[3]}")
            logger.debug("======================")
            
        except Exception as e:
            logger.error(f"Error debugging cache contents: {e}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self.conn:
            logger.debug("DuckDB cache not available, returning empty stats")
            return {}
            
        try:
            stats_query = """
            SELECT 
                COUNT(DISTINCT cache_key) as cache_entries,
                COUNT(*) as total_reviews,
                MIN(cached_at) as oldest_cache,
                MAX(cached_at) as newest_cache,
                COUNT(CASE WHEN expires_at > CURRENT_TIMESTAMP THEN 1 END) as valid_caches
            FROM cache_metadata
            """
            
            result = self.conn.execute(stats_query).fetchone()
            
            return {
                "cache_entries": result[0],
                "total_reviews": result[1],
                "oldest_cache": result[2].isoformat() if result[2] else None,
                "newest_cache": result[3].isoformat() if result[3] else None,
                "valid_caches": result[4]
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}

    def clear_cache(self, cache_key: Optional[str] = None) -> None:
        """Clear cache entries."""
        if not self.conn:
            logger.debug("DuckDB cache not available, cannot clear cache")
            return
            
        try:
            if cache_key:
                self.conn.execute("DELETE FROM cache_metadata WHERE cache_key = ?", [cache_key])
                logger.info(f"Cleared cache for key: {cache_key}")
            else:
                self.conn.execute("DELETE FROM cache_metadata")
                self.conn.execute("DELETE FROM reviews")
                logger.info("Cleared all cache")
                
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            try:
                self.conn.close()
                logger.info("DuckDB cache connection closed")
            except Exception as e:
                logger.warning(f"Error closing DuckDB connection: {e}")
            finally:
                self.conn = None

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.close()
        except Exception:
            pass  # Ignore errors during cleanup
