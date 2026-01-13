"""
State schema for the LangGraph agent.
"""

from typing import TypedDict, Annotated, Sequence, Optional, Dict, Any
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    State schema for the agent workflow.
    
    Attributes:
        messages: Conversation history
        task: Current task description
        task_type: Type of task (code_review, error_analysis, repo_query, etc.)
        augment_result: Result from Augment SDK
        analysis: Analysis of the Augment result
        final_output: Final formatted output
        session_id: Augment SDK session ID for continuity
        metadata: Additional metadata
    """
    # Messages are accumulated using operator.add
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # Task information
    task: str
    task_type: Optional[str]
    
    # Results from different nodes
    augment_result: Optional[str]
    analysis: Optional[str]
    final_output: Optional[str]
    
    # Session management
    session_id: Optional[str]
    
    # Additional context
    metadata: Optional[Dict[str, Any]]

