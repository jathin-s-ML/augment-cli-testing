"""
LangGraph workflow definition.
"""

from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    augment_executor_node,
    analyzer_node,
    cleanup_node
)


def create_agent_graph():
    """
    Create the LangGraph agent workflow.

    Simplified 3-node workflow:
    1. Augment Executor: Execute using Augment SDK with session
    2. Analyzer: Auto-detect result type, format output with headers
    3. Cleanup: End session and clean up resources

    Returns:
        Compiled LangGraph workflow
    """
    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes (3 nodes only)
    workflow.add_node("augment_executor", augment_executor_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("cleanup", cleanup_node)

    # Define the flow
    workflow.set_entry_point("augment_executor")

    # Linear flow: executor → analyzer → cleanup
    workflow.add_edge("augment_executor", "analyzer")
    workflow.add_edge("analyzer", "cleanup")
    workflow.add_edge("cleanup", END)

    # Compile the graph
    app = workflow.compile()

    return app

