"""
LangGraph workflow definition.
"""

from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    planner_node,
    augment_executor_node,
    analyzer_node,
    formatter_node,
    cleanup_node
)


def create_agent_graph():
    """
    Create the LangGraph agent workflow.
    
    Workflow:
    1. Planner: Classify the task
    2. Augment Executor: Execute using Augment SDK
    3. Analyzer: Process the result
    4. Formatter: Format for user
    5. Cleanup: Clean up resources
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("augment_executor", augment_executor_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("formatter", formatter_node)
    workflow.add_node("cleanup", cleanup_node)
    
    # Define the flow
    workflow.set_entry_point("planner")
    
    # Linear flow for now (can add conditional edges later)
    workflow.add_edge("planner", "augment_executor")
    workflow.add_edge("augment_executor", "analyzer")
    workflow.add_edge("analyzer", "formatter")
    workflow.add_edge("formatter", "cleanup")
    workflow.add_edge("cleanup", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

