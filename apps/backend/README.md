# Reputation Horizon Backend

FastAPI backend service with LangGraph for AI-powered interactions.

## Features

- 🚀 **FastAPI**: Modern, fast web framework for building APIs
- 🤖 **LangGraph**: Stateful AI agent with conversational capabilities
- 📦 **uv**: Fast Python package manager
- 🔧 **Multiple LLM Providers**: Support for OpenAI and Anthropic
- ⚙️ **Best Practices**: Clean architecture, type hints, async/await

## Architecture

```
src/
├── main.py           # FastAPI application entry point
├── config.py         # Configuration and settings
├── models.py         # Pydantic models for validation
├── graph.py          # LangGraph agent implementation
└── routers/
    └── chat.py       # Chat API endpoints
```

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

Install uv if you haven't:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

1. **Install dependencies:**
   ```bash
   cd apps/backend
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env and add your API keys
   ```

3. **Set your LLM API key:**
   
   For OpenAI:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```
   
   For Anthropic:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   export LLM_PROVIDER="anthropic"
   export LLM_MODEL="claude-3-5-sonnet-20241022"
   ```

## Running the Server

### Development mode with auto-reload:
```bash
uv run uvicorn src.main:app --reload --port 8000
```

### Production mode:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Chat with AI Agent
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! What can you help me with?"
  }'
```

## LangGraph Architecture

The agent uses a simple but extensible graph structure:

1. **State Management**: Conversation history is maintained in the graph state
2. **LLM Node**: Processes messages and generates responses
3. **System Prompt**: Configurable context for the AI assistant
4. **Async Operations**: Full async support for high performance

### Extending the Agent

You can easily extend the graph in `src/graph.py`:

- Add tool/function calling nodes
- Implement multi-step reasoning
- Add memory/retrieval nodes
- Include conditional routing logic

Example with tools:
```python
from langgraph.prebuilt import ToolNode

# Define your tools
tools = [your_tool_1, your_tool_2]

# Add tool node
workflow.add_node("tools", ToolNode(tools))

# Update routing logic
def should_continue(state):
    if needs_tools(state):
        return "tools"
    return END
```

## Configuration

All configuration is managed through environment variables (see `.env.example`):

- `PORT`: Server port (default: 8000)
- `LLM_PROVIDER`: Choose "openai" or "anthropic"
- `LLM_MODEL`: Model name (e.g., "gpt-4o-mini", "claude-3-5-sonnet-20241022")
- `LLM_TEMPERATURE`: Response randomness (0.0 to 1.0)

## Development

### Code formatting and linting:
```bash
uv run ruff check .
uv run ruff format .
```

### Run tests:
```bash
uv run pytest
```

## Production Deployment

For production, consider:

1. Use environment-specific `.env` files
2. Configure CORS properly in `main.py`
3. Add authentication/authorization
4. Implement conversation persistence (database)
5. Add rate limiting
6. Use a production ASGI server like Gunicorn with Uvicorn workers

Example production command:
```bash
uv run gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Troubleshooting

**Issue**: `OPENAI_API_KEY not set`
- Make sure your `.env` file exists (copy from `env.example`)
- Add your API key to the `.env` file
- Or export it as an environment variable

**Issue**: Package conflicts
```bash
uv lock --upgrade
uv sync
```

**Issue**: Module not found
```bash
# Make sure you're running from the backend directory
cd apps/backend
uv run uvicorn src.main:app --reload
```

## License

Part of the Reputation Horizon project.

