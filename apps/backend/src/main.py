"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.models import HealthResponse
from src.routers import chat, reviews, reputation


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    print(f"🚀 Starting Reputation Horizon Backend")
    print(f"   Environment: {settings.environment}")
    print(f"   LLM Provider: {settings.llm_provider}")
    print(f"   LLM Model: {settings.llm_model}")
    print(f"   Wextractor API: {'✓ Configured' if settings.wextractor_api_key else '✗ Not configured'}")

    yield

    # Shutdown
    print("👋 Shutting down Reputation Horizon Backend")


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
            "reputation_analysis": "/api/reputation/analyze",
            "reputation_summary": "/api/reputation/summary",
        },
    }
