"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.models import HealthResponse
from src.routers import chat, reviews, reputation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("🚀 Starting Reputation Horizon Backend")
    logger.info(f"   Environment: {settings.environment}")
    logger.info(f"   LLM Provider: {settings.llm_provider}")
    logger.info(f"   LLM Model: {settings.llm_model}")
    logger.info(f"   Wextractor API: {'✓ Configured' if settings.wextractor_api_key else '✗ Not configured'}")
    logger.info("   DuckDB Cache: ✓ Enabled (data/reviews_cache.db)")

    yield

    # Shutdown
    logger.info("👋 Shutting down Reputation Horizon Backend")


app = FastAPI(
    title="Reputation Horizon API",
    description="FastAPI backend with LangGraph for AI-powered interactions and app review monitoring",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(reviews.router)
app.include_router(reputation.router)


@app.get("/api/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        message="Backend is running",
        llm_provider=settings.llm_provider,
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Reputation Horizon API",
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "chat": "/api/chat",
            "reviews": "/api/reviews",
            "google_reviews": "/api/reviews/google",
            "apple_reviews": "/api/reviews/apple",
            "cache_stats": "/api/reviews/cache/stats",
            "clear_cache": "/api/reviews/cache",
            "reputation_analysis": "/api/reputation/analyze",
            "reputation_summary": "/api/reputation/summary",
        },
    }
