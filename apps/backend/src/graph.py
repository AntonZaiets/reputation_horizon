"""LangGraph agent implementation with best practices."""

from typing import Annotated, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from src.config import settings


class AgentState(TypedDict):
    """State definition for the agent graph."""

    messages: Annotated[list[BaseMessage], add_messages]


def get_llm():
    """Get the configured LLM instance."""
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        return ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key,
        )
    elif settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        return ChatAnthropic(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.anthropic_api_key,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")


# Initialize LLM
llm = get_llm()


# System prompt for the agent
SYSTEM_PROMPT = """You are a helpful AI assistant for Reputation Horizon. 
You help users with their questions in a friendly and professional manner.
Always be concise, accurate, and helpful."""


async def call_model(state: AgentState) -> AgentState:
    """
    Call the LLM model with the current state.

    This node invokes the LLM with the conversation history.
    """
    messages = state["messages"]

    # Add system prompt if not present
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # Call the LLM
    response = await llm.ainvoke(messages)

    # Return updated state
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """
    Determine if the conversation should continue.

    In this simple implementation, we always end after one response.
    You can extend this to add multi-turn reasoning, tool calls, etc.
    """
    return END


# Build the graph
def create_agent_graph() -> StateGraph:
    """Create and compile the agent graph."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges("agent", should_continue)

    # Compile the graph
    return workflow.compile()


# Global graph instance
agent_graph = create_agent_graph()


async def run_agent(message: str, conversation_history: list[BaseMessage] | None = None) -> str:
    """
    Run the agent with a user message.

    Args:
        message: User's input message
        conversation_history: Optional previous messages in the conversation

    Returns:
        The agent's response as a string
    """
    # Prepare initial state
    messages = conversation_history or []
    messages.append(HumanMessage(content=message))

    initial_state = AgentState(messages=messages)

    # Run the graph
    result = await agent_graph.ainvoke(initial_state)

    # Extract the last message (agent's response)
    final_messages = result["messages"]
    if final_messages:
        return final_messages[-1].content

    return "I apologize, but I couldn't generate a response. Please try again."

