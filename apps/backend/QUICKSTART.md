# Quick Start Guide

Get up and running with the Reputation Horizon backend in 5 minutes!

## Step 1: Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 2: Navigate to backend directory

```bash
cd apps/backend
```

## Step 3: Install dependencies

```bash
uv sync
```

This will create a virtual environment and install all dependencies.

## Step 4: Set up environment variables

```bash
cp env.example .env
```

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

Or if using Anthropic Claude:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
```

## Step 5: Run the server

### Option A: Using the run script
```bash
./run.sh
```

### Option B: Using uvicorn directly
```bash
uv run uvicorn src.main:app --reload --port 8000
```

## Step 6: Test it out!

Open your browser to:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

Or test with curl:
```bash
# Health check
curl http://localhost:8000/api/health

# Chat with the AI
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Tell me a joke."}'
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API documentation](http://localhost:8000/docs) in your browser
- Customize the agent in `src/graph.py`
- Add new endpoints in `src/routers/`

## Architecture Overview

```
src/
├── main.py          # FastAPI app & startup
├── config.py        # Settings & environment vars
├── models.py        # Request/response models
├── graph.py         # LangGraph agent logic ⭐
└── routers/
    └── chat.py      # Chat API endpoints
```

The core AI logic is in `src/graph.py` - start there to customize the agent!

## Common Issues

**Error: "OPENAI_API_KEY not set"**
→ Make sure you created a `.env` file and added your API key

**Error: "command not found: uv"**
→ Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Error: "Address already in use"**
→ Change the port in `.env` or kill the process using port 8000

Happy coding! 🚀

