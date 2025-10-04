# Backend Project Structure

## 📁 File Organization

```
apps/backend/
├── pyproject.toml          # Python dependencies (managed by uv)
├── env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── run.sh                  # Quick start script (executable)
│
├── README.md               # Full documentation
├── QUICKSTART.md           # 5-minute getting started guide
├── STRUCTURE.md            # This file - project structure
│
└── src/                    # Source code
    ├── __init__.py         # Package marker
    ├── main.py             # FastAPI application entry point
    ├── config.py           # Settings & environment configuration
    ├── models.py           # Pydantic models (request/response)
    ├── graph.py            # LangGraph agent implementation
    │
    └── routers/            # API route handlers
        ├── __init__.py
        └── chat.py         # Chat endpoints
```

## 🎯 Key Files Explained

### `pyproject.toml`
- Defines project dependencies
- Uses `uv` for fast package management
- Includes FastAPI, LangGraph, and LLM provider packages

### `src/main.py`
- FastAPI application setup
- CORS middleware configuration
- Router registration
- Health check endpoint

### `src/config.py`
- Centralized configuration using `pydantic-settings`
- Loads environment variables from `.env` file
- Type-safe settings with validation

### `src/models.py`
- Pydantic models for API validation
- Request/response schemas
- Type hints for IDE support

### `src/graph.py` ⭐ **Most Important**
- LangGraph agent implementation
- State management for conversations
- LLM integration (OpenAI/Anthropic)
- Extensible graph structure

### `src/routers/chat.py`
- Chat API endpoints
- Request handling and validation
- Error handling

## 🔄 Request Flow

```
1. Client sends POST to /api/chat
   ↓
2. FastAPI routes to chat.router
   ↓
3. Pydantic validates ChatRequest
   ↓
4. run_agent() called with user message
   ↓
5. LangGraph processes through state graph
   ↓
6. LLM generates response
   ↓
7. Response wrapped in ChatResponse
   ↓
8. JSON returned to client
```

## 🧩 LangGraph Architecture

```
[User Input]
     ↓
[Create State]
     ↓
[Agent Node] → [Call LLM]
     ↓
[Should Continue?]
     ↓
   [END]
```

### State Definition
```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

### Graph Nodes
- **agent**: Calls the LLM with conversation history
- *(extensible)*: Add tool nodes, retrieval, multi-step reasoning

## 🚀 Development Workflow

### 1. Add New Endpoint
Create a new router in `src/routers/`:
```python
# src/routers/my_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/my-feature", tags=["my-feature"])

@router.get("/")
async def my_endpoint():
    return {"message": "Hello"}
```

Register in `src/main.py`:
```python
from src.routers import chat, my_feature

app.include_router(chat.router)
app.include_router(my_feature.router)
```

### 2. Extend LangGraph Agent
Add nodes to the graph in `src/graph.py`:
```python
# Add a tool node
from langgraph.prebuilt import ToolNode

tools = [my_tool_1, my_tool_2]
workflow.add_node("tools", ToolNode(tools))

# Update routing
def should_continue(state):
    if needs_tools(state):
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
```

### 3. Add Configuration
Update `src/config.py`:
```python
class Settings(BaseSettings):
    my_new_setting: str = "default_value"
```

Add to `env.example`:
```bash
MY_NEW_SETTING=some_value
```

## 📦 Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation

### AI/LLM
- `langgraph` - Stateful agent graphs
- `langchain` - LLM framework
- `langchain-openai` - OpenAI integration
- `langchain-anthropic` - Anthropic integration

### Development
- `pytest` - Testing
- `httpx` - HTTP client for tests
- `ruff` - Linting and formatting

## 🔧 Configuration Files

### `pyproject.toml`
- Project metadata
- Dependencies
- Build system
- Tool configurations (ruff)

### `.env` (create from env.example)
- API keys
- Server configuration
- LLM settings

### `.gitignore`
- Excludes virtual environments
- Ignores `.env` files
- Excludes Python cache files

## 🎨 Best Practices Implemented

1. **Type Hints**: All functions have type annotations
2. **Async/Await**: Full async support for performance
3. **Separation of Concerns**: Clear separation between API, logic, and config
4. **Validation**: Pydantic models validate all inputs/outputs
5. **Environment Config**: Centralized, type-safe configuration
6. **Error Handling**: Proper exception handling with HTTP status codes
7. **Documentation**: Docstrings and auto-generated API docs
8. **Extensibility**: Easy to add new endpoints, tools, and features

## 📚 Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Contributing

When adding features:
1. Keep the simple, clean architecture
2. Add type hints
3. Update documentation
4. Follow existing patterns
5. Test your changes

Start with `QUICKSTART.md` → `README.md` → `STRUCTURE.md` (you are here!) → dive into the code!

