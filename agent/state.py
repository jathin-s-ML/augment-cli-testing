"""
State schema for the LangGraph agent.
"""

from typing import TypedDict, Annotated, Sequence, Optional, Dict, Any
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    State schema for the agent workflow.

    Simplified state with 3-node workflow:
    - augment_executor: Executes task and stores augment_result + session_id
    - analyzer: Auto-detects type and creates final_output
    - cleanup: Ends session

    Attributes:
        messages: Conversation history (accumulated)
        task: Current task description
        augment_result: Raw result from Augment SDK
        final_output: Final formatted output (auto-detected type)
        session_id: Augment SDK session ID for continuity
        metadata: Additional metadata
    """
    # Messages are accumulated using operator.add
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # Task information
    task: str

    # Results from nodes
    augment_result: Optional[str]
    final_output: Optional[str]

    # Session management
    session_id: Optional[str]

    # Additional context
    metadata: Optional[Dict[str, Any]]

