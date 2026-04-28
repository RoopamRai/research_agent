"""Defines the memory/state structure for the LangGraph agent."""

from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    The state dictionary passed linearly through the graph execution.
    
    Attributes:
        messages: A list of all conversation turns (HumanMessage, AIMessage, ToolMessage).
                  The `add_messages` annotation ensures we append to the list 
                  rather than replacing it at every step.
    """
    messages: Annotated[list[BaseMessage], add_messages]
