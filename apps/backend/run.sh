#!/bin/bash
# Development server startup script

cd "$(dirname "$0")"

echo "🚀 Starting Reputation Horizon Backend..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from env.example..."
    cp env.example .env
    echo "✅ Created .env file. Please edit it with your API keys before running again."
    exit 1
fi

# Run the server
uv run uvicorn src.main:app --reload --port 8000

