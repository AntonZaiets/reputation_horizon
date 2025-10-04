# DuckDB Caching System

This document describes the DuckDB-based caching system implemented for review data in the Reputation Horizon backend.

## Overview

The caching system provides:
- **Fast data retrieval** for frequently requested review data
- **Automatic cache expiration** with configurable TTL
- **Cache invalidation** and cleanup mechanisms
- **Cache statistics** and monitoring
- **DRY principles** with reusable service architecture

## Architecture

### Components

1. **CacheService** (`src/services/cache.py`)
   - Manages DuckDB database operations
   - Handles cache storage and retrieval
   - Provides cache statistics and cleanup

2. **ReviewService** (`src/services/review_service.py`)
   - Orchestrates between Wextractor API and cache
   - Implements caching logic and fallback strategies
   - Provides unified interface for review data

3. **Reviews Router** (`src/routers/reviews.py`)
   - Exposes caching parameters via API
   - Provides cache management endpoints

### Database Schema

#### `reviews` Table
```sql
CREATE TABLE reviews (
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
```

#### `cache_metadata` Table
```sql
CREATE TABLE cache_metadata (
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
```

## Usage

### API Endpoints

#### Get Reviews with Caching
```http
GET /api/reviews?hours=24&cached=true&force_refresh=false
```

**Parameters:**
- `hours`: Time range (1-168 hours)
- `cached`: Use cache if available (default: true)
- `force_refresh`: Force refresh even if cache exists (default: false)

#### Get Platform-Specific Reviews
```http
GET /api/reviews/google?hours=24&cached=true
GET /api/reviews/apple?hours=24&cached=true
```

#### Cache Management
```http
GET /api/reviews/cache/stats          # Get cache statistics
DELETE /api/reviews/cache             # Clear all cache
DELETE /api/reviews/cache?cache_key=reviews_24h  # Clear specific cache
POST /api/reviews/cache/cleanup      # Clean up expired entries
```

### Response Format

All review responses include a `cached` field indicating data source:

```json
{
  "reviews": [...],
  "stats": {...},
  "fetched_at": "2024-01-01T12:00:00",
  "time_range_hours": 24,
  "cached": true
}
```

## Configuration

### Cache Settings

Default configuration in `ReviewService`:
- **Cache Duration**: 24 hours
- **Max Cache Age**: 24 hours
- **Database Path**: `data/reviews_cache.db`

### Environment Variables

No additional environment variables required. Cache uses local DuckDB file.

## Cache Key Strategy

Cache keys are generated based on:
- Time range (`hours`)
- Source filter (`google`/`apple`)

**Examples:**
- `reviews_24h` - All reviews for 24 hours
- `reviews_24h_google` - Google reviews for 24 hours
- `reviews_48h_apple` - Apple reviews for 48 hours

## Performance Benefits

### Before Caching
- Every request hits Wextractor API
- Response time: 2-5 seconds
- API rate limits apply
- External dependency risk

### After Caching
- First request: 2-5 seconds (API + cache)
- Subsequent requests: <100ms (cache only)
- Reduced API calls
- Improved reliability

## Best Practices

### 1. Cache-First Strategy
```python
# Always try cache first
if cached and not force_refresh:
    cached_data = cache_service.get_cached_reviews(hours)
    if cached_data:
        return cached_data

# Fallback to API
fresh_data = await wextractor_service.get_reviews(hours)
cache_service.cache_reviews(fresh_data)
return fresh_data
```

### 2. Graceful Degradation
```python
# Cache failures don't break the API
try:
    cache_service.cache_reviews(response)
except Exception as e:
    logger.warning(f"Cache failed: {e}")
    # Continue without caching
```

### 3. Automatic Cleanup
```python
# Clean up expired entries on startup
cache_service._cleanup_expired_cache()
```

## Monitoring

### Cache Statistics
```json
{
  "cache_stats": {
    "cache_entries": 5,
    "total_reviews": 150,
    "oldest_cache": "2024-01-01T10:00:00",
    "newest_cache": "2024-01-01T12:00:00",
    "valid_caches": 3
  }
}
```

### Health Checks
- Monitor cache hit rates
- Track cache size growth
- Alert on cache failures

## Error Handling

### Cache Errors
- Database connection failures
- Disk space issues
- Corrupted cache data

### Fallback Strategy
1. Try cache retrieval
2. If cache fails, log warning
3. Fetch fresh data from API
4. Attempt to cache new data
5. Return data regardless of cache status

## Development

### Testing Cache
```bash
# First request (cache miss)
curl "http://localhost:8000/api/reviews?hours=24"

# Second request (cache hit)
curl "http://localhost:8000/api/reviews?hours=24"

# Force refresh
curl "http://localhost:8000/api/reviews?hours=24&force_refresh=true"
```

### Cache Debugging
```bash
# Check cache stats
curl "http://localhost:8000/api/reviews/cache/stats"

# Clear cache
curl -X DELETE "http://localhost:8000/api/reviews/cache"
```

## Future Enhancements

### Planned Features
1. **Redis Integration** - Distributed caching
2. **Cache Warming** - Pre-populate cache
3. **Smart Invalidation** - Event-driven cache updates
4. **Compression** - Reduce storage footprint
5. **Analytics** - Detailed cache performance metrics

### Configuration Options
1. **TTL per endpoint** - Different cache durations
2. **Cache size limits** - Prevent disk overflow
3. **Background refresh** - Update cache before expiration
4. **Cache partitioning** - Separate caches by app/platform

## Troubleshooting

### Common Issues

#### Cache Not Working
1. Check database file permissions
2. Verify data directory exists
3. Review cache statistics endpoint

#### Performance Issues
1. Monitor cache hit rates
2. Check database file size
3. Review cleanup frequency

#### Data Inconsistency
1. Clear cache and refresh
2. Check cache expiration settings
3. Verify API data freshness

### Debug Commands
```bash
# Check cache file
ls -la data/reviews_cache.db

# View cache stats
curl "http://localhost:8000/api/reviews/cache/stats"

# Clear all cache
curl -X DELETE "http://localhost:8000/api/reviews/cache"
```
