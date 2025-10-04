#!/bin/bash
# Setup script for Reputation Horizon Backend

set -e

echo "🎯 Setting up Reputation Horizon Backend"
echo "========================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo ""
    echo "Install it with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

echo "✅ uv is installed"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing dependencies with uv..."
uv sync
echo "✅ Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API key!"
    echo ""
    echo "For OpenAI:"
    echo "  OPENAI_API_KEY=sk-your-key-here"
    echo ""
    echo "For Anthropic Claude:"
    echo "  ANTHROPIC_API_KEY=sk-ant-your-key-here"
    echo "  LLM_PROVIDER=anthropic"
    echo "  LLM_MODEL=claude-3-5-sonnet-20241022"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Make run.sh executable
chmod +x run.sh

echo "========================================"
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API key"
echo "  2. Run: ./run.sh"
echo "  3. Visit: http://localhost:8000/docs"
echo ""
echo "Or read QUICKSTART.md for more details"
echo "========================================"

