"""Chat API router."""

import uuid

from fastapi import APIRouter, HTTPException

from src.graph import run_agent
from src.models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the LLM agent.

    This endpoint processes a user message and returns the agent's response.
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Run the agent
        # Note: In a production app, you'd want to store and retrieve
        # conversation history from a database
        response = await run_agent(request.message)

        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

